from abc import ABC, abstractmethod
from uuid import uuid4

from typing import Tuple
from .ticket import Ticket, Feedback


class Worker(ABC):
    def __init__(self) -> None:
        super(Worker, self).__init__()
        self.busy = False

    def __enter__(self):
        self.busy = True
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.teardown()
        self.busy = False
        return False

    @property
    def id(self) -> str:
        return str(uuid4())

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def duties(self) -> Tuple:
        pass

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def teardown(self) -> None:
        pass

    @abstractmethod
    def doing(self, ticket: Ticket) -> Feedback:
        pass
