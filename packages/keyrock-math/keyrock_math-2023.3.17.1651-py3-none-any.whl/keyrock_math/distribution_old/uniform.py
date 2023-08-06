import scipy.stats as sps

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Uniform(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        class Meta:
            include = {
                'min': m.fields.Float(missing=0),
                'max': m.fields.Float(missing=1),
            }

    def load_config(self, config):
        super().load_config(config)
        self.min_rv = config['min']
        self.max_rv = config['max']
        scale = self.max_rv - self.min_rv
        self.rv = sps.uniform(loc=self.min_rv, scale=scale)

    def get_x_min(self):
        return self.min_rv

    def get_x_max(self):
        return self.max_rv
