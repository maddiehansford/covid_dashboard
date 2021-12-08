from flaskapp import create_update
from flaskapp import schedule_covid_updates
from flaskapp import get_update_seconds

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_create_update():
    test = create_update('test','11:11',True,True,True)
    assert isinstance(test,dict)

def test_get_update_seconds():
    test = get_update_seconds('11:11')
    assert isinstance(test, int)
