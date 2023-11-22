# Dynamic Carpooling API


## Overview

The Dynamic Carpooling API is a FastAPI-based project that provides dynamic carpooling functionalities, allowing users to find and share rides seamlessly.

## Features

- User registration and authentication (Authentication not yet implemented)
- Demand and offer services
- Matrix off origin and destinations (To be implemented)
- ...

## Getting Started

To run this project locally, follow the instructions below.

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python](https://www.python.org/) (>= 3.6)
- Code editor - preferably Vscode

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ihonore/Dynamic-Carpooling-API.git

2. Navigate to the project directory:
    ```bash
    cd dynamic-carpooling-api
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv env
4. Activate the virtual environment:
- On Windows:
    ```bash
    .\env\Scripts\activate
- On MacOs:
    ```bash
    source env/bin/activate

5. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Finally run the Application
   ```bash
   uvicorn main:app --reload

### Usage
    Once the application is running, you can access at http://127.0.0.1:8000/docs
    for interactive documentation.

![screencapture-127-0-0-1-8000-docs-2023-11-22-23_31_52](https://github.com/ihonore/Dynamic-Carpooling-API/assets/79599396/b8f1ea47-8239-4465-8b30-5929d2fe1b98)
