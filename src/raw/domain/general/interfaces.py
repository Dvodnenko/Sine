from abc import ABC, abstractmethod

from ..config.entity import Config


class GeneralRepository(ABC):
    '''
    This interface (or implementation) does not relate to a specific Entity.

    It can be used to get some common system `Raw` information.
    '''

    @abstractmethod
    def get_max_ID(self, config: Config) -> int: ...
