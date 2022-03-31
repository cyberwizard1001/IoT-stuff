from dataclasses import fields
from max30102 import MAX30102
import hrcalc
import threading
import time

import numpy as np

import csv
import json

import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate({
  "type": "service_account",
  "project_id": "solutions-challenge-345805",
  "private_key_id": "c7960dc691f8be6d3b1cace0951aeee9e07a2de4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBmyH3bTsGpWwa\nO7N/xgrBlQp2/cnN1hM7YGxwtDzO7SBbefaJc+eWrP3mUIbNTYS4Qmh+o6yub2m5\nOJGtm3w2rIYnSzxsOydMWQbjRAE+G+GGs246dS7c6Dcc1qVvcQtb8zfvxbBJAGVZ\nRPhYfx0CWdHk2ev6decpKuHnA3iLj97Hxq3WLW40pF/X3t1Roj7FNk2a1nCfYACD\nO68GTFs5OFssRRdkrRs/Y3cZBud5BEna1SdimZI3aqhyeBIimn4QyBt66p/gYh6z\n6K19MSTa8Vi+tTRObljjjM5ZoYkCeD1TeeXI035LHSUsVvgvfAHWaHw9Et3PlgVb\nUzy1nVd/AgMBAAECggEARHlkswkMBla9fC2/V6KorTzUXa93D3j2hlqdH+NvWlRd\nzFy/iG/Y6d63Uh0LAFO5bB34rUmgSnWXM+5A/+DtNr0gGYevkCv/wy39lKW5tsjP\no/+ULdLCR1lOHMIB8v9NYDEOiJwntDoSnlcZattSXEF+Te2RW50Vq+bBzR3aJamY\nE+tEt0i/piUaCrkHhiuLRqh14sbc7LlC16QldZixVUeX8aFH7F+R9KHtpMaS8rNq\nF4TPY5+LDwLHzevMlKXvn14roiEuzZULOy4EUPti8Cvb35ZYBswTSociH4noFNRt\nAxci3V9b7XJAY9ij3sFU8+Hm9DAs/8rO57Zg7LlI0QKBgQDqqq4BYsSGwx6hD4zw\n+QNhQ4YWcu8u7cV9zU7A3B9Up9hRwMzbxwR5Op2mrFv4ChBLYmah/PjRsRJ7gtjy\nmDQNLUjmhy7UzaGqBSZe69l1PFzD3OP4fEDNcFnlJQ+bZFbhgyJLkFAMl25WBJuR\n6n9dElACFEzVxcSB7JeoLURX6QKBgQDTNNw7MdKRPhGnl03HYMrwWKOQQpbu8/1o\nXA6D9sBIUOMh3qwRziZLGKpEJAlsglUIejupinCfrCEe71a7bbNt1kdo/Yg0iiIc\n9wUypbY6Rthk6Tb3+SRHBdTtIThDI1UJmqRtppG4qjGT4N7M2KNoTl/FZ4E443Dj\newtQdt97JwKBgQCPwNz1Zl7DuzXBLniFidXDOI0kpWXWVrv7s9CBnpbm0idW9YfJ\nPqKD7R90YfO4/9k5hN8gboqyUgnjdaWW/xwr0kjtR3St0gYt1BfMYCiHg+HD7kYN\nC3jbIO9AyzJDW/VJEn7o0U/oVr+1m/79JSy+hCBVFcB32D3n5VqGIKzUOQKBgCNM\nXVZDUGbX0cmJnwUoZyJeHg/5IRKUkpCDeiWR8rbjVeKOPYHIS1wXpjU3NJ/+9Ekz\nbI88RPBaqzppU7yFbAx6WHryjHYDdAoVOrgpO9hniLjsxTQSXn7EOb7b43RNDmRJ\nhRuSUB5ly11korfnqP/AwX7TeqRQVsieAtkS1OzXAoGAcKmNFULxMOXD4eOkHCvz\nKrpd4jO51Zo3fTlfy1c+4/Uo6BfK0cbD0rV+am4lxEs5hDkO0cf0Duu0WPoLCJV7\nCe/NABSixCETLJ+ec8PQRtJa4IysAZtwZch3rFpyENCzb2eUJXazaD1UHrD5wHXe\nWehSBkkyGm6dsI+gupRNwGo=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-lbl4o@solutions-challenge-345805.iam.gserviceaccount.com",
  "client_id": "109126900938867603601",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lbl4o%40solutions-challenge-345805.iam.gserviceaccount.com"
}
)
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://solutions-challenge-345805-default-rtdb.firebaseio.com/"
    })

ref = db.reference("/")

# heartRateRef = db.reference("heartrate")
# spo2Ref = db.reference("spo2")
# triggerSentryRef = db.reference("trigger-sentry")


class HeartRateMonitor(object):
    """
    A class that encapsulates the max30102 device into a thread
    """

    LOOP_TIME = 0.1

    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print("IR, Red")
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self, filename="sensor_heartBeatRate.csv"):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []

        # run until told to stop
        while not self._thread.stopped:
            # check if any data is available
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)
                    if self.print_raw:
                        print("{0}, {1}".format(ir, red))

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                    if valid_bpm:
                        bpms.append(bpm)
                        while len(bpms) > 4:
                            bpms.pop(0)
                            self.bpm = np.mean(bpms)
                            if np.mean(ir_data) < 50000 and np.mean(red_data) < 50000:
                                self.bpm = 0
                                if self.print_result:
                                    print("Finger not detected")
                            if self.print_result:

                                print("BPM: {0}, SpO2: {1}".format(self.bpm, spo2))
                                # filename = "sensor_heartBeatRate.csv"
        
                                # writing to csv file 
                                # with open(filename, 'w') as csvfile: 
                                #     # creating a csv writer object 
                                #     csvwriter = csv.writer(csvfile) 
                                        
                                #     # writing the fields 
                                #     fields = [self.bpm, spo2]
                                #     csvwriter.writerow(fields)

                                # a Python object (dict):
                                # x = {
                                # "heartrate": self.bpm,
                                # "oxygen": spo2,
                                # "trigger-sentry": False
                                # }
                                
                                # ref.set(x)

                                # # the result is a JSON string:
                                # print(x)


            time.sleep(self.LOOP_TIME)

        # sensor.shutdown()

    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()

    def stop_sensor(self):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join()
