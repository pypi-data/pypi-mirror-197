# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from abc import ABC
from pathlib import Path


class Platform(ABC):
    base_path: Path
    cache_path: Path
    config_path: Path
    data_path: Path
    executable_path: Path
    library_path: Path
    optional_path: Path
    state_path: Path
