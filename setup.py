#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from setuptools import find_packages, setup

# CPU-only package: the C++/CUDA extension (adet._C) is no longer built.
# The only op that used it at inference, MSDeformAttn, already goes through
# the pure-PyTorch fallback (multi_scale_deformable_attn_pytorch), and
# adet/layers/ms_deform_attn.py tolerates the missing module. This also
# frees setup.py from importing torch, so the sdist installs with regular
# build isolation.
#
# Version is static semver (see RELEASING.md) — it used to be derived from
# the torch version found at build time (0.2.113 = torch 1.13).

setup(
    name="AdelaiDet",
    version="0.3.0",
    author="Adelaide Intelligent Machines",
    url="https://github.com/stanstarks/AdelaiDet",
    description="AdelaiDet is AIM's research "
    "platform for instance-level detection tasks based on Detectron2.",
    packages=find_packages(exclude=("configs", "tests")),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "termcolor>=1.1",
        "Pillow>=6.0",
        "yacs>=0.1.6",
        "tabulate",
        "cloudpickle",
        "matplotlib",
        "tqdm>4.29.0",
        "tensorboard",
        "rapidfuzz",
        "Polygon3",
        "shapely",
        "scikit-image",
        "editdistance",
        # opencv: not pinned here so consumers choose the variant
        # (opencv-python-headless server-side); cv2 is still imported by
        # adet.modeling. numba: only used by adet.evaluation
        # (lexicon_procesor), never imported at inference — install it
        # yourself if you run evaluation.
        "timm",
    ],
    extras_require={"all": ["psutil"]},
)
