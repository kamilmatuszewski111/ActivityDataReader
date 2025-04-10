
import re
import time

from matplotlib import ticker

from fit_file_decoder import FitFileDecoder
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

import time

from strava_api import StravaAPIRequests


if __name__ == "__main__":
    # paces = defaultdict(list)
    # kupa = FitFileDecoder(r"C:\Users\Pan Mirek\Downloads\13_DOZ_Maraton.fit")
    # kupa.define_records("heart_rate", "enhanced_speed", "timestamp")
    # kupa.define_hr_limits(120, 151)
    # pace = kupa.calculate_average_pace()
    # key, value = next(iter(pace.items()))
    # paces[key] = value

    LOW_HR_LIMIT = 100
    HIGH_HR_LIMIT = 151

    kupa = StravaAPIRequests()
    activities = kupa.collect_required_data()

    training_dict = defaultdict(list)

    for key, value in activities.items():
        hr_in_limit = [hr for hr, speed in zip(activities[key][1], activities[key][2]) if LOW_HR_LIMIT <= hr <= HIGH_HR_LIMIT and speed*3.6]
        mps_to_kmh = [speed*3.6 for hr, speed in zip(activities[key][1], activities[key][2]) if LOW_HR_LIMIT <= hr <= HIGH_HR_LIMIT and speed*3.6]
        training_dict[activities[key][0]].append(sum(hr_in_limit)/len(hr_in_limit))
        training_dict[activities[key][0]].append(FitFileDecoder.pace_calculate(sum(mps_to_kmh)/len(mps_to_kmh)))


