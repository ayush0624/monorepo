""" Rules and Macros for Managing Alembic """
load("@rules_python//python/entry_points:py_console_script_binary.bzl", "py_console_script_binary")

def alembic(name, config, versions, driver = "@pypi//psycopg2_binary"):
    """General Macro for Alembic targets

    Args:
        name: name of the target
        config: the target corresponding to alembic migration configs
        versions: the target corresponding to alembic versions
        driver: the db driver to use (postgres by default)
    """
    deps = [config, versions, driver]
    
    py_console_script_binary(
        name = name,
        pkg = "@pypi//alembic",
        data = ["//:alembic.ini"],
        script = "alembic",
        deps = deps,
    )
