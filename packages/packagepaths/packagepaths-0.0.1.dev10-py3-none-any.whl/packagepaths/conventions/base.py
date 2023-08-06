# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod
from pathlib import Path

from packagepaths.package import Package
from packagepaths.platforms.base import Platform


class Convention(ABC):
    @abstractmethod
    def get_package_cache_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_package_config_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_package_data_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_package_executable_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_package_library_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        raise NotImplementedError  # pragma: no cover
