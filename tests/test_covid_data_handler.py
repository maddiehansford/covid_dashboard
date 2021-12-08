from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import local_7_days_extract
from covid_data_handler import national_7_days_extract
from covid_data_handler import hospital_cases_extract
from covid_data_handler import total_deaths_extract
from covid_data_handler import data_gatherer

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_local_7_days_extract():
    test = local_7_days_extract()
    assert isinstance(test, int)

def test_national_7_days_extract():
    test = national_7_days_extract()
    assert isinstance(test, int)

def test_hospital_cases_extract():
    test = hospital_cases_extract()
    assert isinstance(test, int)

def test_total_deaths_extract():
    test = total_deaths_extract()
    assert isinstance(test, int)

def test_data_gatherer():
    test = data_gatherer()
    assert isinstance(test, list)

