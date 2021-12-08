# README

## Introduction
This project is a **covid dashboard** that displays current covid data and news taken from the uk-covid19 API. It also enables the user to update the data and news.

## Prerequisites
**Version:** Python 3.9.7

## Installation

### 1. Creating a virtual environment:

In the terminal, enter the covid_dashboard
``` 
cd covid_dashboard
```

Check this with *pwd* command
```
pwd
```
The root should end in */covid_dashboard*

Create and enter the virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

Your terminal prompt should now look something like this:
```
(.venv) maddiehansford@Maddies-MacBook covid_dashboard %
```

### 2. Installing requirements:

**NOTE:** Must be in virtual environment before installing.

Install all the requirements from the requirements.txt file:
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

### 1. How to run the code:

Enter the following into terminal:
```
python3 flaskapp.py
```

Then open http://127.0.0.1:5000/ in chosen web browser.

### 2. How to use the code:

1. Enter the time you'd like an update at into the 'Schedule data updates' box.

2. Tick the 'Repeat update' box if you would like the update to be repeated.

3. Tick either the 'Update Covid data' box, the 'Update news articles' box, or both depending on what you would like updated.

4. Click 'submit' and the update appear in the top left corner, and will occur at your chosen time.

5. Cancel an update or delete a news article by clicking the 'x' in the top right corner of the box.

## Testing

### 1. Setting up the tests

Make sure you are in the virtual environment and root folder of the project, which should look something like this:
```
(.venv) maddiehansford@Maddies-MacBook covid_dashboard %
```

You must now deactivate the virtual environment and then activate it again.
Deactivate your virtual environment by entering the following into the terminal:
```
deactivate
```

Now, reactivate your virtual environment by entering the following into the terminal:
```
source .venv/bin/activate
```

Run the setup.py file by entering the following into the terminal, *including the period*:
```
pip install -e .
```

### 2. Running the tests

Tests are located in the 'tests' folder, and include: 

- ***test_flaskapp.py*** that tests functions in the ***flaskapp.py*** module,

- ***test_covid_data_handler.py*** that tests functions in the ***covid_data_handler.py*** module,

- ***test_covid_news_handler.py*** that tests functions in the ***covid_news_handling.py*** module.


**In order to run tests, enter the following into the terminal:**

```
pytest
```

Whether the tests have passed will appear in the terminal.

## Developer documentation

Sphinx developer documentation can be found in:
```
docs/build/html
```

Open ***index.html*** in your chosen web browser.

## Details

**Author:** Madelene Hansford

**License:** MIT License

**Link to source:** https://github.com/maddiehansford/covid_dashboard

**Acknowledgements:** Matt Collison, Hugo Barbosa