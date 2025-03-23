"""Rules and macros for building Swift applications for macOS."""

load("@build_bazel_rules_apple//apple:macos.bzl", "macos_application")
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")


def macos_swift_app(name, srcs, infoplist, minimum_os_version = "10.13", bundle_id = None, **kwargs):
    """
    A custom macro to create a macOS Swift app.

    Args:
        name: The target name for the app.
        srcs: A list of Swift source files.
        infoplist: The path to the Info.plist file.
        minimum_os_version: The minimum supported macOS version.
        bundle_id: The bundle ID for the app.
        **kwargs: Additional arguments to pass to the swift_bundle rule.
    """

    if bundle_id == None:
        bundle_id = "com.example." + name

    swift_library(
        name = name + "_lib",
        srcs = srcs,
        **kwargs
    )

    macos_application(
        name = name,
        bundle_id = bundle_id,
        families = ["mac"],
        infoplists = infoplist,
        minimum_os_version = minimum_os_version,
        deps = [":" + name + "_lib"],
    )
    
    
