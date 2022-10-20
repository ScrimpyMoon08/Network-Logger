from scapy.all import *
from scapy.sendrecv import sniff
import pyrebase
from helper.FlowRecoder import get_data, gen_json
import time
# net start npcap  <- if windows user to enable monitor mode

### THIS PYTHON FILE SHOULD INSTALL INSIDE RPI


config = {
    "apiKey": "AIzaSyAmbZSRs7INBAYZZD93zlfxs3OEI9bM5Kw",
    "authDomain": "anomaly-detection-db.firebaseapp.com",
    "databaseURL": "https://anomaly-detection-db-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "anomaly-detection-db",
    "storageBucket": "anomaly-detection-db.appspot.com",
    "messagingSenderId": "173477063235",
    "appId": "1:173477063235:web:86a7d4423578b78394c2f6"
};

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
database = firebase.database()


def main():
    sleep_interval = 1
    print("Setting up device...");
    while True:
        captured_buffer = []
        isActive = eval(database.child("Network-Active").get().val())
        database.child("Network-Connection").set("Connected")
        if isActive == True:
            for pkt in sniff(iface=conf.iface, count=40):
                captured_buffer.append(pkt)
            data = get_data(captured_buffer)
            data = gen_json(data)
            database.child("Network-Traffic").set(data)
            database.child("Network-Active").set("True")
            print(captured_buffer)
        time.sleep(sleep_interval)



if __name__ == '__main__':
    try:
        main()
    finally:
        print("Terminating the program")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
