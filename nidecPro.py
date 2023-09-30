import time
from machine import Pin, PWM
from chrpy import chrpy

# Construct PWM object
power = PWM(Pin(19))
enable = Pin(17, Pin.OUT)
led = Pin(25, Pin.OUT)
converted_power = 0
percent_power = 50

# Set the PWM frequency.
power.freq(2500)
# power.freq(15625)

converted_power = 65535 * (50 / 100.0) # Set power to 50%

# print(converted_power)

power.duty_u16(int(converted_power))

def beep(hz, duration):
    power.freq(hz)
    time.sleep_ms(duration)

def play_song(song):
    for note in song:
        if note[0] == -1:
            enable.high()
            time.sleep_ms(note[1])
            enable.low()
        else:
            beep(note[0],note[1])

def play_chrp(file, track):
    chrp_song = chrpy.from_file(file)

    chrp_track = chrp_song.tracks[track]

    start_tick = time.ticks_ms()
    for note in chrp_track:
        while time.ticks_diff(time.ticks_ms(), start_tick) < note.off:
            enable.high()
            if time.ticks_diff(time.ticks_ms(), start_tick) < note.on:
                enable.low()
                beep(note.note, note.off - note.on)



enable.low()
led.high()

try:
    play_song(None)
except KeyboardInterrupt:
    print("Cancelled playback!")

print("song finished")

enable.high()
led.low()