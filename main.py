import machine
import utime

NOTES = (262, 294, 330, 392, 440)  # C4 D4 E4 G4 A4
BTN_PINS = (0, 4, 8, 10, 12)
LED_PINS = (1, 5, 9, 11, 13)

buttons = [machine.Pin(p, machine.Pin.IN, machine.Pin.PULL_UP) for p in BTN_PINS]
leds = [machine.Pin(p, machine.Pin.OUT) for p in LED_PINS]
buzzer = machine.PWM(machine.Pin(14))
buzzer.duty_u16(0)

while True:
    any_pressed = False
    for i, btn in enumerate(buttons):
        if btn.value() == 0:
            leds[i].on()
            buzzer.freq(NOTES[i])
            buzzer.duty_u16(25000)
            any_pressed = True
        else:
            leds[i].off()
    if not any_pressed:
        buzzer.duty_u16(0)
    utime.sleep_ms(5)