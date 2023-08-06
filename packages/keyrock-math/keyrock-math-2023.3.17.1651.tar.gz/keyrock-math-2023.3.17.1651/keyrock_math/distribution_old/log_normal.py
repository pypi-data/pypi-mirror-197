import numpy as np
import scipy.stats as sps
from scipy.special import erfinv
import numpy as np
import math

from .analytic import Analytic

import marshmallow as m
import logging
logger = logging.getLogger(__name__)


SQRT2 = math.sqrt(2)
SQRT2PI = math.sqrt(2 * math.pi)
MIN_X = 0.000000001

class LogNormal(Analytic):
    class ConfigSchema(Analytic.ConfigSchema):
        loc = m.fields.Float(missing=0)
        scale = m.fields.Float(missing=1)

    def load_config(self, config):
        super().load_config(config)
        self.mu = config['loc']
        self.sigma = config['scale']

        # a = 1 + (sigma / mu) ** 2
        # s = np.sqrt(np.log(a))
        # scale = mu / np.sqrt(a)
        # logger.debug('LogNormal mu:{} sigma:{} a:{} s:{} scale:{}'.format(
        #     mu, sigma, a, s, scale))

        # zeta = np.sqrt(np.log(1 + (sigma / mu) ** 2)) # shape factor
        # lambda_value = np.log(mu) - 0.5 * zeta ** 2   # expected value of ln x
        # logger.debug('LogNormal mu:{} sigma:{} zeta:{} lambda:{}'.format(
        #     mu, sigma, zeta, lambda_value))

        # self.rv = sps.lognorm(
        #     s=sigma,
        #     loc=mu)

        # self.rv = sps.lognorm(
        # 	s=s,
        #     loc=0,
        #     scale=scale)

    def get_random_value(self):
        val = np.random.lognormal(self.mu, self.sigma)
        return val

    def quantile(self, p):
        Q = math.sqrt(2.0 * self.sigma * self.sigma)
        Q *= erfinv(2.0 * p - 1.0)
        Q += self.mu
        Q = math.exp(Q)
        return Q

    def cdf(self, x):
        # Avoid SciPy LogNormal implementation
        #  since it inteprets mu differently
        if (x < MIN_X):
            return 0.0

        CDF = 0.5 * (1.0 + math.erf((np.log(x) - self.mu) / (self.sigma * SQRT2)))
        return CDF;

    def pdf(self, x):
        # Avoid SciPy LogNormal implementation
        #  since it inteprets mu differently
        if (x < MIN_X):
            return 0.0

        PDF = 1.0 / (x * self.sigma * SQRT2PI)
        PDF *= math.exp(-1.0 * ((np.log(x) - self.mu) ** 2) / (2.0 * self.sigma * self.sigma))
        return PDF

    def get_x_min(self):
        return 0

    def get_x_max(self):
        return math.inf
