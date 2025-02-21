# Puzzle Solver Drift 

## Overview
Puzzle Solver Drift from DSW is a **calendar puzzle solver** that determines how to arrange a set of given pieces on a **7x7 grid**, leaving only a specific month and day uncovered. The project includes a **backtracking algorithm** to find valid solutions and a **Streamlit-based web application** for an interactive user experience.

## Features
- **Solves the calendar puzzle** by determining how to arrange pieces to cover all but one month and one day.
- **Supports piece transformations (rotations and flips)** for accurate placement.
- **Provides a user-friendly Streamlit interface** for selecting month/day and visualizing the solution.
- **Dynamic solution visualization** using a colored table representation.

![618aeYh2b0L](https://github.com/user-attachments/assets/464294d2-0dc7-4920-83f1-c695793f036a)


## Installation
To run the project, ensure you have **Python 3.x** installed, then install the required dependencies:
```sh
pip install streamlit pandas numpy
```

## Usage
### Running the CLI Solver
You can use the command-line interface to solve a specific date:
```sh
python puzzle.py
```
Modify the `desired_month` and `desired_day` variables inside `puzzle.py` to set your preferred values.

### Running the Web App
To launch the Streamlit application, run:
```sh
streamlit run app.py
```
This will open the app in your web browser, where you can select a month and day and visualize the solution.

## Project Structure
```
├── puzzle.py        # Core backtracking solver logic
├── app.py           # Streamlit-based web application
└── README.md        # Project documentation
```

## How It Works
### 1. Grid Layout
The board is a **7x7 grid** with only 43 valid squares representing:
- **12 months (Jan–Dec)**
- **31 days (1–31)**
- Other squares are unused (`X`).

### 2. Puzzle Pieces
Each piece is a predefined shape covering specific squares, with transformations allowed (rotations & flips). The pieces include:
- **Red, Blue, Green, Yellow, LightBlue, Purple, Pink, Box** (Each has a unique shape and placement constraints.)

### 3. Backtracking Algorithm
The solver:
- Recursively tries to place each piece.
- Ensures the given month and day remain uncovered.
- Backtracks when a configuration is invalid.

## Web Interface
The **Streamlit app** provides:
- Dropdowns to select **month** and **day**.
- A button to **solve the puzzle**.
- **Color-coded solution visualization** using Pandas DataFrame styling.
- **Piece legend** for easy identification.

## Example Output (CLI)
![Screenshot 2025-02-21 161814](https://github.com/user-attachments/assets/4b703329-7690-4206-98bb-6da2d6946893)


(`UN` means uncovered; `..` means unused space.)

## Authors
Developed by **Thejas and Arya** exclusively for **DSW**.

## License
This project is licensed under the MIT License.

