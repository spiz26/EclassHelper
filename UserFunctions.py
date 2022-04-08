import time
from datetime import datetime
from selenium.webdriver.common.alert import Alert

def DeadLine(dead):
    """time compare function"""
    #Now time
    Now_date = time.strftime('%x', time.localtime(time.time())).split("/")
    Now_time = time.strftime('%X', time.localtime(time.time())).split(":")
    
    Now_date = int(Now_date[2] + Now_date[0] + Now_date[1])
    t = list(map(int, Now_time))
    Now_time = t[0]*60 + t[1] 

    #Dead Line
    dead = dead.split(" ")
    dead_date = dead[0].split(".")
    dead_date[0] = dead_date[0][2:]
    dead_date = int("".join(dead_date))

    if dead[1] == "오전":
        noon = 0
    else:
        noon = 12
    
    dead_time = list(map(int, dead[2].split(":")))
    dead_time[0] += noon
    dead_time = dead_time[0]*60 + dead_time[1]

    #compare
    if Now_date >= dead_date:
        return False

    elif Now_time >= dead_time:
        return False
    else:
        return True

def RestTime(time_string):
    """Calculating the Time Difference"""
    time_string = time_string.replace(" ", "").split("/")
    numerator = time_string[0]
    denominator = time_string[1]
    time_format1 = ""
    time_format2 = ""

    #numerator
    if "시" in numerator:
        time_format1 = "%I시"

    if "분" in numerator:
        time_format1 += "%M분"

    if "초" in numerator:
        time_format1 += "%S초"

    #denominator
    if "시" in denominator:
        time_format2 = "%I시"

    if "분" in denominator:
        time_format2 += "%M분"

    if "초" in denominator:
        time_format2 += "%S초"

    numer_time = datetime.strptime(numerator, time_format1)
    denom_time = datetime.strptime(denominator, time_format2)

    if denom_time < numer_time:
        return 60

    return (denom_time-numer_time).seconds + 3

def alert_accept(browser):
    Alert(browser).accept()
    time.sleep(0.3)