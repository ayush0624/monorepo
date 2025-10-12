""" Common Definitions for Python """
load(
    "//bazel/python/pytest:defs.bzl",
    _pytest_test = "pytest_test"
)
load(
    "//bazel/python:alembic.bzl",
    _alembic = "alembic"
)

pytest_test = _pytest_test
alembic = _alembic
