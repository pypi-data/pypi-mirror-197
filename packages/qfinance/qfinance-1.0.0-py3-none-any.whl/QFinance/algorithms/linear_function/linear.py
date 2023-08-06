#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright (c) 2022 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
This module implements the linear function operator.
Reference: http://arxiv.org/abs/1905.02666
"""

import numpy as np

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegPool, QRegStorage


class SimpleLinearFunction:
    """
    This class implements the simple linear function.
    f: [0, ..., 2^n - 1] --> [0, 1]
    f(i) = alpha * i + beta
    discretized to 2^n grid points.

    Requires n+1 qubits, the first n qubits are used to store the input.
    The last qubit is used to store the rotated angle.
    It's the caller's duty to guarantee the last qubit be initialized to |0>.

    After the call, the last qubit is in the state
        cos( (scaling*f(i) + res_angle) / 2 ) |0> + sin( (scaling*f(i) + res_angle) / 2 ) |1>
    """

    def __init__(self, n: int, alpha: float, beta: float):
        """
        Initialize the linear function.

        :param n: number of qubits used to encode the input
        :param alpha: the slope of the linear function
        :param beta: the intercept of the linear function
        :param scaling: the scaling factor which appears before f(i)
        :param res_angle: the extra angle of the rotation aside from scaling * f(i)
        """
        self.n_ = n
        self.alpha_ = alpha
        self.beta_ = beta
        self.scaling_ = 1
        self.res_angle_ = np.pi / 2
        self.check_range()


    @property
    def alpha(self):
        return self.alpha_
    
    @property
    def beta(self):
        return self.beta_
    
    @property
    def scaling(self):
        return self.scaling_
    
    @property
    def res_angle(self):
        return self.res_angle_
    
    @alpha.setter
    def alpha(self, alpha: float):
        self.alpha_ = alpha
    
    @beta.setter
    def beta(self, beta: float):
        self.beta_ = beta

    @scaling.setter
    def scaling(self, scaling: float):
        self.scaling_ = scaling

    @res_angle.setter
    def res_angle(self, res_angle: float):
        self.res_angle_ = res_angle

    
    def check_range(self):
        """
        check that the given input alpha and beta is suitable:
        alpha * i + beta does not go out of range [-1, 1] for any i in range [0, 2^n - 1]
        """
        boundary_value1 = self.alpha_ * (2 ** self.n_ - 1) + self.beta_
        boundary_value2 = self.alpha_ * 0 + self.beta_
        if boundary_value1 > 1 or boundary_value1 < -1 or boundary_value2 > 1 or boundary_value2 < -1:
            raise ValueError('alpha * i + beta is out of range [-1, 1] for some i in range [0, 2^n - 1]')
    

    def __call__(self, qreg: list[QRegStorage]):
        """
        Apply the linear function to the input.
        The first n qubits are used to store the input, in the big-endian order:
        qreg[0] is the most significant bit, qreg[n-1] is the least significant bit.

        The last qubit is used to store the rotated angle.
        It's the caller's duty to guarantee the last qubit be initialized to |0>.

        After the call, the last qubit is in the state
        cos( (scaling*f(i) + res_angle) / 2 ) |0> + sin( (scaling*f(i) + res_angle) / 2 ) |1>

        :param qreg: the input qubits
        """
        # check that qreg is a list of QRegStorage
        if not isinstance(qreg, list):
            raise TypeError('qreg must be a list of QRegStorage')
        if not all(isinstance(q, QRegStorage) for q in qreg):
            raise TypeError('qreg must be a list of QRegStorage')
        
        # check that the number of qubits is correct
        if len(qreg) != self.n_ + 1:
            raise ValueError(f'qreg must have {self.n_ + 1} qubits')
        
        # check that the last qubit is initialized to |0>
        # TODO: is there any good way to check this?

        # apply the gates
        RY(self.scaling_ * self.beta_ + self.res_angle_)(qreg[-1])

        for i in range(self.n_):
            dual = self.n_ - i - 1
            CRY(self.scaling_ * self.alpha_ * 2 ** i)(qreg[dual], qreg[-1])

    def __str__(self):
        return f'LinearFunction(n={self.n_}, alpha={self.alpha_}, beta={self.beta_})'

    def __repr__(self):
        return f'LinearFunction(n={self.n_}, alpha={self.alpha_}, beta={self.beta_})'
    
    def p1_exact(self, i: int):
        """
        calculate the exact value of P1, the probability of measuring 1 in the last qubit,
        when the input is i
        """
        inner = (self.scaling_ * (self.alpha_ * i + self.beta_) + self.res_angle_) / 2
        return np.sin(inner) ** 2
    
    def p1_approximate(self, i: int):
        """
        return the approximate value of P1, when self.scaling is very small,
        when the input is i
        """
        return self.scaling_ * (self.alpha_ * i + self.beta_) + 1 / 2
    

class LinearFunctionConverter:
    """
    Transform linear function presented in different forms
    """

    def __init__(self, n: int, domain: tuple[float, float], slope_intercept: tuple[float, float]):
        """
        :param n: number of qubits used to encode the input
        """
        self.n_ = n
        self.i_min = 0
        self.i_max = 2 ** n - 1
        self.x_min = 1.0 * domain[0]
        self.x_max = 1.0 * domain[1]
        self.slope = 1.0 * slope_intercept[0]
        self.intercept = 1.0 * slope_intercept[1]
        self.fmin = self.slope * self.x_min + self.intercept
        self.fmax = self.slope * self.x_max + self.intercept

    def i2x(self, i: int):
        """
        convert the input i to x
        """
        return self.x_min + (self.x_max - self.x_min) * i / self.i_max
    
    def f_orig(self, x: float):
        """
        the original function
        """
        return self.slope * x + self.intercept
    
    def codomain_map(self, y: float):
        """
        the codomain map, into the range [-1, 1]
        """
        return 2 * ( (y - self.fmin) / (self.fmax - self.fmin) ) - 1
    
    def f_x(self, i: int):
        """
        the function f(x), which is the composition of i2x and f_orig
        """
        return self.f_orig(self.i2x(i))
    
    def fhat(self, i: int):
        """
        the final function fhat, which is the composition of i2x, f_orig and codomain_map
        """
        return self.codomain_map(self.f_orig(self.i2x(i)))


class LinearFunction:
    """
    This class implements the linear function.
    f: [x_min, x_max] --> [f_min, f_max]
    f(x) = alpha * x + beta

    The interval [x_min, x_max] is discretized to 2^n grid points.

    Requires n+1 qubits, the first n qubits are used to store the input,
    the last qubit is used to store the rotated angle.

    On input, the last qubit must be initialized to |0>.

    :param n: number of qubits used to encode the input
    :param alpha: the slope of the linear function
    :param beta: the intercept of the linear function
    """

    def __init__(self, n: int, domain: tuple[float, float], slope_intercept: tuple[float, float]):
        """
        Initialize the linear function.

        :param n: number of qubits used to encode the input
        :param domain: the tuple (x_min, x_max)
        :param slope_intercept: the tuple (alpha, beta)
        """
        self.n_ = n
        self.alpha_ = slope_intercept[0]
        self.beta_ = slope_intercept[1]
        self.xmin_ = domain[0]
        self.xmax_ = domain[1]
        self.domain_ = (self.xmin_, self.xmax_)
        self.slope_intercept_ = (self.alpha_, self.beta_)

        self.slf = SimpleLinearFunction(n, self.alpha_, self.beta_)

        self.lfc = LinearFunctionConverter(n, self.domain, self.slope_intercept)
        self.fhat = self.lfc.fhat
        self.f_x = self.lfc.f_x

    @property
    def alpha(self):
        """
        retrive the slope of the linear function
        """
        return self.alpha_
    
    @property
    def beta(self):
        """
        retrive the intercept of the linear function
        """
        return self.beta_
    
    # @alpha.setter
    # def alpha(self, alpha: float):
    #     self.alpha_ = alpha
    #     self.slope_intercept_ = (self.alpha_, self.beta_)
    
    # @beta.setter
    # def beta(self, beta: float):
    #     self.beta_ = beta
    #     self.slope_intercept_ = (self.alpha_, self.beta_)
    
    @property
    def domain(self):
        """
        retrieve the domain (xmin, xmax) of the linear function
        """
        return self.domain_
    
    @property
    def slope_intercept(self):
        """
        retrieve the slope and intercept of the linear function
        """
        return self.slope_intercept_
    
    @domain.setter
    def domain(self, domain: tuple[float, float]):
        """
        set the domain (xmin, xmax) of the linear function
        """
        self.xmin_ = domain[0]
        self.xmax_ = domain[1]
        self.domain_ = (self.xmin_, self.xmax_)
        self.lfc = LinearFunctionConverter(self.n_, self.domain, self.slope_intercept)
        self.fhat = self.lfc.fhat
        self.f_x = self.lfc.f_x

    @slope_intercept.setter
    def slope_intercept(self, slope_intercept: tuple[float, float]):
        """
        set the slope and intercept of the linear function
        """
        self.alpha_ = slope_intercept[0]
        self.beta_ = slope_intercept[1]
        self.slope_intercept_ = (self.alpha_, self.beta_)
        self.lfc = LinearFunctionConverter(self.n_, self.domain, self.slope_intercept)
        self.fhat = self.lfc.fhat
        self.f_x = self.lfc.f_x
    

    def __call__(self, qreg: list[QRegStorage]):
        """
        Apply the linear function to the input.
        qreg has n + 1 qubits.
        The first n qubits are used to store the input, in the big-endian order:
        qreg[0] is the most significant bit, qreg[n-1] is the least significant bit.

        The last qubit is used to store the rotated angle.
        It's the caller's duty to guarantee the last qubit be initialized to |0>.

        After the call, the last qubit is in the state
        cos( f(i)/2 ) |0> + sin( f(i)/2 ) |1>

        :param qubits: the input qubits
        """
        # check that qreg is a list of QRegStorage
        if not isinstance(qreg, list):
            raise TypeError('qreg must be a list of QRegStorage')
        if not all(isinstance(q, QRegStorage) for q in qreg):
            raise TypeError('qreg must be a list of QRegStorage')