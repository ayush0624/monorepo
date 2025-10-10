""" Definitions relating to pytest """
load("@rules_python//python:defs.bzl", "py_test")
load("@pypi//:requirements.bzl", "requirement")

def pytest_test(name, srcs, deps = [], args = [], **kwargs):
    """
        Call pytest
    """
    if requirement("pytest") not in deps:
        deps.append(requirement("pytest"))

    py_test(
        name = name,
        srcs = [
            "//bazel/python/pytest:wrapper.py",
        ] + srcs,
        main = "//bazel/python/pytest:wrapper.py",
        args = args + ["$(location :%s)" % x for x in srcs],
        python_version = "PY3",
        srcs_version = "PY3",
        deps = deps,
        **kwargs
    )
