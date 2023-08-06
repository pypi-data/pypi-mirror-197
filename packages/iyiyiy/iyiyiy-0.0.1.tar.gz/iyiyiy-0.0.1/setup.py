from setuptools import setup
import os
def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )
def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


setup(name="iyiyiy",
version="0.0.1",
url="http://github.com/iyyoo9806/iyiyiy",
license="MIT",
author="Yooinyoung",
author_email="iyyoo980615@naver.com",
keywords=["calendar","isoweek","listsum"],
description="Min",
packages=find_packages("."),
install_requires=["isoweek"])