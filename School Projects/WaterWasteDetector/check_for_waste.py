import os
import time
from datetime import date

file_count = "calibration/count"

SPAN = 1 
TODAYS_DATE = date.today().strftime("%d-%m-%y")

# Medianen importes
with open("calibration/median_diff") as f:
    med = float(f.read())

if os.path.exists(file_count):
    with open(file_count) as f:
        count = int(f.read())
else:
    count = 0

with open(f"logs/log_data_{TODAYS_DATE}.csv", "r") as f:
    for line in f:
        pass
    last_input = float(line.split(",")[3])
if last_input < med+SPAN and last_input > 0-SPAN:
    count = 0
else:
    count += 1
with open(file_count, "w") as f:
    f.write(str(count))
