#!/usr/bin/env python
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
# Initially based on https://bit.ly/3L7HOQK
import os
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType

from setuptools import find_namespace_packages, setup

# https://packaging.python.org/guides/single-sourcing-package-version/
# http://blog.ionelmc.ro/2014/05/25/python-packaging/
_PATH_ROOT = os.path.dirname(__file__)
_PATH_REQUIRE = os.path.join(_PATH_ROOT, "requirements")


def _load_py_module(name: str) -> ModuleType:
    spec = spec_from_file_location(name, os.path.join(_PATH_ROOT, "src", "finetuning_scheduler", name))
    assert spec, f"Failed to load module {name}"
    py = module_from_spec(spec)
    assert spec.loader, f"ModuleSpec.loader is None for {name}"
    spec.loader.exec_module(py)
    return py


about = _load_py_module(name="__about__.py")
setup_tools = _load_py_module("setup_tools.py")

# https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras
# Define package extras. These are only installed if you specify them.
# From remote, use like `pip install finetuning_scheduler[dev, docs]`
# From local copy of repo, use like `pip install ".[dev, docs]"`
extras = {
    "examples": setup_tools._load_requirements(path_dir=_PATH_REQUIRE, file_name="examples.txt"),
    "extra": setup_tools._load_requirements(path_dir=_PATH_REQUIRE, file_name="extra.txt"),
    "test": setup_tools._load_requirements(path_dir=_PATH_REQUIRE, file_name="test.txt"),
    "ipynb": setup_tools._load_requirements(path_dir=_PATH_REQUIRE, file_name="ipynb.txt"),
    "cli": setup_tools._load_requirements(path_dir=_PATH_REQUIRE, file_name="cli.txt"),
}
for ex in ["extra", "examples"]:
    extras[ex].extend(extras["cli"])
extras["dev"] = extras["extra"] + extras["test"] + extras["ipynb"]
extras["all"] = extras["dev"] + extras["examples"]

# These packages shall be installed only on GPU machines
PACKAGES_GPU_ONLY = ["fairscale"]
# create a version for CPU machines
for ex in ("cpu", "cpu-extra"):
    kw = ex.split("-")[1] if "-" in ex else "all"
    # filter cpu only packages
    extras[ex] = [pkg for pkg in extras[kw] if not any(pgpu.lower() in pkg.lower() for pgpu in PACKAGES_GPU_ONLY)]

long_description = setup_tools._load_readme_description(
    _PATH_ROOT, homepage=about.__homepage__, version=about.__version__
)

# https://packaging.python.org/discussions/install-requires-vs-requirements /
# keep the meta-data here for simplicity in reading this file... it's not obvious
# what happens and to non-engineers they won't know to look in init ...
# the goal of the project is simplicity for researchers, don't want to add too much
# engineer specific practices
setup(
    name="finetuning-scheduler",
    version=about.__version__,
    description=about.__docs__,
    author=about.__author__,
    author_email=about.__author_email__,
    url=about.__homepage__,
    download_url="https://github.com/speediedan/finetuning-scheduler",
    license=about.__license__,
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "fts_examples.config": ["*.yaml"],
        "fts_examples.config.advanced.fsdp": ["*.yaml"],
        "fts_examples.config.advanced.reinit_lr": ["*.yaml"],
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    keywords=["deep learning", "pytorch", "AI", "machine learning", "pytorch lightning", "fine-tuning", "finetuning"],
    python_requires=">=3.7",
    setup_requires=[],
    install_requires=setup_tools._load_requirements(_PATH_REQUIRE),
    # install_requires=setup_tools._load_requirements(
    #     _PATH_REQUIRE, pl_commit="fc195b95405e9e2629466e5b28c6a9243209d596"
    # ),
    extras_require=extras,
    project_urls={
        "Bug Tracker": "https://github.com/speediedan/finetuning-scheduler/issues",
        "Documentation": "https://finetuning-scheduler.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/speediedan/finetuning-scheduler",
    },
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
