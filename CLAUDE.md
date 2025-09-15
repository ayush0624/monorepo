# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal projects monorepo built with Bazel, containing multiple applications and tools. The repository uses Bazel's MODULE.bazel system for dependency management and follows a structured approach to multi-language development.

## Project Structure

- **budget_app/**: SwiftUI macOS application for personal finance management
  - Uses custom Bazel macros for Swift app builds
  - Stores data in JSON format locally in `~/.budget`
  - Architecture: Models, Views, Storage layers
- **git/**: Go CLI application built with Cobra framework
- **bazel/**: Shared Bazel configuration and custom macros
  - `swift/macros.bzl`: Custom macros for building macOS Swift applications
  - `go/`: Go module configuration and dependencies

## Build Commands

### Budget App (Swift/macOS)
```bash
# Build the Budget App
bazel build //budget_app:BudgetApp

# Run tests for Budget App
bazel test //budget_app/tests:DataStoreTests
```

### Git CLI Tool (Go)
```bash
# Build the Git CLI binary
bazel build //git:binary
```

### General Bazel Commands
```bash
# Build all targets
bazel build //...

# Run all tests
bazel test //...

# Clean build artifacts
bazel clean
```

## Architecture Notes

### Custom Bazel Macros
The repository uses custom Swift macros defined in `bazel/swift/macros.bzl`:
- `macos_swift_app()`: Simplifies creating macOS applications with Swift
- Automatically generates bundle IDs and handles swift_library + macos_application setup

### Dependencies
- **Swift**: Uses rules_swift, rules_apple, and apple_support
- **Go**: Managed through go.mod in `bazel/go/` with Cobra CLI framework
- **Bazel Version**: Uses MODULE.bazel (bzlmod) instead of legacy WORKSPACE

### Configuration
- `.bazelrc`: Enables Go race detection and specific tool configurations
- Minimum macOS version: 13.0 for Swift applications
- Go version: 1.20

## Development Workflow

1. The monorepo is structured to support multiple independent projects
2. Each project has its own BUILD.bazel files and follows language-specific conventions
3. Shared Bazel configuration is centralized in the `bazel/` directory
4. Tests are co-located with source code in dedicated test directories