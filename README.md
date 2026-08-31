# ICICI 2024 Dashboard

A lightweight, local Flask web application designed to serve as a dashboard for browsing and downloading directories inside the `icici_2024` workspace as compressed ZIP files.

## Features

* **Dynamic Folder Listing**: Automatically scans the base directory and lists all available subdirectories along with their total file counts.
* **On-the-Fly Zipping**: Instantly compresses requested folders into ZIP archives using Python's temporary directories and `shutil`.
* **Premium Glassmorphism UI**: A stunning, modern dark-mode frontend built with pure HTML and CSS (no external CSS frameworks required).
* **Animations & Hover Effects**: Smooth UI transitions that provide a great user experience.

## Prerequisites

* Python 3.7+
* `pip` (Python package manager)

## Installation & Setup

1. Open your terminal or command prompt and navigate to this directory:
   ```powershell
   cd c:\Users\ADMIN\Desktop\icici_2024\dashboard_app
   ```

2. Activate the virtual environment (if it is not already activated):
   ```powershell
   .\venv\Scripts\activate
   ```
   *(Note: The virtual environment `venv` should already be created with Flask installed)*

3. Run the Flask application:
   ```powershell
   python app.py
   ```

## Usage

1. Open a web browser and navigate to the application URL:
   [http://127.0.0.1:7890](http://127.0.0.1:7890)
2. You will see a grid of folders from your `icici_2024` workspace.
3. Click the **Download ZIP** button on any folder to download its contents.

## Project Structure

* `app.py`: The main Flask backend script that handles routing, folder scanning, and ZIP generation.
* `templates/index.html`: The frontend UI template using a glassmorphism dark theme.
* `venv/`: The isolated Python virtual environment for dependencies.

## Technical Details

- The application uses `tempfile` to securely build ZIP archives in temporary directories to prevent cluttering the main workspace.
- The UI is powered by vanilla CSS using CSS Variables (`:root`) and grid layouts, making it highly customizable without requiring node modules.
