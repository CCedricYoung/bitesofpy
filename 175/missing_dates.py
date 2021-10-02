from dateutil.rrule import rrule, DAILY

def get_missing_dates(dates):
    """Receives a range of dates and returns a sequence
       of missing datetime.date objects (no worries about order).

       You can assume that the first and last date of the
       range is always present (assumption made in tests).

       See the Bite description and tests for example outputs.
    """
    dates.sort()
    start, end = dates[0], dates[-1]
    all_dates = {
        date.date()
        for date in rrule(freq=DAILY, count=(end - start).days, dtstart=start)
    }
    return all_dates - set(dates)