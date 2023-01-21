"""_summary_
    Åbner de 3 seneste logs og kombinere dem til en samlet fil. Bruger så den samlede data til at finde medianen.
    Returns:
        Medianen som gemmes i en fil for sig selv.
"""
from datetime import date, timedelta
from functools import lru_cache

from numpy import median

FILE_CALIBRATION = "calibration/calibration.csv"


@lru_cache(maxsize=None)
def make_the_file():
    day1 = date.today() - timedelta(days=2)
    day1 = day1.strftime("%d-%m-%y")
    day2 = date.today() - timedelta(days=1)
    day2 = day2.strftime("%d-%m-%y")
    day3 = date.today().strftime("%d-%m-%y")
    with open(f"logs/log_data_{day1}.csv", "r") as file:
        data = file.read()
    with open(f"logs/log_data_{day2}.csv", "r") as file:
        next(file) 
        data2 = file.read()
    with open(f"logs/log_data_{day3}.csv", "r") as file:
        next(file)  
        data3 = file.read()
    data += data2
    data += data3
    with open(FILE_CALIBRATION, "w") as file:
        file.write(data)


@lru_cache(maxsize=None)
def file_data() -> list:
    readings = [[], [], [], []]
    with open(FILE_CALIBRATION, "r") as file:
        next(file)
        for line in file.read().splitlines():
            time, room, pipe, diff = line.split(",")
            readings[0].append(time)
            readings[1].append(float(room))
            readings[2].append(float(pipe))
            readings[3].append(float(diff))
    return readings


def room_temp() -> list:
    return file_data()[1]


def pipe_temp() -> list:
    return file_data()[2]


def diff_temp() -> list:
    return file_data()[3]


def get_median(temperature: list) -> float:
    return median(temperature)


def write_median():
    with open("calibration/median_diff", "w") as file:
        file.write(f'{get_median(diff_temp())}')


def __main__():
    make_the_file()
    write_median()


if __name__ == '__main__':
    __main__()
