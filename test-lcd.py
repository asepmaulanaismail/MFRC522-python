from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_rw=36, pin_e=35, pins_data=[33,31,29,32], numbering_mode=GPIO.BOARD)
lcd.write_string(u'HELLO')
GPIO.cleanup()
