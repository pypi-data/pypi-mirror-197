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
This module implements the Quantum Monte Carlo Integration algorithm.
Reference: http://arxiv.org/abs/1905.02666
"""

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegStorage

from QFinance.algorithms import MultiQubitStateOP
from QFinance.algorithms import QuantumComparatorOP
from QFinance.algorithms.linear_function import SimplePiecewiseLinear
from QFinance.algorithms.amplitude_estimation import AEProblem
from QFinance.algorithms.amplitude_estimation import IQAE, MLAE

from QFinance.utils import sub_qreg, full_qreg

import numpy



class SimpleQMC:
    """
    This class implements the Quantum Monte Carlo Integration algorithm for the simple function:
    f(x) = max{0, x - xk} where xk is a constant.
    The goal is to calculate the expectation value of f(x) wrt. given distribution on [xmin, xmax].
    """
    
    def __init__(self, qubit_num: int):
        """
        :param qubit_num: The number of qubits used in the prepare state function.
        
        """
        self.qnum = qubit_num
        self.qtotal = 2 * qubit_num + 1 + 1
        self.env = QEnv()
        self.qregL = self.env.Q.createList(self.qtotal)

        self.xmin = None
        self.xmax = None
        self.xk = None

        self.distribution = None

        self.working_qregL = []
        self.ancilla_qregL = [] 
        self.comp_qreg = None
        self.angle_qreg = None

        self.scaling_ = None

        self.pwl = None
        self.aep = None


    # def init_check(self):
    #     """
    #     check initial condition.
    #     """
    #     assert self.qnum > 0
    #     assert self.qtotal > 0
        

    def load_dist(self, dist: numpy.ndarray):
        """
        load distribution.
        :param dist: The distribution on [xmin, xmax], dist should be a normalized vector, i.e., sum_{i=0}^{2^n-1} |v_i|^2 = 1.
        """
        self.distribution = dist
        assert len(self.distribution) == 2 ** self.qnum, "The length of distribution is not equal to 2 ** qnum."


    def set_linear(self, domain: tuple[float, float], xk: float):
        """
        set the linear function which will be loaded after the quantum comparator.
        the linear function is f(x) = x - xk where xk is a constant.
        The piecewise linear function will be max{0, x - xk} defined on the interval [xmin, xmax].

        :param pwl: The tuple of (xmin, xmax, xk) which defines the linear function.
        """
        self.xmin, self.xmax = domain
        self.xk = xk
        assert self.xmin < self.xmax
        assert self.xk >= self.xmin and self.xk <= self.xmax


    def set_scaling(self, scaling: float):
        """
        set the scaling factor for the linear function.
        """
        self.scaling_ = scaling


    def __print__(self) -> None:
        print("xmin: ", self.xmin)
        print("xmax: ", self.xmax)
        print("xk: ", self.xk)
        print("function:", f"f(x) = max{{0, x - {self.xk}}} on [{self.xmin}, {self.xmax}]")
        print("qnum: ", self.qnum)
        print("qtotal: ", self.qtotal)
        # print("distribution: ", self.distribution)
    

    def create_AEProblem(self) -> AEProblem:
        """
        prepare state and load function f(x) into the quantum register.
        """

        # set the qregL
        self.working_qregL = self.qregL[0: self.qnum]
        self.ancilla_qregL = self.qregL[self.qnum: 2 * self.qnum]
        self.comp_qreg = self.qregL[2 * self.qnum]
        self.angle_qreg = self.qregL[2 * self.qnum + 1]

        # prepare state
        self.state = MultiQubitStateOP(self.distribution)
        self.state.load_to(self.working_qregL)

        # load the piecewise linear function
        self.pwl = SimplePiecewiseLinear((self.xmin, self.xmax), self.qnum, self.xk)
        ymax = self.pwl.ymax
        ymin = self.pwl.ymin
        beta = 1 / 2 - self.pwl.scaling * (ymax + ymin) / (ymax - ymin)
        # print(f"ymin: {ymin:.3f}, ymax: {ymax:.3f}, beta: {beta:.3f}")

        if self.scaling_ is not None:
            self.pwl.scaling = self.scaling_
        self.pwl.apply_to(self.working_qregL, self.ancilla_qregL, self.comp_qreg, self.angle_qreg)

        # create the AE problem
        self.aep = AEProblem(self.env, self.qtotal)
        return self.aep
    

    def run_iqae(self) -> float:
        """
        run the algorithm, use IQAE to estimate the expectation value of f(x) wrt. given distribution on [xmin, xmax].
        
        :return: The expectation value of f(x) wrt. given distribution on [xmin, xmax].
        """
        # self.init_check()
        # self.__print__()
        aep = self.create_AEProblem()
        self.iqae = IQAE(aep)
        self.iqae.epsilon = 0.001
        self.iqae.alpha = 0.05
        self.iqae.num_shots = 10000
        # self.iqae.set_confidence_interval_method("CH")
        # self.iqae.group_same_k = False
        # iqae.set_shots(shots)
        self.iqae.run()
        self.measured_P1 = self.iqae.estimated_amp
        self.expectation = self.recover_amp(self.measured_P1)
        return self.expectation
    

    def run_mlae(self, Q_powers: list[int], shots: list[int], precision: float = 1E-4) -> float:
        """
        run the algorithm, use MLAE to estimate the expectation value of f(x) wrt. given distribution on [xmin, xmax].

        :return: The measured expectation value of f(x) wrt. given distribution on [xmin, xmax].
        """
        aep = self.create_AEProblem()
        self.mlae = MLAE(aep)
        self.mlae.set_grid_precision(precision)
        
        error = None

        self.mlae.setup_arbitrary_scheme(Q_powers, shots)
        error = self.mlae.estimated_error()
        # display error as scientific notation
        # print(f"estimated error of MLAE arbitrary scheme: {error:.4e}")

        self.mlae.run()
        self.measured_P1 = self.mlae.estimated_amp
        # print(f"measured P1: {self.measured_P1:.5f}")
        self.measured_expectation = self.recover_amp(self.measured_P1)

        # recover the lower and upper bound of the expectation
        measured_expectation_lower_bound = self.recover_amp(self.measured_P1 - error)
        measured_expectation_upper_bound = self.recover_amp(self.measured_P1 + error)
        self.expectation_random_error = abs(measured_expectation_upper_bound - measured_expectation_lower_bound) / 2
        # print(f"measured QMC expectation: {self.measured_expectation:.5f}")
        return self.measured_expectation
    


    def run_mlae_demo(self) -> float:
        """
        run the algorithm, use MLAE to estimate the expectation value of f(x) wrt. given distribution on [xmin, xmax].

        :return: The measured expectation value of f(x) wrt. given distribution on [xmin, xmax].
        """
        aep = self.create_AEProblem()
        self.mlae = MLAE(aep)
        self.mlae.set_grid_precision(1E-4)
        
        scheme = "arbitrary"
        error = None

        if scheme == "linear":
            shots = 100000
            self.mlae.num_terms = 15
            # 12 is large enough
            self.mlae.setup_linear_scheme(shots)
            error = self.mlae.estimated_error()
            print(f"estimated error of MLAE linear scheme: {error:.4e}")

        elif scheme == "exponential":
            shots = 100000
            self.mlae.num_terms = 7
            self.mlae.setup_exponential_scheme(shots)
            error = self.mlae.estimated_error()
            print(f"estimated error of MLAE exponential scheme: {error:.4e}")

        elif scheme == "arbitrary":
            Q_power_list = [2, 3, 5, 10]
            shots_list = [100000] * len(Q_power_list)
            self.mlae.setup_arbitrary_scheme(Q_power_list, shots_list)
            error = self.mlae.estimated_error()
            # display error as scientific notation
            print(f"estimated error of MLAE arbitrary scheme: {error:.4e}")

        self.mlae.run()
        self.measured_P1 = self.mlae.estimated_amp
        # print(f"measured P1: {self.measured_P1:.5f}")
        self.measured_expectation = self.recover_amp(self.measured_P1)

        # recover the lower and upper bound of the expectation
        measured_expectation_lower_bound = self.recover_amp(self.measured_P1 - error)
        measured_expectation_upper_bound = self.recover_amp(self.measured_P1 + error)
        self.expectation_random_error = (measured_expectation_upper_bound - measured_expectation_lower_bound) / 2
        # print(f"measured QMC expectation: {self.measured_expectation:.5f}")
        return self.measured_expectation
    

    def recover_amp(self, measured_P1: float) -> float:
        """
        recover the desired expectation from the measured probability of |1> state.
        the measured P1 is equal to the return value from amplitude estimation.
        """
        measured_expectation = self.pwl.measured_exp_from_P1(measured_P1)
        return measured_expectation