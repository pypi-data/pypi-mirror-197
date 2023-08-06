from abc import ABC, abstractmethod
from typing import Union, List

import numpy as np
from pydantic import BaseModel


class TextEmbedder(BaseModel, ABC):
    @abstractmethod
    def embed(self, text: Union[List[str], str]) -> Union[List[np.ndarray], np.ndarray]:
        pass

