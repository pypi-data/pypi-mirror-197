"""QuBOX UFSC Client

QuBOX is a portable quantum computing simulator developed by Quantuloop
for the Ket language. Accelerated by GPU, QuBOX has two simulation modes, 
being able to simulate more than 30 quantum bits.

In partnership with Quantuloop, the Quantum Computing Group - UFSC provides
free remote access to a QuBOX simulator. You can use this client to access 
the QuBOX hosted at the Federal University of Santa Catarina (UFSC). 
"""
from __future__ import annotations
# Copyright 2023 Quantuloop
# All rights reserved
from ctypes import c_uint8
from typing import Literal
import random
import requests
from ket.clib import libket
from ket.base import set_quantum_execution_target, set_process_features


QUBOX_URL = "https://qubox.ufsc.br"

MODE = 'sparse'
PRECISION = 1
TOKEN = ""
RNG = random.Random()
TIMEOUT = 0

__all__ = ["login", "config"]


def login(*, name, email, affiliation):
    """Register with QuBOX UFSC to gain access.

    Your information may be used anonymously for statistics.
    """

    global TOKEN

    TOKEN = requests.get(
        QUBOX_URL+'/login',
        params={
            'name': name,
            'email': email,
            'affiliation': affiliation
        },
        timeout=30
    ).content


def config(*,
           mode: Literal["sparse", "dense"] | None = None,
           precision: Literal[1, 2] | None = None,
           seed: any | None = None,
           timeout: int | None = None,
           ):
    """Set QuBOX UFSC as the quantum execution target.

    You must first register with :func:`qubox_ufsc_client.login`.
    Otherwise, the quantum execution will fail.

    Args:
        mode: Set simulation mode. Available modes are "sparse" and "dense".
        precision: Set the floating point precision to "sparse" mode.
                   Acceptable values are "1" for single precision and 
                   "2" for double precision. Dense mode uses single precision.
        seed: Initialize the simulator RNG.
        timeout: Quantum execution timeout in seconds, Set 0 to disable timeout.
    """

    if mode is not None:
        if mode not in ["sparse", "dense"]:
            raise ValueError('parameter "mode" must be "sparse" or "dense"')
        global MODE
        MODE = mode

    if precision is not None:
        if int(precision) not in [1, 2]:
            raise ValueError('parameter "precision" must be int(0) or int(1)')
        global PRECISION
        PRECISION = precision

    if seed is not None:
        global RNG
        RNG = random.Random(seed)

    if timeout is not None:
        if timeout < 0:
            raise ValueError('parameter "timeout" must >= 0')
        global TIMEOUT
        TIMEOUT = int(timeout)

    set_quantum_execution_target(_send_quantum_code)
    set_process_features(plugins=['pown'])


def _send_quantum_code(process: libket.Process):
    process.serialize_quantum_code(libket.JSON)
    process.serialize_metrics(libket.JSON)

    code_data, code_size, _ = process.get_serialized_quantum_code()
    code = bytearray(code_data[:code_size.value])

    metrics_data, metrics_size, _ = process.get_serialized_metrics()
    metrics = bytearray(metrics_data[:metrics_size.value])

    result = requests.get(
        QUBOX_URL+'/run',
        params={
            'mode': MODE,
            'precision': PRECISION,
            'seed': RNG.getrandbits(64),
            'timeout': TIMEOUT
        },
        files={
            'token': ('token.jwt', TOKEN, 'text/plain'),
            'quantum_code': ('quantum_code.json', code, 'text/plain'),
            'quantum_metrics': ('quantum_metrics.json', metrics, 'text/plain')
        },
        timeout=None if TIMEOUT == 0 else TIMEOUT
    ).content

    result_size = len(result)

    process.set_serialized_result(
        (c_uint8*result_size)(*result),
        result_size,
        libket.JSON
    )
