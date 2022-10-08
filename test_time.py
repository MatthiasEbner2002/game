from datetime import datetime
import time
start = datetime.now()
sleep_time = 0.1
# Statements
time.sleep(sleep_time)

end = datetime.now()
print("sleep_time:         " + str(sleep_time))
print("start:              " + str(start))
print("end:                " + str(end))
print("div:                " + str(end-start))
print("div_sek:            " + str((end-start).total_seconds()))
print("div < sleep_time:   " + str((end-start).total_seconds() < sleep_time))
