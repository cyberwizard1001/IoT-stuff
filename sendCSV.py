import firebase_admin
from firebase_admin import db
import csv
import os
# from picamera import PiCamera
import time
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials

credentials_dict = {
  "type": "service_account",
  "project_id": "solutions-challenge-345805",
  "private_key_id": "5b12ea5a625ee4bb4c6f59c2ca65ae2b99ddba54",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvO7VJQgUEluSx\n2pqOmUQkREy3wp16NNe2Oy8Pu38lSwA8LZySAQAtM+OMmkNolXqL32rYt7lb8elX\nVAU/DgzPQHX6QPbhX3224w+CMzGzDibrqFRHjNqVf43h8+XEZvFuWaLOaiy0UlsS\n0eyUhwi0Y+S/cUieFaTB1mArFmV7UKuwsXN0gzlwSPm9GjXO93VQhIptGd6Pmt9u\n4RWqY77DSXVMsGGRmOcfpZdN7Q40vYPskp/3gt8f8SYnZwODTdZmNEK9hcIvfP44\neHgUWFmfJPa9mGfuXF/yuovPLp6H0RMkYLUdhMUFtHUHOgUGdQEK0bj0Tivq25lC\nwHIn20vfAgMBAAECggEAS8bpt+LNUbVA82phoN3Feltww5xsxh6Y08yXJtoBeyqK\nUPu2c+rr3SBNvA0vrkfJxTfZuBsHFKwxqFqEpEZaorsw6YXzXPWS4yYgnECwMsqh\naRITVBekpLaSsA3tI/gSWpJ3lYSTjWz5xlMyV+5nBL8X+fOun/IjG9GtJ6TZQLAj\nEKQJ3Rnb5XYESw2XNVRFTuX+XScpk4rlm/JM6lyntHBkynCc+CRlDcBu2g28qf2e\nM8g5KQjHzYZ1cckDgG/R2cRAGH83oyhARFsXireX8Gbi1CCOHMFT0wQ9mhyzHYYS\ncl5NXB/jnXGEVljEXj0mRnifbJ4Kd0nV2mRnHF6zzQKBgQDtpsA+gnGsYy5iO+YH\n1JSMeYeL2LleKh1nCa9U5tYh75CsBdSpAHUSJP8nlGLsjruCTNmKgZLu2gjvj/N9\nBJmneMa0YArimNtWacjnYxA+b03R937htenuybn2FQ+It8Bp7wM0VoB7j1DpwHud\n30hBEXGdmBOIEZVKGGnAmGWn/QKBgQC8wz6TEqKTcrwsB4H14kE/LP9y9aYQC+oe\nMpVNcUemvpMcq8jzgUnLwUy4OnQP1CxJwgbJSsKQDiKKJ12U47VCmb7IPMcUQ/nW\nH4cqfqjSO1h0H8oc6lbSqMvTlh9F2SjdfM9A7/FsgxVjTndOg/PjEPdOjXyDM1FG\nJySmlAukCwKBgAechp256dAeoRauWnC3w0Y4gjndaBp2+Nga/E2Y0xTlKloIGcaL\n6DP7kVyAKSbwb1r+AR2phr41p4Gct6yyYAV4Hc0bIl4djTDYVIHsr1GAmRp3dc3e\n2K44MceK5yN21yfNaunbN2Q9s9a4vnzQ8Ox8lYn5m+6IuaJU49YyS1c1AoGADazn\nf6g99wi88UOp+rJln7oW17FMUqVKVN29S1sFoeL0rYMUj++x9P0QHdi+R9dLThys\neTDdX6pmfjPT59GHdEfHNqKQmbtDAmxOUpnSiUibY+5ZqjagC6sG+VFK+rh86W79\nZOr9RqtIhWVN53ZP2QeFoz9E4gx5uudjFF5taXkCgYBHg/8IAZ6f79gcNBoD8X+7\nrd2dGmzkJhbztDHDRVF1W7mkiq4eoEpnAbZv860PRmAvOZbWccUbzLtER/6rIAXj\nykNny9laJHxHFHuFM+A1UxJNr5TmT5AyTBOCqrlxPa9Lw2LI0jmQZsS/Kfy19+1M\n/D3WiLaA6OwJuUTKiAoc8Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "solutions-challenge-stuff@solutions-challenge-345805.iam.gserviceaccount.com",
  "client_id": "103377387883861479235",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/solutions-challenge-stuff%40solutions-challenge-345805.iam.gserviceaccount.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)

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

def listener(event):
    if(event.data == True):
        # camera = PiCamera()
        # time.sleep(2)
        # camera.resolution = (1280, 720)
        # camera.vflip = True
        # camera.contrast = 10

        # file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"

        # print("Start recording...")
        # camera.start_recording(file_name)
        # camera.wait_recording(10)
        # camera.stop_recording()
        # print("Done.")
        storage_client = storage.Client.from_service_account_info(credentials_dict)
        bucket = storage_client.bucket('mysample-bucket-videos')
        cmd = 'libcamera-vid -t 60000 -o test.h264'
        for i in range(0,10):
            os.system(cmd)
            time.sleep(10)
            destination_blob_name = 'video_' + str(time.time()) + '.h264'
            source_file_name = 'test.h264'

            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}.".format(
                    source_file_name, destination_blob_name
                )
            )
            os.system('rm test.h264')
            time.sleep(5)


                    


    print("DATA FROM FIREBASE: ", event.data)
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data) 

db.reference('monitor-mode', app= default_app).listen(listener)

ref = db.reference("/")
filename = "sensor_heartBeatRate.csv"
with open(filename, 'r') as csvfile: 
    # creating a csv writer object 
    reader = csv.reader(csvfile) 
    for rows in reader:
        ref.child("heartrate").set(rows[0])
        ref.child("oxygen").set(rows[1])





        
