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
This module defines the help function associated to QRegPool class.
"""

from QCompute.QPlatform.QRegPool import QRegPool


def sub_qreg(qreg:QRegPool, start:int, num:int):
    """
    For a given slice, return a list of QRegStorage with the qubits in the given slice
    qreg: the quantum register
    start: the start index of the slice
    num: the number of qubits in the slice
    """
    if start is None:
        start = 0
        
    dic = qreg.registerMap

    sublist = []
    for k, v in dic.items():
        if start <= k < start + num:
            sublist.append(v)
    return sublist


def sub_qreg_slice(qreg:QRegPool, start: int, end: int):
    """
    For a given slice start:end, return a list of QRegStorage with the qubits in the given slice
    qreg: the quantum register
    start: the start index of the slice
    end: the end index of the slice

    the start index is included, the end index is excluded
    """

    dic = qreg.registerMap

    sublist = []
    for k, v in dic.items():
        if start <= k < end:
            sublist.append(v)
    return sublist


def full_qreg(qreg:QRegPool):
    """
    For a give QRegPool, return a list of QRegStorage with all the qubits in the QRegPool
    """
    return list(qreg.registerMap.values())