import os
import pickle
import re
import urllib.request
from collections import namedtuple

# prework
# download pickle file and store it in a tmp file
pkl_file = "pycon_videos.pkl"
data = f"https://bites-data.s3.us-east-2.amazonaws.com/{pkl_file}"
tmp = os.getenv("TMP", "/tmp")
pycon_videos = os.path.join(tmp, pkl_file)
urllib.request.urlretrieve(data, pycon_videos)

# the pkl contains a list of Video namedtuples
Video = namedtuple("Video", "id title duration metrics")


def load_pycon_data(pycon_videos=pycon_videos):
    """Load the pickle file (pycon_videos) and return the data structure
    it holds"""
    with open(pycon_videos, "rb") as f:
        data = pickle.load(f)
    return data


def get_most_popular_talks_by_views(videos):
    """Return the pycon video list sorted by viewCount"""
    return sorted(videos, key=lambda x: int(x.metrics["viewCount"]), reverse=True)


def get_most_popular_talks_by_like_ratio(videos):
    """Return the pycon video list sorted by most likes relative to
    number of views, so 10 likes on 175 views ranks higher than
    12 likes on 300 views. Discount the dislikeCount from the likeCount.
    Return the filtered list"""
    result = sorted(
        videos,
        key=lambda x: (int(x.metrics["likeCount"]) - int(x.metrics["dislikeCount"]))
        / int(x.metrics["viewCount"]),
        reverse=True,
    )
    return result


def get_talks_gt_one_hour(videos):
    """Filter the videos list down to videos of > 1 hour"""
    return [x for x in videos if "H" in x.duration]


def get_talks_lt_twentyfour_min(videos):
    """Filter videos list down to videos that have a duration of less than
    24 minutes"""
    "PT45M8S"
    get_minutes = re.compile(r"T(2[0-3]|1?[0-9])(?=M)")
    return [x for x in videos if get_minutes.search(x.duration)]
