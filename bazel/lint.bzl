load("@aspect_rules_lint//lint:ruff.bzl", "lint_ruff_aspect")

ruff = lint_ruff_aspect(
    binary = Label("@@//bazel/tools:ruff_bin"),
    configs = [
        Label("@//:.ruff.toml"),
    ],
)
