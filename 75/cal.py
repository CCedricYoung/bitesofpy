import collections
import re

def get_weekdays(calendar_output):
    """Receives a multiline Unix cal output and returns a mapping (dict) where
       keys are int days and values are the 2 letter weekdays (Su Mo Tu ...)"""
    lines = re.sub('   ', ' 0 ', calendar_output).splitlines()
    days = lines[1].split()

    # Overly complicated solution
    weekdays = dict(collections.ChainMap(*[
        {
            int(date):days[index] 
            for index,date 
            in enumerate(line.split()) 
            if date != '0'
        }
        for line in lines[2:]
    ]))

    # Better solution
    lines = calendar_output.splitlines()
    days = lines[1].split()
    weekdays = {}

    for line in lines[2:]:
        matches = re.findall(r'\s\s\s|\s\d\s?|\d\d\s?', line)
        for x,day in zip(matches, days):
            if x.strip():
                weekdays[int(x)] = day

    return weekdays

april_1981 = """     April 1981
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30
"""

print(get_weekdays(april_1981))