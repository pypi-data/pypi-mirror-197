from keyrock_hcs import hcs

from .constant import Constant
from .uniform import Uniform
from .logistic import Logistic
from .normal import Normal
from .skew_normal import SkewNormal
from .log_normal import LogNormal
from .beta import Beta
from .gamma import Gamma

type_map = {
    'constant': Constant,
    'uniform': Uniform,
    'logistic': Logistic,
    'normal': Normal,
    'skew_normal': SkewNormal,
    'log_normal': LogNormal,
    'beta': Beta,
    'gamma': Gamma,
}

factory = hcs.TypeConfigFactory(type_map)
