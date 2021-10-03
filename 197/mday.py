from datetime import date


def get_mothers_day_date(year):
    """Given the passed in year int, return the date Mother's Day
       is celebrated assuming it's the 2nd Sunday of May."""
    
    sundays = 0

    for x in range(1, 31):
        day = date(year, 5, x)
        if day.weekday() == 6:
            sundays += 1

        if sundays == 2:
            return day
