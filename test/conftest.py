# -*- coding: utf-8 -*-
import os

import pytest

import brewtils.test

pytest_plugins = ["brewtils.test.fixtures"]


def pytest_configure():
    setattr(brewtils.test, "_running_tests", True)


def pytest_unconfigure():
    delattr(brewtils.test, "_running_tests")


@pytest.fixture(autouse=True)
def environ():
    """Make sure tests don't clobber the environment"""
    safe_copy = os.environ.copy()
    yield
    os.environ = safe_copy


@pytest.fixture(autouse=True)
def global_config():
    """Make sure that the global CONFIG is reset after every test"""
    yield
    brewtils.plugin.CONFIG = None
