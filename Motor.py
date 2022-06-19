from machine import Pin
from time import sleep


class Motor:
    def __init__(self, step_pin, dir_pin, pin_m0, pin_m1, pin_m2, step_type):
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.pin_m0 = Pin(pin_m0, Pin.OUT)
        self.pin_m1 = Pin(pin_m1, Pin.OUT)
        self.pin_m2 = Pin(pin_m2, Pin.OUT)



        resolution = {'Full': (0, 0, 0),
                      'Half': (1, 0, 0),
                      '1/4': (0, 1, 0),
                      '1/8': (1, 1, 0),
                      '1/16': (0, 0, 1),
                      '1/32': (1, 0, 1)}
        microsteps = {'Full': 1,
                      'Half': 2,
                      '1/4': 4,
                      '1/8': 8,
                      '1/16': 16,
                      '1/32': 32}
        self.delay = .005 / microsteps[step_type]
        self.pin_m0.off()
        self.pin_m1.off()
        self.pin_m2.off()

        # self.mode_pins.write(resolution[step_type])

    def run(self, steps, clockwise):
        if clockwise:
            self.dir_pin.on()
        else:
            self.dir_pin.off()

        for i in range(steps):
            self.step_pin.on()
            sleep(self.delay)
            self.step_pin.off()
            sleep(self.delay)
