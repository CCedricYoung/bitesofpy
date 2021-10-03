from datetime import datetime
from typing import List


def get_srt_section_ids(text: str) -> List[int]:
    """Parse a caption (srt) text passed in and return a
       list of section numbers ordered descending by
       highest speech speed
       (= ratio of "time past:characters spoken")

       e.g. this section:

       1
       00:00:00,000 --> 00:00:01,000
       let's code

       (10 chars in 1 second)

       has a higher ratio then:

       2
       00:00:00,000 --> 00:00:03,000
       code

       (4 chars in 3 seconds)

       You can ignore milliseconds for this exercise.
    """

    results = []
    for section in text.split("\n\n"):
        lines = section.strip().split("\n")
        id = int(lines[0])
        times = lines[1].split(" --> ")
        start = datetime.strptime(times[0], "%H:%M:%S,%f")
        end = datetime.strptime(times[1], "%H:%M:%S,%f")
        duration = end - start
        speed = len(lines[2]) / duration.total_seconds()
        results.append((speed, id))

    results.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in results]