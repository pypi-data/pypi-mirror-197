# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

"""
Resolver: Use a package, platform, and convention to resolve paths.

This module provides the `Resolver` class, which is used to resolve the paths for a package on a platform using a
specific convention.

By allowing package, platform, and convention classes to be loosely coupled we can leverage a resolver to tie everything
together and handle all of the logic for resolving and finalizing paths.
"""

from pathlib import Path

from packagepaths.conventions.base import Convention
from packagepaths.package import Package
from packagepaths.platforms.base import Platform


class Resolver:
    def __init__(
        self,
        package: Package,
        platform: Platform,
        convention: Convention,
        /,
    ):
        self.package = package
        self.platform = platform
        self.convention = convention

    def environment_for_key(self, key: str) -> str:
        """
        Assemble the environment_key for the given path type.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.environment_for_key("bin")
        'PATH_PACKAGE_BIN'

        >>> resolver.environment_for_key("lib")
        'PATH_PACKAGE_LIB'

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.environment_for_key("bin")
        'PATH_PROVIDER_PROJECT_PACKAGE_0_00_BIN'

        Returns:
            str: The environment key for the given path type.
        """
        return f"PATH_{self.package.environment}_{key.upper()}"

    @property
    def cache_path(self) -> Path:
        """
        Resolve the path to the cache directory for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import HybridOptionalConvention, OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.cache_path
        PosixPath('/opt/package/cache')

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.cache_path
        PosixPath('/opt/provider/project/package/0.00/cache')

        >>> convention = HybridOptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.cache_path
        PosixPath('/var/opt/provider/project/package/0.00/cache')

        Returns:
            Path: The path to the cache directory for this package.
        """
        return self.convention.get_package_cache_path_for_platform(self.package, self.platform)

    @property
    def config_path(self) -> Path:
        """
        Resolve the path to the configuration directory for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import HybridOptionalConvention, OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.config_path
        PosixPath('/opt/package/etc')

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.config_path
        PosixPath('/opt/provider/project/package/0.00/etc')

        >>> convention = HybridOptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.config_path
        PosixPath('/etc/opt/provider/project/package/0.00')

        Returns:
            Path: The path to the configuration directory for this package.
        """
        return self.convention.get_package_config_path_for_platform(self.package, self.platform)

    @property
    def data_path(self) -> Path:
        """
        Resolve the path to the data directory for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.data_path
        PosixPath('/opt/package/share')

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.data_path
        PosixPath('/opt/provider/project/package/0.00/share')

        Returns:
            Path: The path to the data directory for this package.
        """
        return self.convention.get_package_data_path_for_platform(self.package, self.platform)

    @property
    def executable_path(self) -> Path:
        """
        Resolve the path to the executable for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.executable_path
        PosixPath('/opt/package/bin')

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.executable_path
        PosixPath('/opt/provider/project/package/0.00/bin')

        Returns:
            Path: The path to the executable for this package.
        """
        return self.convention.get_package_executable_path_for_platform(self.package, self.platform)

    @property
    def library_path(self) -> Path:
        """
        Resolve the path to the library for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.library_path
        PosixPath('/opt/package/lib')

        >>> package = Package("package", provider="provider", project="project", version="0.00")

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.library_path
        PosixPath('/opt/provider/project/package/0.00/lib')

        Returns:
            Path: The path to the library for this package.
        """
        return self.convention.get_package_library_path_for_platform(self.package, self.platform)

    @property
    def paths(self) -> dict[str, Path]:
        """
        Assemble the paths dictionary for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.paths
        {'cache': PosixPath('/opt/package/cache'), ..., 'library': PosixPath('/opt/package/lib')}

        Returns:
            dict[str, Path]: The paths dictionary for this package.
        """

        return {
            "cache": self.cache_path,
            "config": self.config_path,
            "data": self.data_path,
            "executable": self.executable_path,
            "library": self.library_path,
        }

    @property
    def environment(self) -> dict[str, str]:
        """
        Assemble the environment dictionary for this package.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform
        >>> from packagepaths.conventions.optional import OptionalConvention

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> resolver = Resolver(package, platform, convention)
        >>> resolver.environment
        {'PATH_PACKAGE_CACHE': '/opt/package/cache', ..., 'PATH_PACKAGE_LIBRARY': '/opt/package/lib'}

        Returns:
            dict[str, Path]: _description_
        """
        return {
            self.environment_for_key("cache"): str(self.cache_path),
            self.environment_for_key("config"): str(self.config_path),
            self.environment_for_key("data"): str(self.data_path),
            self.environment_for_key("executable"): str(self.executable_path),
            self.environment_for_key("library"): str(self.library_path),
        }
