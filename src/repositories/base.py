from abc import ABC, abstractmethod


class ICrudRepository(ABC):
    @abstractmethod
    def store(self, data):
        pass

    @abstractmethod
    def update(self, entity, data):
        pass

    @abstractmethod
    def delete(self, entity):
        pass

    @abstractmethod
    def find_by_pk(self, entity_id):
        pass

    @abstractmethod
    def get_one(self, filter_data):
        pass

    @abstractmethod
    def get_many(self, paging, filter_data):
        pass

    @abstractmethod
    def build_query(filter_data):
        pass

