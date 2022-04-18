import firebase_admin
from firebase_admin import db
import csv
import os
# from picamera import PiCamera
import time
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials

# credentials_dict = {
#   "type": "service_account",
#   "project_id": "solutions-challenge-345805",
#   "private_key_id": "5b12ea5a625ee4bb4c6f59c2ca65ae2b99ddba54",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvO7VJQgUEluSx\n2pqOmUQkREy3wp16NNe2Oy8Pu38lSwA8LZySAQAtM+OMmkNolXqL32rYt7lb8elX\nVAU/DgzPQHX6QPbhX3224w+CMzGzDibrqFRHjNqVf43h8+XEZvFuWaLOaiy0UlsS\n0eyUhwi0Y+S/cUieFaTB1mArFmV7UKuwsXN0gzlwSPm9GjXO93VQhIptGd6Pmt9u\n4RWqY77DSXVMsGGRmOcfpZdN7Q40vYPskp/3gt8f8SYnZwODTdZmNEK9hcIvfP44\neHgUWFmfJPa9mGfuXF/yuovPLp6H0RMkYLUdhMUFtHUHOgUGdQEK0bj0Tivq25lC\nwHIn20vfAgMBAAECggEAS8bpt+LNUbVA82phoN3Feltww5xsxh6Y08yXJtoBeyqK\nUPu2c+rr3SBNvA0vrkfJxTfZuBsHFKwxqFqEpEZaorsw6YXzXPWS4yYgnECwMsqh\naRITVBekpLaSsA3tI/gSWpJ3lYSTjWz5xlMyV+5nBL8X+fOun/IjG9GtJ6TZQLAj\nEKQJ3Rnb5XYESw2XNVRFTuX+XScpk4rlm/JM6lyntHBkynCc+CRlDcBu2g28qf2e\nM8g5KQjHzYZ1cckDgG/R2cRAGH83oyhARFsXireX8Gbi1CCOHMFT0wQ9mhyzHYYS\ncl5NXB/jnXGEVljEXj0mRnifbJ4Kd0nV2mRnHF6zzQKBgQDtpsA+gnGsYy5iO+YH\n1JSMeYeL2LleKh1nCa9U5tYh75CsBdSpAHUSJP8nlGLsjruCTNmKgZLu2gjvj/N9\nBJmneMa0YArimNtWacjnYxA+b03R937htenuybn2FQ+It8Bp7wM0VoB7j1DpwHud\n30hBEXGdmBOIEZVKGGnAmGWn/QKBgQC8wz6TEqKTcrwsB4H14kE/LP9y9aYQC+oe\nMpVNcUemvpMcq8jzgUnLwUy4OnQP1CxJwgbJSsKQDiKKJ12U47VCmb7IPMcUQ/nW\nH4cqfqjSO1h0H8oc6lbSqMvTlh9F2SjdfM9A7/FsgxVjTndOg/PjEPdOjXyDM1FG\nJySmlAukCwKBgAechp256dAeoRauWnC3w0Y4gjndaBp2+Nga/E2Y0xTlKloIGcaL\n6DP7kVyAKSbwb1r+AR2phr41p4Gct6yyYAV4Hc0bIl4djTDYVIHsr1GAmRp3dc3e\n2K44MceK5yN21yfNaunbN2Q9s9a4vnzQ8Ox8lYn5m+6IuaJU49YyS1c1AoGADazn\nf6g99wi88UOp+rJln7oW17FMUqVKVN29S1sFoeL0rYMUj++x9P0QHdi+R9dLThys\neTDdX6pmfjPT59GHdEfHNqKQmbtDAmxOUpnSiUibY+5ZqjagC6sG+VFK+rh86W79\nZOr9RqtIhWVN53ZP2QeFoz9E4gx5uudjFF5taXkCgYBHg/8IAZ6f79gcNBoD8X+7\nrd2dGmzkJhbztDHDRVF1W7mkiq4eoEpnAbZv860PRmAvOZbWccUbzLtER/6rIAXj\nykNny9laJHxHFHuFM+A1UxJNr5TmT5AyTBOCqrlxPa9Lw2LI0jmQZsS/Kfy19+1M\n/D3WiLaA6OwJuUTKiAoc8Q==\n-----END PRIVATE KEY-----\n",
#   "client_email": "solutions-challenge-stuff@solutions-challenge-345805.iam.gserviceaccount.com",
#   "client_id": "103377387883861479235",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/solutions-challenge-stuff%40solutions-challenge-345805.iam.gserviceaccount.com"
# }

# credentials = ServiceAccountCredentials.from_json_keyfile_dict(
#     credentials_dict
# )

