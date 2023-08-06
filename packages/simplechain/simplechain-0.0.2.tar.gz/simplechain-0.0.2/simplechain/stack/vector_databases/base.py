from abc import ABC, abstractmethod
from typing import Tuple, List, Any

import numpy as np


class VectorDatabase(ABC):
    @abstractmethod
    def add(self, embed: np.ndarray, metadata: Any):
        """
        Add a name and its embed to the database
        :param metadata:
        :param name:
        :param embed:
        :return:
        """
        pass
    @abstractmethod
    def save(self):
        """
        Build the database
        :return:
        """
        pass

    @abstractmethod
    def get_nearest_neighbors(self, query_embed: np.ndarray, k: int = 1) -> List[Tuple[str, float]]:
        """
        Given a query embed, get the k nearest neighbors with their distances
        :param query_embed:
        :param k:
        :return: k nearest neighbors as strings with their distances
        """
        pass
