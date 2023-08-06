import logging
import numpy as np
import scipy.stats as sps
import math
from typing import List, Literal

from abc import abstractmethod

from .distribution import Distribution

logger = logging.getLogger(__name__)

class Analytic(Distribution):
    _rv: None = None
    _rv_cache: None = None
    _rv_index: int = 0

    def pdf(self, x:float) -> float:
        return self._rv.pdf(x)

    def cdf(self, x:float) -> float:
        return self._rv.cdf(x)

    def quantile(self, p:float) -> float:
        return self._rv.ppf(p)

    def get_random_value(self, size=1) -> float:
        if self._rv_cache is None:
            self._rv_cache = self.rv.rvs(10001)

        val = self._rv_cache[self.rv_index % 10001]
        self._rv_index += 1
