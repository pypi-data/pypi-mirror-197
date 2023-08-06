# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path
from typing import Optional


class Package:
    def __init__(
        self,
        name: str,
        /,
        provider: Optional[str] = None,
        project: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.name = name
        self.provider = provider
        self.project = project
        self.version = version

    @property
    def path(self) -> Path:
        path = Path()
        if self.provider:
            path = path / self.provider
        if self.project:
            path = path / self.project
        path = path / self.name
        if self.version:
            path = path / self.version
        return path  # noqa: R504

    @property
    def environment(self) -> str:
        return "_".join(self.path.parts).replace(".", "_").upper()
