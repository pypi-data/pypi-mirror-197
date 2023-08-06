# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import PosixPath
from typing import Optional

from packagepaths.platforms.base import Platform


class LinuxPlatform(Platform):
    """
    Linux platform implementation contains all of the platform specific path information typically related to Linux
    based distributions.
    """

    base_path = PosixPath("/")
    cache_path = PosixPath("cache")
    config_path = PosixPath("etc")
    data_path = PosixPath("share")
    executable_path = PosixPath("bin")
    library_path = PosixPath("lib")
    optional_path = PosixPath("opt")
    state_path = PosixPath("var")

    def __init__(self, /, base: Optional[str] = None) -> None:
        """
        Initialize the Linux platform and ensure paths are PosixPath objects.

        >>> platform = LinuxPlatform()
        >>> platform.base_path
        PosixPath('/')
        >>> platform.cache_path
        PosixPath('cache')

        >>> platform = LinuxPlatform(base="/alternative")
        >>> platform.base_path
        PosixPath('/alternative')

        Args:
            base (Optional[str], optional): Override the base to use. Defaults to None.
        """
        if base is not None:
            self.base_path = PosixPath(base)
