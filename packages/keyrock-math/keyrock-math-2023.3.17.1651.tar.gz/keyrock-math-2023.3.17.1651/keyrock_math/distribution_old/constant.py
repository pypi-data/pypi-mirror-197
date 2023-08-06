from .distribution import Distribution

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Constant(Distribution):
    class ConfigSchema(Distribution.ConfigSchema):
        loc = m.fields.Float(missing=0)

    def load_config(self, config):
        super().load_config(config)
        self.v = config['loc']

    def get_x_min(self):
        return self.v

    def get_x_max(self):
        return self.v

    def get_percentile(self, p):
        return self.v

    def get_random_value(self, size=1):
        return self.v

    def cdf(self, x):
        return self.v * x

    def pdf(self, x):
        return self.v