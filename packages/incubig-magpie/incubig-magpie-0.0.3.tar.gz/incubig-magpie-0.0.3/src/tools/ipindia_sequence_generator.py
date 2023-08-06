import dredger
from datetime import date, timedelta

def weeks_in_year(year):
    return dredger.week_count(date(year,12,31),4)

def generate_sequence(input_date):
    get_week = dredger.week_count(input_date,4)
    while input_date.year()<2021:
        pass


def generate_week_numbers(input_date):
    start_date = dredger.date_on_day(date(input_date.year(),12,31),4)
    week_count = weeks_in_year(input_date.year())
    while start_date > input_date:

    