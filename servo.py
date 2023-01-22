import RPi.GPIO as GPIO
from time import sleep



class Servo():

    servo : GPIO.PWM = None

    def __init__(self, pinNo) -> None:        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinNo, GPIO.OUT)
        self.servo = GPIO.PWM(pinNo,50)
        self.servo.start(0)
        pass
    
    def turnLeft(self, howLongMS):
        self.servo.ChangeDutyCycle(7)

    def turnRight(self, howLongMS):
        self.servo.ChangeDutyCycle(8)

    def hold(self):
        self.servo.ChangeDutyCycle(7.5)

    def wave(self):
        for i in range (40,150,1):
            self.servo.ChangeDutyCycle(i/10)
            print(str(i/10)+"\n")
            sleep(0.5)

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()
        print("Cleanup complete")