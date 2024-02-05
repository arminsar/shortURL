# shortURL

A web service in Python that can shorten URLs like TinyURL and bit.ly.

## Getting Started

### 1. Clone or download the app

### 2. Set up a virtual environment on Windows
If using Windows, navigate to the shortURL directory, and run the following commands inside the terminal:

#### Create a new virtual environment
py -m venv .venv
#### Activate a virtual environment
.venv\Scripts\python
#### Install packages from the requirements.txt
pip install -r requirements.txt

### Set up a virtual environment on Unix/macOS

If using Unix/macOS, navigate to the shortURL directory, and run the following commands inside the terminal:

#### Create a new virtual environment
python3 -m venv .venv
#### Activate a virtual environment
source .venv/bin/activate
#### Install packages from the requirements.txt
pip install -r requirements.txt

## Running the App
Navigate to shortURL directory and run the following command:
uvicorn main:app --reload

## Running the tests
Navigate to shortURL directory and run the following command:
pytest

