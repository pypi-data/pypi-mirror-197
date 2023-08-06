import numpy as np
import scipy.stats as sps

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Gamma(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        class Meta:
            include = {
                'a': m.fields.Float(missing=1),
                'rate': m.fields.Float(missing=1),
                'loc': m.fields.Float(missing=0),
            }

    def load_config(self, config):
        super().load_config(config)
        scale = 1.0 / config['rate']
        self.rv = sps.gamma(
            a=config['a'],
            loc=config['loc'],
            scale=scale)
