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

## Custom Workflows

### Create a PR

When creating a pull request from the master branch:

1. **Check current branch**: Verify if currently on master branch
2. **Create feature branch**: Create a new branch with prefix `ayush/` followed by a descriptive name
3. **Stage changes**: Add all existing changes to the staging area
4. **Commit changes**: Create a commit with an appropriate commit message
5. **Push branch**: Push the new branch to the remote repository
6. **Create PR**: Use `gh pr create` to create the pull request
7. **Update PR description**: Use `gh pr edit` to update the PR description with details of what was done

Example flow:
```bash
# Check if on master
git branch --show-current

# Create and switch to feature branch
git checkout -b ayush/feature-description

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Add feature description"

# Push to remote
git push -u origin ayush/feature-description

# Create PR
gh pr create --title "Feature description" --body "Description of changes"

# Update PR description if needed
gh pr edit --body "Updated description of changes made"
```

### Close the PR

When cleaning up after a pull request has been merged or closed:

1. **Check PR status**: Verify if the PR associated with the current branch is closed/merged
2. **Switch to master**: Switch back to the master branch
3. **Delete local branch**: Remove the local feature branch
4. **Update master**: Pull latest changes and rebase with master

Example flow:
```bash
# Check PR status for current branch
gh pr status

# Switch to master branch
git checkout master

# Delete the local feature branch (replace branch-name with actual branch)
git branch -d ayush/branch-name

# Pull latest changes and rebase
git pull --rebase origin master
```
