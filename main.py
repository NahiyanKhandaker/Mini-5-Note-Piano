import machine
import utime
import math

KEYS = (
    (0, 1, 262),    # C4
    (4, 5, 294),    # D4
    (8, 9, 330),    # E4
    (10, 11, 392),  # G4
    (12, 13, 440),  # A4
)

DECAY_MS = 200   # how long a released key's LED takes to fade out
IDLE_MS = 4000   # how long idle before the breathing glow starts

keys = []
for btn_pin, led_pin, note in KEYS:
    button = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_UP)
    led = machine.PWM(machine.Pin(led_pin))
    led.freq(1000)
    led.duty_u16(0)
    keys.append({"button": button, "led": led, "note": note, "released_at": None})

buzzer = machine.PWM(machine.Pin(14))
buzzer.duty_u16(0)

last_active = utime.ticks_ms()

while True:
    now = utime.ticks_ms()
    any_held = False
    current_note = None

    for key in keys:
        if key["button"].value() == 0:
            key["led"].duty_u16(65535)
            key["released_at"] = None
            any_held = True
            current_note = key["note"]
            last_active = now
        elif key["released_at"] is None:
            key["released_at"] = now
        else:
            elapsed = utime.ticks_diff(now, key["released_at"])
            fraction = max(0, 1 - elapsed / DECAY_MS)
            key["led"].duty_u16(int(fraction * 65535))

    if any_held:
        buzzer.freq(current_note)
        buzzer.duty_u16(25000)
    else:
        buzzer.duty_u16(0)
        if utime.ticks_diff(now, last_active) > IDLE_MS:
            brightness = (math.sin(now / 600) + 1) / 2
            for key in keys:
                fully_decayed = (
                    key["released_at"] is not None
                    and utime.ticks_diff(now, key["released_at"]) > DECAY_MS
                )
                if fully_decayed:
                    key["led"].duty_u16(int(brightness * 15000))

    utime.sleep_ms(5)
