from core.API import API
import RPi.GPIO as GPIO
import time

class BuzzerAPI(API):
	def setup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)

	def post():
		try:
			while True:
			    GPIO.output(18, True)
			    time.sleep(1/5)
			    GPIO.output(18, False)
		except KeyboardInterrupt:
			GPIO.cleanup()