from typing import List, Optional

import pymongo
from bson import ObjectId
from cache import AsyncLRU

from mongorepository.repositories.base import AbstractRepository, T


class Repository(AbstractRepository[T]):
    def __init__(self, database):
        super().__init__(database)

    def __get_paginated_documents(self, query, sort, next_key=None):
        query, next_key_fn = self.generate_pagination_query(
            query, sort, next_key
        )  # noqa: E501

        cursor = (
            self.get_collection()
            .find(query, projection=self.get_projection())
            .sort(sort)
            .limit(self._query_limit)
        )

        documents = [document for document in cursor]  # noqa: E501

        return {
            "total": len(documents),
            "results": documents,
            "next_page": next_key_fn(documents),
        }

    def list_all(
        self,
        query: Optional[dict] = None,
        sort: Optional[list] = None,
        next_page: Optional[dict] = None,
    ) -> List[T]:
        collection = self.get_collection()
        if query is None:
            query = {}

        if not sort:
            sort = [("_id", pymongo.DESCENDING)]

        if self._paginated:
            result = self.__get_paginated_documents(query, sort, next_page)
            self._convert_paginated_results_to_model(result)
            return result

        cursor = collection.find(query).sort(sort)

        return [self._model_class(**document) for document in cursor]

    @AsyncLRU(maxsize=128)
    def find_by_query(self, query: dict) -> Optional[T]:
        collection = self.get_collection()
        if document := collection.find_one(query):
            return self._model_class(**document)
        return None

    @AsyncLRU(maxsize=128)
    def find_by_id(self, document_id: str) -> Optional[T]:
        collection = self.get_collection()
        document = collection.find_one(
            {"_id": ObjectId(document_id)},
            projection=self.get_projection(),
        )
        return self._model_class(**document)

    def save(self, model: T) -> T:
        collection = self.get_collection()
        raw_model = model.dict(by_alias=True, exclude_none=True)

        if id_model := raw_model.get("_id", raw_model.get("id")):
            collection.update_one(
                {"_id": ObjectId(id_model)}, {"$set": raw_model}
            )  # noqa: E501
            return self.find_by_id(model.id)

        document = collection.insert_one(raw_model)

        return self.find_by_id(str(document.inserted_id))

    def bulk_create(self, models: List[T]) -> List[ObjectId]:
        raw_models = [model.dict(exclude_none=True) for model in models]
        result = self.get_collection().insert_many(raw_models)
        return result.inserted_ids

    def delete(self, model: T) -> bool:
        collection = self.get_collection()
        raw_model = model.dict(by_alias=True, exclude_none=True)
        if id_model := raw_model.get("_id", raw_model.get("id")):
            collection.delete_one({"_id": ObjectId(id_model)})
            return True
        return False
