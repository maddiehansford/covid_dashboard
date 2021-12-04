from covid_data_handler import parse_csv_data, process_covid_csv_data

def test_pcd():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240299
    assert current_hospital_cases == 7019
    assert total_deaths == 141544

if __name__ == '__main__':
    test_pcd()
    test_process_covid_csv_data()