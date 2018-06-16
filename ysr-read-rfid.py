import RPi.GPIO as GPIO
import MFRC522
import signal
import requests

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
def save(uid):
    try:
        r = requests.post('http://128.199.82.144:1506/absensi/tap', json={"uid": uid})
        if (r.status_code == 200):
            print("SUCCESS")
        else:
            print("FAILED")
        print(r.json()["message"])
    except requests.exceptions.RequestException as e:
        print(e)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        strUid = ("".join(str(uid[x]) for x in range(0, len(uid)-1)))
        # Print UID
        print ("Card read UID: " + strUid)
        save(strUid)

