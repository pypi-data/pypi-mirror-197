import math
import sys
import numpy as np
from .distribution import Distribution

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Analytic(Distribution):
    class ConfigSchema(Distribution.ConfigSchema):
        class Meta:
            include = {
                # 'min': m.fields.Float(missing=-sys.float_info.max),
                # 'max': m.fields.Float(missing=sys.float_info.max),
            }

    def load_config(self, config):
        super().load_config(config)
        # self.min_rv = config['min']
        # self.max_rv = config['max']

    def cache_init(self):
        self.x_space = None
        self.rv_cache = None
        self.rv_index = 0

    def get_random_value(self):
        if self.rv_cache is None:
            self.rv_cache = self.rv.rvs(10001)

        val = self.rv_cache[self.rv_index % 10001]
        self.rv_index += 1

        # Test comment
        # val = self.rv.rvs(size=1)[0]
        # if val > self.max_rv:
        #     return self.max_rv
        # if val < self.min_rv:
        #     return self.min_rv

        return val

    def quantile(self, p):
        return self.rv.ppf(p)

    def cdf(self, x):
        return self.rv.cdf(x)

    def pdf(self, x):
        return self.rv.pdf(x)

    def get_x_min(self):
        return -math.inf

    def get_x_max(self):
        return math.inf

    def get_percentile(self, p):
        return self.quantile(p)

    def get_x_space(self):
        if self.x_space is None:
            self.x_space = np.linspace(self.rv.ppf(0.01), self.rv.ppf(0.99), 100)
        return self.x_space