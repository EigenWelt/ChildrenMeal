import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
self_SCK = 29
self_DT = 31
self_flag = 1
self_initweight = 100
self_weight = 0
self_delay = 0.89
GPIO.setmode(GPIO.BOARD)
GPIO.setup(self_SCK,GPIO.OUT)
GPIO.setup(self_DT,GPIO.IN)

GPIO.output(self_SCK,0)

while(1):
    value = 0
    time.sleep(self_delay)
    for i in range(24):
        GPIO.output(self_SCK,1)
        if(0==GPIO.input(self_SCK)):
            time.sleep(self_delay)
        value = value<<1
        GPIO.output(self_SCK,0)
        if GPIO.input(self_DT)==1:
            value = value+1
    GPIO.output(self_SCK,1)
    GPIO.output(self_SCK,0)
    time.sleep(self_delay)
    if self_flag == 1:
        self_flag = 0
        self_initweight = value
    else:
        self_weight = abs(value-self_initweight)
    print(self_weight/1900)
