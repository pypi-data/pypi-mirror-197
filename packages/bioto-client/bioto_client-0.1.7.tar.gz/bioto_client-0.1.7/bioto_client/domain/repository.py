from abc import ABC, abstractmethod
from datetime import datetime
from pydantic import BaseModel
from requests import Response


class Garden(BaseModel):
    name: str


class Repository(ABC):
    @abstractmethod
    def get_gardens(self) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def get_subscriptions(self) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def device_data(
        self,
        device_id: str,
        offset: datetime,
        range: int = 1
    ) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def search_garden(self, query: str) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def subscribe_garden(self, uuid: str) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def update_client(self) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self) -> Response | dict:
        raise NotImplementedError()