cred_obj = firebase_admin.credentials.Certificate({
  "type": "service_account",
  "project_id": "womens-safety-2022",
  "private_key_id": "cd81202ee9aeb81249bd77805d77cfe9912f6f22",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUq5BFPvuxkeL1\n15j+TmKQYJztDJilgRPqf9UAf2GGyHU3Gvy6bGqDwI8V/gxWbrjij0DEH5zi86BP\n6EowcCQ2OFZCsB4pgnvkBlqaz+mMPIwj684aV1Nr4POpkL6RXrTumGERDz1i0GBr\nKf5oQAUnujCJzrcn9w8GseoEQqqTefqAWzackdh374TOWZOQk+kG+h+sGuKt0HWm\nvXrn3xWhdsJA9sTsYqYlRaqjlVZ2mt5rqglU6NhbNbFWo7UiQ7JGHkwd7bh666rb\nwXRta8ivSKHD6uglKlX5z8UfcOVtmKXR1CCVHjbkIH4EblKbZ8dtMM0YkA6Ab7SS\nkAWdJEcrAgMBAAECggEAYeB7y4LLL9QmkmKhZRkKP8xXLLoJXtJjKh+fFlWJuxBy\n8eOXwOy4sN5kfAiqAPWAXbT0Z87s036wn1YXHufdop6XBKYtm4kUH8PU2z8pC4Oq\nM7YI6xKZsCKdwcJ+EkV2HAFBWyqaY+nnFisDjVM5jCkiwanDnb8UyU4El+Vev/Qi\nW4wdpxz3Zg0Q9Uc2OpHC+FCGRL2nqrqcn05nX1Q+JwblZXT0e7cpcIMmPEOMU4Pk\nG0vXYxLlLgFeszYpYbBBKx/NUZlNuejTznR0dNqge352yQ207AP6pjJHtxQotkyU\nqUuEom8x0bJz1QEhQI+JSEDRhrXESV7b0IHj51BZwQKBgQD5ImWRTpT4PaX66qkh\nCOdVWsdpc/ZBBHI1PEKxfmhbgw3RHcc43jiUDk0f+VOszBGNsTPk+uAOKGNRSvYZ\nrlRPQebTseS8aCcV/Rjig18F5HSirUFsAKhbWxH5uuGis1J/Lb55UnLX6zmUNwOq\nziVLW8eUxeIcxbT8l7B6RQnIsQKBgQDah+rw+AEQep5aqXsDprACfBy5Zl3eI+iJ\nFixOOgWcKgMN7I6kPTAnppdjK1G7quhyS3q4LeFFFwMWYtq9HZYbpFEQn/2D6fjm\noKEtmQ2MIbtqDVauW2WxZ8kREEv5ONQjgGsoM/QbUb8yHtrBluYosEd5v6Xjv9RB\niKaj/6UEmwKBgQCtwIKLq/2TgBNhgwV/x6DnU4+eCUUmpT4tyKBO//UyVZ1uSdFm\n5P0arTq24QGtkwlvA7ZIrXtUBHD4AkrPMFkWicS9weTgTddsq38Og0bjaii6SBFH\njNHeHQ7VV7QD8ALKNhIQtSLpWeFncFL7bhhujU0NglEnde+69uQa8klXkQKBgCRO\nQHIYQdUDChv13EIXB1biV8NVhnLJdHCSBnpYmWYAdNFzY59VqxJrUute3w1Wr5eN\ngq3msW5RDGpDsiOJLs8Y1X71laC81mU6eoygyOdnE0PjQ2tkM9jtbTIwiu60ykm7\npBHhz8RaKHGjPqS69TH9V2KavGzCCfl5QnYsmrXRAoGBAJZeNO+wKc5zfYH9oKQ6\nn7FbpvVU8+973qZvK7a59OHrZnpR71lZ/EsYYC472MIzHkozXaRv+f4ZTE/3aJy6\nIJ6H9ypZtYhTCu6ejmf7Sk2HbzvKkLTOGfD+kfd12gcwFynUum+YzTjYrC/JK4Rh\ndZQOYIMbkqFQf3XomU1XNC+C\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-8v0s8@womens-safety-2022.iam.gserviceaccount.com",
  "client_id": "107467027601937298613",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8v0s8%40womens-safety-2022.iam.gserviceaccount.com"
}
)
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://womens-safety-2022-default-rtdb.firebaseio.com",
  'storageBucket':"womens-safety-2022.appspot.com"
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
        # storage_client = storage.Client.from_service_account_info(credentials_dict)
        bucket = storage.bucket()
        cmd = 'libcamera-vid -t 7000 -o test.h264'
        for i in range(0,10):
            os.system(cmd)
            time.sleep(10)
            command = "MP4Box -add test.h264 test.mp4"
            os.system(command)
            time.sleep(10)
            destination_blob_name = 'video_' + str(time.time()) + '.mp4'
            source_file_name = 'test.mp4'

            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}.".format(
                    source_file_name, destination_blob_name
                )
            )
            os.system('rm test.h264')
            os.system('rm test.mp4')
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





        
