import RPi.GPIO as GPIO
import MFRC522
import signal
import requests
import sys
import RPi.GPIO as GPIO
import time
from RPLCD.gpio import CharLCD
from subprocess import call

continue_reading = True
BeepPin = 7
RIGHT=1
WRONG=0
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_rw=36, pin_e=35, pins_data=[33,31,29,32], numbering_mode=GPIO.BOARD)

santri={
    "18163373": "Achmad Nurjamil",
    "21119513591": "Achmad Pamudji ",
    "1811913273": "Ade Mulyadi    ",
    "175213373":"Ahmad Rohman   ",
    "73113373": "Ajat Sudrajat  ",
    "1991753373": "Ako            ",
    "1315313091": "Asep Maulana I ",
    "2211023373": "Asep Purnama   ",
    "1102173273": "Asep Supriatna ",
    "211693373": "Asmarul Abadi  ",
    "991413373": "Ayi Sumirat    ",
    "11916620320": "Azhar Dzulfikar",
    "3322012991": "Bambang Widiyo ",
    "19815112991": "Beben Muhtadin ",
    "952133373": "Dadan Suhandi  ",
    "1711413691": "Dadan Sukmana  ",
    "871182421": "Dani Kurmina   ",
    "437913091": "Dayat Hidayat  ",
    "46493373": "Dede Koswara   ",
    "2331093373": "Diki Fauzi     ",
    "1211783273": "Eko Puji S     ",
    "1226903484": "Engkus Wiyono  ",
    "522023273": "Eri Ridwan     ",
    "19314013691": "Euis Sumiyati  ",
    "2342033373": "Fajar Pariyanto",
    "2422613691": "Fikri Syahid   ",
    "48883373": "Fitri Yuningsih",
    "2352223273": "Gilang Ramadhan",
    "202313691": "Hari Ardiansyah",
    "182063373": "I Gia Andriana ",
    "67683373": "Iwan Setiawan  ",
    "85473373": "Jumirah        ",
    "1055313691": "Kamal Taufiq   ",
    "792303273": "Kamso H.       ",
    "2531093373": "Lia Mulyani    ",
    "827113691": "M. Saiful Munir",
    "24223613591": "Madyo Sasongko ",
    "1632353273": "Mia Kusmiyati  ",
    "621233373": "Mohamad Khoerun",
    "621973373": "Mulyono        ",
    "1772423273": "Pitrianto      ",
    "9211913691": "Ratna Windari  ",
    "2307813691": "Ratno Wibowo   ",
    "1572173273": "Rina Rusmawati ",
    "201543373": "Rini Karyani   ",
    "1901753373": "Rudiana        ",
    "20293373": "Rudy N. Fahla  ",
    "19419212991": "Sopi Kuswandari",
    "1306113691": "Sopyan Taufik  ",
    "1036324820": "Sukamto (Ato)  ",
    "156523373": "Sukarni        ",
    "602103273": "Sukmarani Pati ",
    "2042203273": "Sumiyati       ",
    "1912323373": "Supo Wahono    ",
    "17321213091": "Supriatna      ",
    "12422712991": "Susi Susilawati",
    "1941873373": "Syarif Hidayat ",
    "372313273": "Taryanto       ",
    "1991113373": "Ujang Nuryana  ",
    "962353273": "Ujang Sudrajat ",
    "212777195": "Usep Wachya    ",
    "602193273": "Yadi Mulyadi   ",
    "14815812991": "Yayan Mulyanto ",
    "17216612991": "Yostian Saputro",
    "2411313373": "Yude Ruhimat   ",
    "3818312991": "Str. Majalengka",
    "99693373": "Hari Mulyawan  ",
    "382173273": "Siti Budiyati  ",
    "1039724920": "Suryana        ",
    "19917724820": "Neni Winarsih  ",
    "877221": "Hisap Mulya    "
}

def clearText(line):
    lcd.cursor_pos = (line, 0)
    lcd.write_string("                ")
    #lcd.cursor_pos = (1, 0)
    #lcd.write_string("                ")

def setText(line, msg):
    clearText(line)
    lcd.cursor_pos = (line, 0)
    lcd.write_string(msg)

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(BeepPin, GPIO.OUT)   # Set BeepPin's mode is output
    #  GPIO.output(BeepPin, GPIO.HIGH) # Set BeepPin high(+3.3V) to turn on led
    GPIO.output(BeepPin, GPIO.HIGH)  # led on
    time.sleep(1)
    GPIO.output(BeepPin, GPIO.LOW) # led off
    # lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_rw=36, pin_e=35, pins_data=[33,31,29,32], numbering_mode=GPIO.BOARD)
    setText(0, u'Siap')


def beep(mode):
    GPIO.output(BeepPin, GPIO.HIGH)  # led on
    time.sleep(0.1)
    GPIO.output(BeepPin, GPIO.LOW) # led off
    if (mode == WRONG):
        time.sleep(0.1)
        GPIO.output(BeepPin, GPIO.HIGH)  # led on
        time.sleep(0.1)
        GPIO.output(BeepPin, GPIO.LOW) # led off


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
def save(uid):
    try:
        r = requests.post('http://' + sys.argv[1] + '/absensi/tap', json={"uid": uid})
        if (r.status_code == 200):
            setText(1, r.json()["message"])
            print("SUCCESS")
            beep(RIGHT)
        else:
            setText(1, r.json()["message"])
            print("FAILED")
            beep(WRONG)
        print(r.json())
    except requests.exceptions.RequestException as e:
        setText(1, "Error")
        print("ERROR")

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

setup()
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
        if strUid == "":
            setText(0, "Shutting down")
            setText(1, "Bye!")
            beep(WRONG)
            time.sleep(2)
            setText(0, "")
            setText(1, "")
            call("sudo shutdown -h now", shell=True)
        else:
            # Print UID
            if strUid in santri.keys():
                setText(0, santri[strUid])
                print ("Card read UID: " + strUid)
                save(strUid)
            else:
                setText(0, strUid)
                setText(1, u"Tidak Dikenal")
                beep(WRONG)