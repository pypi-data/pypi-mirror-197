import marshmallow as m
import numpy as np
import scipy.stats as sps
import math

import logging
logger = logging.getLogger(__name__)

from keyrock_hcs import hcs


class Distribution(hcs.HCSObject):
    class ConfigSchema(hcs.HCSObject.ConfigSchema):
        class Meta:
            pass

    def  __init__(self, config=None):
        super().__init__(config)
        self.cache_init()

    def cache_init(self):
        pass

    def get_x_min(self):
        return -math.inf

    def get_x_max(self):
        return math.inf

    def get_percentile(self, p):
        raise NotImplementedError()

    def get_x_space(self):
        raise NotImplementedError()

    def get_random_value(self, size=1):
        raise NotImplementedError()

    def quantile(self, p):
        raise NotImplementedError()

    def cdf(self, x):
        raise NotImplementedError()

    def pdf(self, x):
        raise NotImplementedError()