# 🧱 Flutter Clean Architecture Mason Template

This repository contains an automated Python script (`setup_mason.py`) that generates a complete set of [Mason](https://github.com/felangel/mason) bricks for Flutter. This template enforces a standardized Clean Architecture structure (Domain, Data, and Presentation layers) to drastically speed up your Flutter project initialization.

## 🚀 Getting Started

Follow these steps to set up the template and use it in your Flutter projects.

### 1. Activate Mason CLI
First, you need to install the Mason CLI globally on your machine using Dart:
```bash
dart pub global activate mason_cli
```
*(Ensure your Dart pub-cache is in your system PATH so you can use the `mason` command).*

### 2. Generate and Register the Bricks
Clone or download this repository, then run the Python generator script to create the bricks locally:

```bash
# Run the generator script
python setup_mason.py
```
This will automatically generate a `bricks/` folder containing three templates: `core_setup`, `data_layer`, and `presentation_layer`.

Next, register these bricks **globally** so you can use them in any project:
```bash
mason add -g core_setup --path ./bricks/core_setup
mason add -g data_layer --path ./bricks/data_layer
mason add -g presentation_layer --path ./bricks/presentation_layer
```

---

## 🛠 Usage in a New Flutter Project

Once the bricks are registered globally, you can easily apply them to any new project.

### 1. Create Project & Add Dependencies
Create your Flutter project and install the mandatory packages that this architecture depends on:
```bash
flutter create my_awesome_app
cd my_awesome_app

# Add required dependencies
flutter pub add get_it http google_fonts fpdart
flutter pub add flutter_bloc equatable
```

### 2. Inject the Architecture (Mason Make)
Now, use the mason templates to generate the boilerplate code!

**A. Generate Core Setup**
Creates the main structural files (App, routing, themes, dependency injection).
```bash
mason make core_setup
```
*(When prompted, enter your project name, e.g., `my_awesome_app`)*

**B. Generate Data & Domain Layer for a Feature**
Creates the Models, Repositories, Data Sources, and Entities for a specific feature.
```bash
mason make data_layer
```
*(When prompted, enter the feature name, e.g., `auth` or `movies`)*

**C. Generate Presentation Layer for a Feature**
Creates the BLoC state management, Pages, and reusable Widgets for a specific feature.
```bash
mason make presentation_layer
```
*(When prompted, enter the feature name, e.g., `auth` or `movies`)*

---

## 📂 Generated Folder Structure Example
After running the commands above for a feature named `auth`, your `lib/` directory will look like this:

```text
lib/
├── app/                  # App initialization & Dependency Injection
├── core/                 # Global configs, routing, themes, custom UI
├── features/
│   └── auth/
│       ├── data/         # Data sources, Models, Repositories implementation
│       ├── domain/       # Entities, Repositories interface
│       └── presentation/ # BLoC, Pages, Widgets
└── main.dart
```

## 📜 License
This project is open-source and available under the MIT License. Feel free to fork, modify, and use it for your own projects!
