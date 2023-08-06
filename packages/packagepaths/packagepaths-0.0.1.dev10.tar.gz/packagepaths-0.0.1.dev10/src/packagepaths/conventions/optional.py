# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

"""
Optional Convention: A convention that focuses on `/opt` like paths.
"""

from pathlib import Path

from packagepaths.conventions.base import Convention
from packagepaths.package import Package
from packagepaths.platforms.base import Platform


class OptionalConvention(Convention):
    """
    The optional convention is a convention that is not required to be implemented by all platforms and is primarily
    supported on top of POSIX style systems.
    """

    def get_package_cache_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the path to the cache directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> convention.get_package_cache_path_for_platform(package, platform)
        PosixPath('/opt/package/cache')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the cache directory for the package and platform.
        """
        return platform.base_path / platform.optional_path / package.path / platform.cache_path

    def get_package_config_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the path to the configuration directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> convention.get_package_config_path_for_platform(package, platform)
        PosixPath('/opt/package/etc')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the configuration directory for the package and platform.
        """
        return platform.base_path / platform.optional_path / package.path / platform.config_path

    def get_package_data_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the path to the data directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> convention.get_package_data_path_for_platform(package, platform)
        PosixPath('/opt/package/share')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the data directory for the package and platform.
        """
        return platform.base_path / platform.optional_path / package.path / platform.data_path

    def get_package_executable_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the path to the executable directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> convention.get_package_executable_path_for_platform(package, platform)
        PosixPath('/opt/package/bin')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the executable directory for the package and platform.
        """
        return platform.base_path / platform.optional_path / package.path / platform.executable_path

    def get_package_library_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the path to the library directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = OptionalConvention()

        >>> convention.get_package_library_path_for_platform(package, platform)
        PosixPath('/opt/package/lib')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the library directory for the package and platform.
        """
        return platform.base_path / platform.optional_path / package.path / platform.library_path


class HybridOptionalConvention(OptionalConvention):
    """
    The hybrid optional convention is a convention that is not required to be implemented by all platforms and is
    primarily supported on top of POSIX style systems.

    The hybrid optional convention is a hybrid of the optional convention and the state convention where paths like
    `/etc/opt` and `/var/opt` are used instead of `/opt`.  Sometimes there is special handling depending on the sort of
    path being assembled.
    """

    def get_package_cache_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the hybrid path to the cache directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = HybridOptionalConvention()

        >>> convention.get_package_cache_path_for_platform(package, platform)
        PosixPath('/var/opt/package/cache')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the cache directory for the package and platform.
        """
        return platform.base_path / platform.state_path / platform.optional_path / package.path / platform.cache_path

    def get_package_config_path_for_platform(self, package: Package, platform: Platform, /) -> Path:
        """
        Assemble the hybrid path to the configuration directory for a package and platform.

        >>> from packagepaths.package import Package
        >>> from packagepaths.platforms.linux import LinuxPlatform

        >>> package = Package("package")
        >>> platform = LinuxPlatform()
        >>> convention = HybridOptionalConvention()

        >>> convention.get_package_config_path_for_platform(package, platform)
        PosixPath('/etc/opt/package')

        Args:
            package (Package): The package to assemble the path for.
            platform (Platform): The platform to assemble the path for.

        Returns:
            Path: The assembled path to the configuration directory for the package and platform.
        """
        return platform.base_path / platform.config_path / platform.optional_path / package.path
