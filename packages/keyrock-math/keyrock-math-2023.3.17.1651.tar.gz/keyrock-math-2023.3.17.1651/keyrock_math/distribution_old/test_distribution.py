import unittest
import math

from . import *

import logging
logger = logging.getLogger(__name__)


class TestConstant(unittest.TestCase):
    def test_v(self):
        test_var = Constant()
        self.assertEqual(test_var.get_random_value(), 0)

        constant_var0 = Constant({'loc': 0})
        self.assertEqual(constant_var0.get_random_value(), 0)

        constant_var1 = Constant({'loc': 1})
        self.assertEqual(constant_var1.get_random_value(), 1)

    def test_cdf(self):
        constant_var10 = Constant({'loc': 10})
        self.assertEqual(constant_var10.cdf(20), 200)
        self.assertEqual(constant_var10.pdf(0), 10)
        self.assertEqual(constant_var10.pdf(1), 10)


class TestUniform(unittest.TestCase):
    def test_uniform(self):
        test_var = Uniform({'max': 2.0})
        cdf = test_var.cdf(0.5)
        self.assertAlmostEqual(cdf, 0.25)
        pdf = test_var.pdf(0.5)
        self.assertAlmostEqual(pdf, 0.5)


class TestLogistic(unittest.TestCase):
    def test_cdf(self):
        test_var = Logistic()
        cdf0 = test_var.cdf(0)
        self.assertEqual(cdf0, 0.5)


class TestNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = Normal()
        cdf = test_var.cdf(0.0)
        self.assertAlmostEqual(cdf, 0.5)

        cdf = test_var.cdf(1.0)
        self.assertAlmostEqual(cdf, 0.841344746)

    def test_pdf(self):
        test_var = Normal()
        self.assertAlmostEqual(test_var.pdf(2.0), 0.05399096651)


class TestSkewNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = SkewNormal({'a': 1})
        cdf = test_var.cdf(0)
        self.assertAlmostEqual(cdf, 0.25)

        test_var = SkewNormal({'a': -1})
        cdf = test_var.cdf(0)
        self.assertAlmostEqual(cdf, 0.75)


class TestLogNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = LogNormal()

        p50 = test_var.get_percentile(.5)
        self.assertAlmostEqual(p50, 1.0)

        p75 = test_var.get_percentile(0.75)
        cdf = test_var.cdf(p75)
        self.assertAlmostEqual(cdf, 0.75)

    def test_pdf(self):
        test_var = LogNormal({'loc':0, 'scale':1})
        self.assertAlmostEqual(test_var.pdf(1.5), 0.24497365)


class TestGamma(unittest.TestCase):
    def test_gamma1(self):
        test_var = Gamma({'loc': 1})
        pdf0 = test_var.pdf(1)
        self.assertAlmostEqual(pdf0, 1.0)

    def test_gamma_half(self):
        test_var = Gamma({'rate': 0.5})
        pdf1 = test_var.pdf(1)
        self.assertAlmostEqual(pdf1, 0.30326532)


class TestBeta(unittest.TestCase):
    def test_pdf(self):
        test_var = Beta({})
        pdf = test_var.pdf(0.1)
        self.assertAlmostEqual(pdf, 1.0)
