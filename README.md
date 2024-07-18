# Quiniela Predictor

## Overview

Quiniela Predictor is a Python project designed to scrape the latest lottery numbers from LaBanca's website. The program continuously updates the data, providing users with the most recent lottery results. It stores the scraped data in CSV format and organizes it with the `organizer.py` script. Additionally, it includes a function to calculate the probabilities of numbers appearing in future draws and display these probabilities along with the top 5 most probable numbers.

## Features

- **Scrape Lottery Numbers**: Automatically scrapes the latest lottery numbers from LaBanca's website.
- **Constantly Updated Data**: Continuously updates the lottery numbers as LaBanca only shows results from the last two months.
- **Graphical Visualization**: Provides an option to visualize the data with graphs (currently has bugs and needs improvement).
- **CSV Data Storage**: Stores the scraped data in CSV format for easy access and manipulation.
- **Data Organization**: Uses `organizer.py` to organize the data.
- **Probability Calculation**: Calculates and displays the probabilities of numbers appearing in future draws.
- **Top 5 Most Likely Numbers**: Displays the top 5 most probable numbers based on historical data.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Quiniela-Predictor.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Quiniela-Predictor
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Scraping Lottery Numbers

The main script to scrape the lottery numbers is `crawler.py`. It uses Selenium to navigate to LaBanca's website and extract the latest results.

### Organizing Data

The `organizer.py` script organizes the scraped data and saves it in a structured CSV format.

### Calculating Probabilities

The `calculate_probabilities` function in the `probabilities.py` script calculates the probabilities of numbers appearing in future draws. It also displays the top 5 most likely numbers.

