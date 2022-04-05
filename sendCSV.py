import firebase_admin
from firebase_admin import db
import csv

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
        ref.set({"heartrate": rows[0],
            "oxygen": rows[1]
            })
        
