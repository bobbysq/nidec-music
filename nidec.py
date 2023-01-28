# Example using PWM to fade an LED.

import time
from machine import Pin, PWM


# Construct PWM object, with LED on Pin(25).
power = PWM(Pin(19))
converted_power = 0
percent_power = 50

# Set the PWM frequency.
# power.freq(2500)
power.freq(15625)

converted_power = 65535 * (50 / 100.0)

print(converted_power)

power.duty_u16(int(converted_power))

while True:
    # percent_power = input('Input a power (0-100, 50 = neutral): ')
    # converted_power = 65535 * (int(percent_power) / 100.0)
    # power.duty_u16(int(converted_power))
    new_freq = input('Input frequency: ')
    power.freq(int(new_freq))