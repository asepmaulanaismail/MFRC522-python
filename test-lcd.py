from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,32], numbering_mode=GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

GPIO.setup(32, GPIO.OUT)
GPIO.output(32, GPIO.HIGH)

GPIO.setup(38, GPIO.OUT)
GPIO.output(38, GPIO.LOW)
lcd.write_string('Asep M')

#GPIO.cleanup()
