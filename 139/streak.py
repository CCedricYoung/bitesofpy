from datetime import datetime, timedelta, date
import re

TODAY = date(2018, 11, 12)


def extract_dates(data):
    """Extract unique dates from DB table representation as shown in Bite"""
    return sorted({date.fromisoformat(x) for x in re.findall('\d{4}-\d\d-\d\d', data)}, reverse=True)


def calculate_streak(dates):
    """Receives sequence (set) of dates and returns number of days
       on coding streak.

       Note that a coding streak is defined as consecutive days coded
       since yesterday, because today is not over yet, however if today
       was coded, it counts too of course.

       So as today is 12th of Nov, having dates 11th/10th/9th of Nov in
       the table makes for a 3 days coding streak.

       See the tests for more examples that will be used to pass your code.
    """
    data = [TODAY] + dates
    streak = 0
    for x in range(1, len(data)):
        if data[x-1] - data[x] > timedelta(days=1):
            break

        streak += 1

    return streak


data = """
+------------+------------+---------+
| date       | activity   | count   |
|------------+------------+---------|
| 2018-11-12 | pcc        | 1       |
| 2018-11-11 | 100d       | 1       |
| 2018-11-10 | 100d       | 2       |
| 2018-10-15 | pcc        | 1       |
| 2018-10-15 | pcc        | 1       |
| 2018-10-05 | bite       | 1       |
| 2018-09-21 | bite       | 4       |
| 2018-09-18 | bite       | 2       |
| 2018-09-16 | bite       | 4       |
+------------+------------+---------+
"""

print(calculate_streak(extract_dates(data)))
