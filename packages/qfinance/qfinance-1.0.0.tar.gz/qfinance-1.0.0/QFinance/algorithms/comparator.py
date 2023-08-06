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
This module implements the quantum comparator.
Reference: 
http://arxiv.org/abs/1905.02666
http://arxiv.org/abs/quant-ph/0410184
"""

from copy import deepcopy

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegStorage
from QFinance.utils import sub_qreg, full_qreg, sub_qreg_slice, extract_to_int_by_max


class QuantumComparator:
    """
    The quantum comparator class, used to compare a n-qubit register with a fixed value K.
    The result is stored in an ancillary qubit.

    register memory layout:
    n = num_working_qubits = num_ancillary_qubits
    0 ~ n - 1: working qubits
    n ~ 2n - 1: ancillary qubits
    2n: result qubit

    in the working register |i>_n, 
    i0 is the least significant bit, and i_{n-1} is the most significant bit.
    """

    def __init__(self, env: QEnv, num_qubits: int, value: int):
        """
        Initialize the class.

        env: The QEnv object, contains the state |psi>
        num_qubits: number of qubits in the state |psi>
        value: The fixed value to compare with.
        """
        self.state_env = env
        self.num_working_qubits = num_qubits
        self.value = value

        self.init_check()

        self.num_ancillary_qubits = self.num_working_qubits
        self.num_result_qubits = 1
        self.num_total_qubits = self.num_working_qubits + self.num_ancillary_qubits + self.num_result_qubits
        
        self.env = QEnv()
        self.q = self.env.Q
        self.q.createList(self.num_total_qubits)

        # register memory layout
        # n = num_working_qubits = num_ancillary_qubits
        # 0 ~ n - 1: working qubits
        # n ~ 2n - 1: ancillary qubits
        # 2n: result qubit
        self.working_qreg = sub_qreg(self.q, 0, self.num_working_qubits)
        self.ancillary_qreg = sub_qreg(self.q, self.num_working_qubits, self.num_ancillary_qubits)
        self.result_qreg = sub_qreg(self.q, self.num_working_qubits + self.num_ancillary_qubits, self.num_result_qubits)

        self.load_initial_state()


    def init_check(self) -> None:
        """
        Check that the value is a nonnegative inteter, and it's in the correct range [0, 2^n - 1].
        Check that the env contains the correct number of qubits.
        """
        if len(self.state_env.Q.registerMap) != self.num_working_qubits:
            raise ValueError("The number of qubits in the env is not correct.")

        if not isinstance(self.value, int):
            raise ValueError("The classical value to compare with must be an integer.")
        
        if self.value < 0:
            raise ValueError("The classical value to compare with must be a nonnegative integer.")
        
        if self.value >= 2 ** self.num_working_qubits:
            raise ValueError("The classical value to compare with is out of range.")
    

    def load_initial_state(self) -> None:
        """
        Load the initial state |psi> into the working qubits.
        |psi> is stored in self.state_env.
        """
        op_Psi = self.state_env.convertToProcedure("psi", self.env)()
        op_Psi(*self.working_qreg)


    def twos_complement(self) -> list:
        """
        calculate the classical array that holds the two's complement of the value.
        return a list t of 0s and 1s in the little-endian order.
        """
        t = [0] * self.num_working_qubits

        # the binary_max is equivalent to -1 in the signed representation
        binary_max = 2 ** self.num_working_qubits - 1
        bitstring = bin(-self.value & binary_max)[2:]

        # reverse the bitstring and convert it to a list of 0s and 1s
        # then pad the list with 0s to the correct length
        t = [int(x) for x in bitstring[::-1]]
        t = t + [0] * (self.num_working_qubits - len(t))
        return t


    def logical_OR(self, a: QRegStorage, b: QRegStorage, c: QRegStorage) -> None:
        """
        apply the logical OR gate to the qubits a, b, c.
        """
        X(a)
        X(b)
        X(c)
        CCX(a, b, c)
        X(a)
        X(b)


    def build(self) -> None:
        """
        Build the circuit.
        The two's complement array t holds the bits of -value, in the little-endian order.
        if t[k] = 0, then apply the logical OR gate,
        if t[k] = 1, then apply the CCX gate.
        """
        # deal with the special case where self.value = 0
        # in this case, just flip the result qubit
        if self.value == 0:
            X(self.result_qreg[0])
            return

        t = self.twos_complement()

        # if t[0] = 0 then do nothing
        # if t[0] = 1 then corresponds to a CX gate
        if t[0] == 1:
            CX(self.working_qreg[0], self.ancillary_qreg[0])

        # for the rest of the bits
        # if t[k] = 0 then apply a logical OR gate
        # if t[k] = 1 then apply a CCX gate
        for k in range(1, self.num_working_qubits):
            if t[k] == 1:
                self.logical_OR(self.working_qreg[k], self.ancillary_qreg[k - 1], self.ancillary_qreg[k])
            else:
                CCX(self.working_qreg[k], self.ancillary_qreg[k - 1], self.ancillary_qreg[k])
        
        # the result is stored in the last ancillary qubit
        # if the result is 1, then the register binary is >= self.value
        # apply a CX gate to read the result from ancillary_qreg[-1] to result_qreg[0]
        CX(self.ancillary_qreg[-1], self.result_qreg[0])

        # reset the ancilla qubits by reverting the above operations
        for k in range(self.num_working_qubits - 1, 1, -1):
            if t[k] == 1:
                self.logical_OR(self.working_qreg[k], self.ancillary_qreg[k - 1], self.ancillary_qreg[k])
            else:
                CCX(self.working_qreg[k], self.ancillary_qreg[k - 1], self.ancillary_qreg[k])
        
        if t[0] == 1:
            CX(self.working_qreg[0], self.ancillary_qreg[0])

    
    def measure(self) -> int:
        """
        Measure the result qubit.
        Return 1 if the register binary is >= self.value, otherwise return 0.
        """
        shots = 1000
        self.env.backend(BackendName.LocalBaiduSim2)
        MeasureZ(self.result_qreg, [0])
        task_result = self.env.commit(shots)
        counts_dict = task_result['counts']
        return extract_to_int_by_max(counts_dict)
    


class QuantumComparatorOP:
    """
    The quantum comparator operator class, used to compare a n-qubit register with a fixed value K.
    The result is stored in an ancillary qubit.

    register memory layout:
    n = num_working_qubits = num_ancillary_qubits
    0 ~ n - 1: working qubits
    n ~ 2n - 1: ancillary qubits
    2n: result qubit
    """

    def __init__(self, num_qubits: int, value: int):
        """
        Initialize the class.

        env: The QEnv object, contains the state |psi>
        num_qubits: number of qubits in the state |psi>
        value: The fixed integer value to compare with.
        """
        # self.state_env = env
        self.num_working_qubits = num_qubits
        self.value = value

        self.init_check()

        self.num_ancillary_qubits = self.num_working_qubits
        self.num_result_qubits = 1
        self.num_total_qubits = self.num_working_qubits + self.num_ancillary_qubits + self.num_result_qubits
        
        self.working_qregL = None
        self.ancillary_qregL = None
        self.result_qreg = None

        # self.env = QEnv()
        # self.q = self.env.Q
        # self.q.createList(self.num_total_qubits)

        # register memory layout
        # n = num_working_qubits = num_ancillary_qubits
        # 0 ~ n - 1: working qubits
        # n ~ 2n - 1: ancillary qubits
        # 2n: result qubit

    def init_check(self) -> None:
        """
        Check that the value is a nonnegative inteter, and it's in the correct range [0, 2^n - 1].
        Check that the env contains the correct number of qubits.
        """
        if not isinstance(self.value, int):
            raise ValueError("The classical value to compare with must be an integer.")
        
        if self.value < 0:
            raise ValueError("The classical value to compare with must be a nonnegative integer.")
        
        if self.value >= 2 ** self.num_working_qubits:
            raise ValueError("The classical value to compare with is out of range.")


    def twos_complement(self) -> list:
        """
        calculate the classical array that holds the two's complement of the value.
        return a list t of 0s and 1s in the little-endian order.
        """
        t = [0] * self.num_working_qubits

        # the binary_max is equivalent to -1 in the signed representation
        binary_max = 2 ** self.num_working_qubits - 1
        bitstring = bin(-self.value & binary_max)[2:]

        # reverse the bitstring and convert it to a list of 0s and 1s
        # then pad the list with 0s to the correct length
        t = [int(x) for x in bitstring[::-1]]
        t = t + [0] * (self.num_working_qubits - len(t))
        return t


    def logical_OR(self, a: QRegStorage, b: QRegStorage, c: QRegStorage) -> None:
        """
        apply the logical OR gate to the qubits a, b, c.
        """
        X(a)
        X(b)
        X(c)
        CCX(a, b, c)
        X(a)
        X(b)


    def __call__(self, 
                 working_qregL: list[QRegStorage], 
                 ancillary_qregL: list[QRegStorage], 
                 result_qreg: QRegStorage,
                 big_endian: bool = True) -> None:
        """
        Build the circuit and act on the state |psi> to compare the register with the fixed value.
        The two's complement array t holds the bits of -value, in the little-endian order.
        if t[k] = 0, then apply the logical OR gate,
        if t[k] = 1, then apply the CCX gate.

        use little-endian by default: in the working register |i>_n, 
        i0 is the least significant bit, and i_{n-1} is the most significant bit.

        if big_endial = True, then use big-endian: in the working register |i>_n,
        i0 is the most significant bit, and i_{n-1} is the least significant bit.
        """
        self.working_qregL = working_qregL
        self.ancillary_qregL = ancillary_qregL
        self.result_qreg = result_qreg

        if big_endian:
            self.working_qregL = self.working_qregL[::-1]

        # deal with the special case where self.value = 0
        # in this case, just flip the result qubit
        if self.value == 0:
            X(self.result_qreg)
            return

        t = self.twos_complement()

        # if t[0] = 0 then do nothing
        # if t[0] = 1 then corresponds to a CX gate
        if t[0] == 1:
            CX(self.working_qregL[0], self.ancillary_qregL[0])

        # for the rest of the bits
        # if t[k] = 0 then apply a logical OR gate
        # if t[k] = 1 then apply a CCX gate
        for k in range(1, self.num_working_qubits):
            if t[k] == 1:
                self.logical_OR(self.working_qregL[k], self.ancillary_qregL[k - 1], self.ancillary_qregL[k])
            else:
                CCX(self.working_qregL[k], self.ancillary_qregL[k - 1], self.ancillary_qregL[k])
        
        # the result is stored in the last ancillary qubit
        # if the result is 1, then the register binary is >= self.value
        # apply a CX gate to read the result from ancillary_qreg[-1] to result_qreg[0]
        CX(self.ancillary_qregL[-1], self.result_qreg)

        # reset the ancilla qubits by reverting the above operations
        for k in range(self.num_working_qubits - 1, 1, -1):
            if t[k] == 1:
                self.logical_OR(self.working_qregL[k], self.ancillary_qregL[k - 1], self.ancillary_qregL[k])
            else:
                CCX(self.working_qregL[k], self.ancillary_qregL[k - 1], self.ancillary_qregL[k])
        
        if t[0] == 1:
            CX(self.working_qregL[0], self.ancillary_qregL[0])

    
    def measure(self) -> int:
        """
        Measure the result qubit.
        Return 1 if the register binary is >= self.value, otherwise return 0.
        """
        shots = 1000
        # point to the env created outside the class
        env = self.result_qreg.env
        env.backend(BackendName.LocalBaiduSim2)
        MeasureZ([self.result_qreg], [0])
        task_result = env.commit(shots)
        counts_dict = task_result['counts']
        return extract_to_int_by_max(counts_dict)
 