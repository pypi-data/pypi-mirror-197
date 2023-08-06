import numpy as np
import scipy.stats as sps

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class SkewNormal(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        loc = m.fields.Float(missing=0)
        scale = m.fields.Float(missing=1)
        a = m.fields.Float(missing=0)

    def load_config(self, config):
        super().load_config(config)
        self.rv = sps.skewnorm(
        	loc=config['loc'],
        	scale=config['scale'],
        	a=config['a'])
