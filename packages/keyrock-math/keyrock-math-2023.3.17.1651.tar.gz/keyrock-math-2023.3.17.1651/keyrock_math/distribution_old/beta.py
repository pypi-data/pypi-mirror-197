import numpy as np
import scipy.stats as sps

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Beta(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        class Meta:
            include = {
                'a': m.fields.Float(missing=1),
                'b': m.fields.Float(missing=1),
            }

    def load_config(self, config):
        super().load_config(config)
        self.rv = sps.beta(
            a=config['a'],
            b=config['b'],
            loc=0,
            scale=1)

    def get_x_min(self):
        return 0.0

    def get_x_max(self):
        return 1.0
