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
This module is a demo to show how to use Option Pricing module.
"""


import numpy

import QCompute
QCompute.Define.Settings.outputInfo = False

from QFinance.pricing import EuropeanOptionPricingClassical, EuropeanCallQMC


def european_option_pricing():
    """
    Test the EuropeanOptionPricingClassical class.
    """
    s0 = 100
    k = 90
    t = 1
    r = 0.05
    sigma = 0.1

    option_classical = EuropeanOptionPricingClassical(s0, k, t, r, sigma, "call", "long")

    bsm_price = option_classical.bsm_price()

    option_classical.set_CMC_sample_size(1000000)
    cmc_price = option_classical.cmc_price()
    conf_rad = option_classical.confidence_radius

    option_classical.show_info()
    
    ########################################################################################

    option = EuropeanCallQMC(s0, k, t, r, sigma)
    option.set_num_qubits(3)
    option.set_scaling(0.04)
    
    # set MLAE configuration
    option.method = "MLAE"
    Q_powers = [2, 3, 5, 10]
    shots = [100000] * len(Q_powers)
    price_qmc, price_random_error_radius = option.get_price_and_error_mlae(Q_powers, shots)
    # price_qmc, price_error = option.get_price_and_error()

    print(f"BSM price: \t{bsm_price:.5f}")
    print(f"CMC price: \t{cmc_price:.5f}", u"\u00B1", f"{conf_rad:.5f}","(with confidence level 0.95)")
    print(f"QMC price: \t{price_qmc:.5f}", u"\u00B1", f"{price_random_error_radius:.5f}", "(with tail compensation)\n")

    debug = True
    # print debug info
    if debug:
        option.print_error_info()
        # grid_price = numpy.exp(-r * t) * option.calc_grid_expectation()
        # price_overall_error = abs(bsm_price - price_qmc) / bsm_price
        # price_random_error = abs(grid_price - price_qmc) / grid_price
        # print(f"Random error of option price: \t{price_random_error * 100:.3f}%")
        # print(f"Overall error of option price: \t{price_overall_error * 100:.3f}%\n")
        

if __name__ == "__main__":
    european_option_pricing()