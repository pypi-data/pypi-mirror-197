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
This module defines a general amplitude estimation problem.
"""

from QCompute import *
from copy import deepcopy

from QFinance.utils import sub_qreg, full_qreg
from QFinance.utils import cnx, cnz


class AEProblem:
    """
    Amplitude estimation problem class.

    opA: the operator A, which satisfies
    A|0> = sqrt(1-a) |psi0>|0> + sqrt(a) |psi1>|1>
    `a` is the probability of measuring |1> in the ancilla qubit
    Equivalently, A |0> = cos(theta_a) |psi0>|0> + sin(theta_a) |psi1>|1>.
    On the left hand side, |0> represesnts an array of num_qubits zero states.

    num_qubits: number of qubits that operator A acts on
    envQ: the operator Q, which is the main unitary operator in the amplitude estimation algorithm.
    Q = A S0 A^dagger S_{psi0}
    """

    def __init__(self, envA: QEnv, num_qubits: int) -> None:
        """
        Initialize the amplitude estimation problem.
        :param opA: the operator A
        :param num_qubits: number of qubits that operator Q acts on
        """
        self.envA_ = envA
        # self.envA_copy_ = deepcopy(envA)
        self.num_qubits_ = num_qubits
        self.envQ_ = None
        

    @property
    def envA(self) -> QEnv:
        """
        Get the operator A.
        """
        return self.envA_

    @envA.setter
    def envA(self, envA: QEnv) -> None:
        """
        Set the operator A.
        """
        self.envA_ = envA

    @property
    def num_qubits(self) -> int:
        """
        Get the number of qubits that operator A acts on.
        """
        return self.num_qubits_

    @num_qubits.setter
    def num_qubits(self, num_qubits: int) -> None:
        """
        Set the number of qubits that operator A acts on.
        """
        self.num_qubits_ = num_qubits
    
    @property
    def envQ(self) -> QEnv:
        """
        Get the operator Q.
        """
        if self.envQ_ is None:
            # print('Assembling the operator Q...', end = '')
            self.assemble_Q()
            # print(' Done.')
        return self.envQ_
    
    @envQ.setter
    def envQ(self, envQ: QEnv) -> None:
        """
        Set the operator Q.
        """
        self.envQ_ = envQ
    
    def reflection_S_psi0(self) -> QEnv:
        """
        Construct the reflection operator S_{psi0}.
        S_{psi0} = I \otimes Z is a reflection about the bad state |psi0>|0>
        |phi_0>|0> -> -|phi_0>|0>
        |phi_0>|1> -> |phi_0>|1>
        """
        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        Z(q[self.num_qubits_ - 1])
        return env

    def reflection_S0(self) -> QEnv:
        """
        Construct the reflection operator S0.
        S0 is the reflection about the state |0>^n, where n = self.num_qubits
        S0 = 2|0...0><0...0| - I
        S0 = X^n C^{n-1}Z X^n 
        """
        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        qreglist = full_qreg(q)
        for i in range(self.num_qubits_):
            X(q[i])
        cnz(self.num_qubits_ - 1, env)
        for i in range(self.num_qubits_):
            X(q[i])
        return env

    def assemble_Q(self) -> None:
        """
        Assemble the Grover operator Q.
        Q = A S0 A^dagger S_{psi0}
        The circuit of Q has the same size as the circuit of A.
        """
        # this is the main env associated to opQ 

        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        qreglist = full_qreg(q)

        # in case where an instance of AEProblem calls assemble_Q() multiple times
        envA = deepcopy(self.envA_)

        # construct A and A^dagger operators
        # the inverseCircuit() method already uses the deepcopy, so we don't need to deepcopy self.envA_ here
        opA_dagger = envA.inverseCircuit().convertToProcedure('opA_dagger', env)()
        opA = envA.convertToProcedure('opA', env)()
        
        # construct S0 and S_{psi0} operators
        opS0 = self.reflection_S0().convertToProcedure('opS0', env)()
        opS_psi0 = self.reflection_S_psi0().convertToProcedure('opS_psi0', env)()

        # assemble Q operator: Q = A S0 A^dagger S_{psi0}
        opS_psi0(*qreglist)
        opA_dagger(*qreglist)
        opS0(*qreglist)
        opA(*qreglist)

        self.envQ_ = env
