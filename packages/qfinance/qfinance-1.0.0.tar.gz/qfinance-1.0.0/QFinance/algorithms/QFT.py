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
This module defines a QFT class and implements the QFT algorithm.
"""

import numpy as np
from QCompute import *
from QFinance.utils import sub_qreg, full_qreg

class QFT:
    """
    Quantum Fourier Transform
    :param num_qubits: number of qubits to transform
    :inverse: if True, perform inverse QFT  
    :swap: if True, swap all qubits in the last step in QFT, or swap all qubits in the first step in IQFT
    
    1. instantiate a QFT class
    2. call qft.qft_env to get the QEnv
    3. call qft_env.convertToProcedure('QFT', env) to get the corresponding QProcedure

    example:
    >>> env = QEnv()
    >>> env.backend(BackendName.LocalBaiduSim2)
    >>> num_qubits = 5
    >>> shots = 1024
    >>> 
    >>> q = env.Q.createList(num_qubits)
    >>> qft_instance = QFT(num_qubits)
    >>> qft_env = qft_instance.qft_env
    >>> qft_procedure = qft_env.convertToProcedure('QFT', env)
    >>> qft_procedure()(*q)
    >>>
    >>> MeasureZ(*env.Q.toListPair())
    >>> taskResult = env.commit(shots, fetchMeasure=True)
    >>> print(taskResult['counts'])
    """

    def __init__(self, num_qubits:int, inverse:bool = False) -> None:
        self.env = QEnv()
        self.num_qubits = num_qubits
        self.inverse = inverse
        self.q = self.env.Q
        self.q.createList(self.num_qubits)
        self.swap = True
        #assert len(self.q.registerMap) == self.n, "number of qubits in env is not equal to num_qubits"
        # self.shots = 1024
        # self.qft = None

    def required_num_qubits(self) -> int:
        """
        :return: number of qubits required by the QFT algorithm
        """
        return self.num_qubits

    def swap_all(self, env:QEnv) -> QEnv:
        """
        Swap all qubits in the QRegPool in the following order:
        0 <-> n-1
        1 <-> n-2
        ...
        """
        q = env.Q
        num = len(q.registerMap)
        for i in range(num // 2):
            SWAP(q[i], q[num -i - 1])
        return env


    def qft_bare(self, n:int, env:QEnv = QEnv()) -> QEnv:
        """
        Quantum Fourier Transform, without swapping in the last step
        :param n: number of qubits to transform
        :return: QEnv
        use the recursion relation in QFT: QFT_{n} = QFT_{n-1} then apply sequential CU gates
        """

        q = env.Q

        if n <= 0:
            raise ValueError('number of qubits must be greater than 0')
        elif n == 1:
            H(q[0])
        else:
            env = self.qft_bare(n - 1, env)
            for i in range(n - 1):
                CU(0, 0, 2 * np.pi / 2 ** (n - i))(q[n - 1], q[i])
            H(q[n - 1])
        return env


    def iqft_bare(self, n:int, env:QEnv = QEnv()) -> QEnv:
        """
        Inverse Quantum Fourier Transform, without swapping in the first step
        :param n: number of qubits to transform
        :return: QEnv
        use the recursion relation in IQFT: IQFT_{n} = IQFT_{n-1} then apply sequential CU gates
        """
        q = env.Q

        if n <= 0:
            raise ValueError('number of qubits must be greater than 0')
        elif n == 1:
            H(q[0])
        else:
            H(q[n - 1])
            for i in range(n - 1):
                CU(0, 0, -2 * np.pi / 2 ** (n - i))(q[n - 1], q[i])
            env = self.iqft_bare(n - 1, env)
        return env


    @property
    def qft_env(self) -> QEnv:
        """
        Quantum Fourier Transform
        :return: QEnv
        """
        if self.inverse:
            self.swap_all(self.env)
            self.iqft_bare(self.num_qubits, self.env)
        else:
            self.qft_bare(self.num_qubits, self.env)
            self.swap_all(self.env)
        return self.env


    # @property
    # def qft_env(self) -> QEnv:
    #     """
    #     Construct a Quantum Fourier Transform circuit, with swapping in the last step
    #     :return: QEnv
    #     """
        
    #     QFTEnv = QEnv()

    #     QFTEnv = self.qft_bare(self.num_qubits, QFTEnv)
    #     QFTEnv = self.swap_all(QFTEnv)

    #     if not self.inverse:
    #         return QFTEnv

    #     # if self.inverse:
    #     #     QFTEnv.publish(applyModule = False)
    #     #     QFTEnv.program = InverseCircuitModule()(QFTEnv.program)

    #     # return the inverse env
    #     else:
    #         QFTEnv_copy = deepcopy(QFTEnv)
    #         QFTEnv_copy.circuit = []
    #         env_procedure = QFTEnv.convertToProcedure('QFT', QFTEnv_copy)
    #         env_procedure_inv, _ = QFTEnv_copy.inverseProcedure(env_procedure.name)
    #         env_procedure_inv()(*QFTEnv_copy.Q.registerMap.values())
    #         QFTEnv_copy.publish(False)
    #         return QFTEnv_copy

