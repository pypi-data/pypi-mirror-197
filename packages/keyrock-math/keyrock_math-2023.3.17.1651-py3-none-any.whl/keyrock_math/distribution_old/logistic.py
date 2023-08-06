import numpy as np
import scipy.stats as sps

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


class Logistic(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        loc = m.fields.Float(missing=0)
        scale = m.fields.Float(missing=1)

    def load_config(self, config):
        super().load_config(config)
        self.rv = sps.logistic(config['loc'], config['scale'])
