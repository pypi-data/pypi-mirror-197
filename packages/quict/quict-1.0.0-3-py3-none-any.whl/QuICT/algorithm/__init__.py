#!/usr/bin/env python
# -*- coding:utf8 -*-
# @TIME    : 2020/2/11 10:30
# @Author  : Han Yu
# @File    : __init__.py.py

from ._algorithm import Algorithm
from .quantum_algorithm import *
from .weight_decision import WeightDecision

try:
    from QuICT_ml.utils import GpuSimulator as MLSimulator
    from QuICT_ml import ansatz_library as AnsatzLibrary
    from QuICT_ml import model as MLModel
    from QuICT_ml import utils as MLUtils
except:
    MLSimulator = None
    AnsatzLibrary = None
    MLModel = None
    MLUtils = None
    print(
        "Please install pytorch, cupy and quict_ml first, you can use 'pip install quict-ml' to install quict_ml. "
    )

