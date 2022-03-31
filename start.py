from fileinput import filename
from heartrate_monitor import HeartRateMonitor
import time
import argparse
import os
while True:
    parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="print raw data instead of calculation result")
    parser.add_argument("-t", "--time", type=int, default=10,
                        help="duration in seconds to read from sensor, default 30")
    args = parser.parse_args()

    print('sensor starting...')
    hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
    hrm.start_sensor()
    try:
        time.sleep(args.time)
    except KeyboardInterrupt:
        print('keyboard interrupt detected, exiting...')

    hrm.stop_sensor()
    print('sensor stoped!')

    cmd = 'python sendCSV.py'
    os.system(cmd)
    time.sleep(10)
    filename = "sensor_heartBeatRate.csv"
    with open(filename, 'w') as f:
        f.truncate()