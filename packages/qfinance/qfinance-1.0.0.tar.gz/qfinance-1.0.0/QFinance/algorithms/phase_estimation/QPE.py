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


import pprint
import numpy as np
import sys

from traitlets import List


from QCompute import *

from QCompute.QPlatform.QRegPool import QRegPool, QRegStorage
from QCompute.QPlatform.QOperation.QProcedure import QProcedure, QProcedureOP

from QFinance.algorithms.QFT import QFT


def subQreg(q:QRegPool, start:int, num:int):
    """
    Return a list of QRegStorage with the qubits in the given slice
    """
    if start is None:
        start = 0
    dic = q.registerMap

    return [v for k, v in dic.items() if start <= k < start + num]


# TODO need eigenstate of the oracle operator

class QPE:
    """
    num_qubits: number of qubits that U acts on
    num_ancillas: number of ancilla qubits, on which the final inverse QFT is applied
    ctrlU: the controlled unitary operator
    oracle: the black box composed of sequential ctrl-U^{2^k} gates
    the eigenvalue of U is e^{2*pi*i*phase}
    """

    def __init__(self, num_qubits:int, num_ancillas:int, ctrlU_env:QEnv):
        self.num_qubits = num_qubits
        self.num_ancillas = num_ancillas
        self.num_total = num_qubits + num_ancillas
        self.ctrlU_env = ctrlU_env
        # self.oracle = oracle
        self.env = QEnv()
        self.q = self.env.Q
        self.q.createList(self.num_total)
        self.ancilla_qubits = subQreg(self.q, 0, self.num_ancillas)
        self.operating_qubits = subQreg(self.q, self.num_ancillas, self.num_qubits)
        self.total_qubits = subQreg(self.q, 0, self.num_total)
        self.eigenstate:QEnv = None
        #self.oracle = self.get_oracle(ctrlU)
        self.oracle:QProcedureOP = None
        self.oracle_constructed = False
        self.oracle_applied = False
        self.estimated_phase = 0
        self.estimated_eigenvalue = 1
        self.shots = 1024
        
    # def __call__(self, env:QEnv) -> QProcedure:
    #     return qpe(env, self.num_qubits, self.num_ancillas, self.oracle)


    def select_backend(self, backendName:str):
        """
        select backend
        :param backendName: backend name
        """
        self.env.backend(backendName)


    def apply_oracle(self):
        """
        apply the oracle
        ctrlU: the controlled unitary operator
        return: oracle
        """

        # convert QEnv ctrlU to an QProcedureOP on the current environment
        self.ctrlU = self.ctrlU_env.convertToProcedure('ctrlU', self.env)()

        for i in range(self.num_ancillas):
            # ctrl-U^{2^(n-i-1)}
            for _ in range(2 ** (self.num_ancillas - i - 1)):
                self.ctrlU(self.q[i], *self.operating_qubits)

        self.oracle_applied = True     


    # deprecated, use self.apply_oracle instead
    def get_oracle(self):
        """
        get the oracle
        ctrlU: the controlled unitary operator
        return: oracle
        """
        oracle_env = QEnv()
        oq = oracle_env.Q
        oq.createList(self.num_total)

        # convert QEnv ctrlU to an QProcedureOP on the current environment
        self.ctrlU = self.ctrlU_env.convertToProcedure('ctrlU', oracle_env)()

        oq_operating_qubits = subQreg(oq, self.num_ancillas, self.num_qubits)
        for i in range(self.num_ancillas):
            # ctrl-U^{2^(n-i-1)}
            for _ in range(2 ** (self.num_ancillas - i - 1)):
                self.ctrlU(oq[i], *oq_operating_qubits)
                # phi = 2 * np.pi / 2
                # CU(0, 0, phi)(oq[i], *oq_operating_qubits)

        self.oracle = oracle_env.convertToProcedure('oracle', self.env)()
        self.oracle_constructed = True


    def prepare_state(self, eigenstate:np.ndarray):
        """
        prepare the eigenstate of the oracle operator
        :param eigenstate: eigenstate of the oracle operator
        """
        assert len(eigenstate) == 2 ** self.num_qubits, "length of eigenstate is not equal to 2 ** num_qubits"
        assert np.linalg.norm(eigenstate) == 1, "eigenstate is not normalized"
        assert np.linalg.norm(eigenstate - np.conj(eigenstate)) == 0, "eigenstate is not a pure state"
        # TODO get eigenstate QProcedure from the matrix

    
    def get_state(self, eigenstate:QEnv):
        self.eigenstate = eigenstate.convertToProcedure('eigenstate', self.env)()
        self.eigenstate(*self.operating_qubits)
    
    # TODO: add implementations of some common eigenstates that are easily realized in QCompute


    def estimate_phase(self) -> None:
        """
        Quantum Phase Estimation
        :return: the estimated phase
        """

        if not self.env.backendName:
            raise RuntimeError("backend not selected")

        if not self.eigenstate:
            raise RuntimeError("eigenstate not prepared")

        # Apply Hadamard gates to the ancilla qubits
        for i in range(self.num_ancillas):
            H(self.q[i])
        


        # Apply the oracle
        # if not self.oracle_constructed:
        #     self.get_oracle()
        # self.oracle(*self.total_qubits)

        # Apply the oracle
        if not self.oracle_applied:
            self.apply_oracle()


        # Apply inverse QFT
        iqft = QFT(self.num_ancillas, True)
        iqft_subroutine =  iqft.qft_env.convertToProcedure('iqft', self.env)()
        iqft_subroutine(*self.ancilla_qubits)

        # Measure the ancilla qubits
        MeasureZ(subQreg(self.q, 0, self.num_ancillas), range(self.num_ancillas))

        task_result = self.env.commit(self.shots, fetchMeasure=True)
        counts_dict = task_result['counts']
        self.estimated_phase = self.get_phase_by_mean(counts_dict)
        # self.estimated_phase = self.get_phase_by_max(counts_dict)
        self.estimated_eigenvalue = np.exp(2 * np.pi * 1j * self.estimated_phase)
        #return self.estimated_phase


    def get_phase_by_max(self, counts_dict:dict) -> float:
        """
        get the estimated phase, use the result with maximum likelihood in the measurement
        :param counts_dict: counts dictionary, looks like {'000': 512, '001': 512}
        QCompute uses big-endian, so the order is like '(n-1),(n-2),...,0'
        :return: estimated phase
        """
        def parse_bits_string(bits_string:str) -> int:
            """
            parse the bits string to integer
            :param bits_string: bits string, like '110'
            :return: integer, like 0
            QCompute uses big-endian
            """
            reversed_bits_string = bits_string[::-1]
            return int(reversed_bits_string, 2)

        phase = 0
        kmax = None
        vmax = 0
        for k, v in counts_dict.items():
            if v > vmax:
                kmax = k
                vmax = v
        
        if kmax is not None:
            phase = parse_bits_string(kmax) / 2 ** self.num_ancillas
        return phase


    def get_phase_by_mean(self, counts_dict:dict) -> float:
        """
        get the estimated phase, use the average result in the measurement with corresponding weight
        :param counts_dict: counts dictionary, looks like {'000': 512, '001': 512}
        QCompute uses big-endian, so the order is like '(n-1),(n-2),...,0'
        :return: estimated phase
        """
        def parse_bits_string(bits_string:str) -> int:
            """
            parse the bits string to integer
            :param bits_string: bits string, like '110'
            :return: integer, like 0
            QCompute uses big-endian
            """
            reversed_bits_string = bits_string[::-1]
            return int(reversed_bits_string, 2)
        
        phase = 0
        v_total = 0

        for k, v in counts_dict.items():
            v_total += v
        
        for k, v in counts_dict.items():
            phase += parse_bits_string(k) * v / v_total

        phase /= 2 ** self.num_ancillas

        return phase