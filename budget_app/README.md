# Budget App

A macOS application for personal finance management built with SwiftUI and Bazel.

## Overview

Budget App is a desktop application that helps you track your expenses, categorize transactions, and generate financial reports. It provides a clean, intuitive interface for managing your personal finances.

## Features

- **Transaction Management**: Add, edit, and delete financial transactions
- **Category Organization**: Create custom categories with subcategories
- **Data Persistence**: All data is stored locally in JSON format
- **Reports**: Visualize your spending patterns (coming soon)

## Technical Details

### Architecture

- **UI Framework**: SwiftUI
- **Build System**: Bazel
- **Minimum macOS Version**: 13.0
- **Data Storage**: Local JSON files

### Project Structure

- `app/`: Contains the application source code
  - `Models/`: Data models (Transaction, Category)
  - `Views/`: SwiftUI views
  - `Storage/`: Data persistence logic
- `resources/`: Application resources and configuration
- `tests/`: Unit tests

## Development

### Prerequisites

- Xcode 14.0+
- Bazel 6.0+

### Building the App

To build the application using Bazel:

```bash
bazel build //budget_app:BudgetApp
```


### Running Tests

To run the unit tests:

```bash
bazel test //budget_app/tests:DataStoreTests
```


## Implementation Details

- **Data Storage**: The app stores all data in JSON files in the `~/.budget` directory
- **State Management**: Uses SwiftUI's `@StateObject` and `@ObservedObject` for reactive UI updates
- **Navigation**: Implements a sidebar-based navigation with a split view

## Future Enhancements

- Budgeting features
- Data import/export
- Advanced reporting and analytics
- Cloud synchronization
