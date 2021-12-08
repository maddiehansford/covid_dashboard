# README

## Introduction
This project is a **covid dashboard** that displays current covid data and news taken from the uk-covid19 API. It also enables the user to update the data and news.

## Prerequisites
**Version:** Python 3.9.7

## Installation

### 1. Creating a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installing requirements:

Try
```
pip3 install -r requirements.txt
```

If this fails, install requirements separately
```
pip3 install flask
pip3 install uk-covid19
pip3 install pylint
pip3 install pytest
```

## Getting started tutorial

How to run code:
```
python3 flaskapp.py
```

Then open http://127.0.0.1:5000/ in chosen web browser.

## Testing

Tests are located in the 'tests' folder, and include: 

*test_flaskapp.py* that tests functions in the *flaskapp.py* module

*test_covid_data_handler.py* that tests functions in the *covid_data_handler.py* module

*test_covid_news_handler.py* that tests functions in the *covid_news_handling.py* module


**In order to run tests, enter the following into the terminal:**

```
pytest
```

Whether the tests have passed will appear in the terminal.

## Developer documentation


## Details

**Author:** Madelene Hansford

**License:** MIT License

**Link to source:** https://github.com/maddiehansford/covid_dashboard

**Acknowledgements:** Matt Collison, Hugo Barbosa