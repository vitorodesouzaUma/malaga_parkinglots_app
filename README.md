# Open Data App Prototype

Welcome to the Open Data App Prototype repository! This application provides real-time information on parking lot occupancy in Málaga City based on open data sources.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)

## Overview

The Open Data App Prototype is a web application built with Flask and Leaflet, offering a live view of parking lot usage in Málaga City. This README provides instructions on how to set up and run the application on your local machine.

## Prerequisites

Before running the application, ensure you have the following installed:

- [Python](https://www.python.org/) (version 3.6 or higher)
- [pip](https://pip.pypa.io/en/stable/)
- Git

Make sure to have a mondoDB database created and configured, with data inserted.
If needed, you can use the .json example files to insert manually the data in your collections.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/vitorodesouza/malaga_parkinglots_app.git
   
2. Navigate to the project directory:

    ```bash
    cd malaga_parkinglots_app

3. Create a virtual environment:

    ```bash
    python -m venv venv


4. Activate the virtual environment:

    ```bash
    .\venv\Scripts\activate

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the Flask application:

    ```bash
    python app.py

3. Open your web browser and go to http://127.0.0.1:5000/ to access the application.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the application.
