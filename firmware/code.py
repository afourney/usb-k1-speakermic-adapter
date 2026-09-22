"""KB2040 USB PTT: D2 or BOOT holds F13; D3 holds Ctrl+Space.

Copy to CIRCUITPY/code.py. Install adafruit_hid in CIRCUITPY/lib.
D2/D3 require external pull-ups to 3.3V with the default settings below.
"""

import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


PTT1_KEY = Keycode.F13
PTT2_KEY = (Keycode.LEFT_CONTROL, Keycode.SPACE)
BOOT_ALIASES_PTT1 = True
USE_INTERNAL_PULLUPS = False  # External 10k pull-ups on D2/D3.
DEBOUNCE_SECONDS = 0.020
POLL_SECONDS = 0.002
LOG_CHANGES = True


def binding_keys(binding):
    return (binding,) if isinstance(binding, int) else tuple(binding)


class Button:
    def __init__(self, pin, key, pull_up):
        self.io = digitalio.DigitalInOut(pin)
        self.io.switch_to_input(pull=digitalio.Pull.UP if pull_up else None)
        self.keys = binding_keys(key)
        self.pressed = False
        self.candidate = not self.io.value
        self.changed_at = time.monotonic()

    def update(self, now):
        sample = not self.io.value
        if sample != self.candidate:
            self.candidate = sample
            self.changed_at = now
        if now - self.changed_at >= DEBOUNCE_SECONDS:
            self.pressed = self.candidate


def main():
    buttons = [
        Button(board.D2, PTT1_KEY, USE_INTERNAL_PULLUPS),
        Button(board.D3, PTT2_KEY, USE_INTERNAL_PULLUPS),
    ]
    if BOOT_ALIASES_PTT1:
        buttons.append(Button(board.BUTTON, PTT1_KEY, True))

    keyboard = Keyboard(usb_hid.devices)
    sent = None
    print("PTT ready.")

    try:
        while True:
            now = time.monotonic()
            for button in buttons:
                button.update(now)

            # Combine aliases before sending releases: either source can hold F13.
            desired = {
                key for button in buttons if button.pressed for key in button.keys
            }
            try:
                if sent is None:
                    keyboard.release_all()
                    sent = set()
                released = sent - desired
                pressed = desired - sent
                if released:
                    keyboard.release(*released)
                if pressed:
                    keyboard.press(*pressed)
                if LOG_CHANGES and desired != sent:
                    print(
                        "PTT1:",
                        "DOWN" if all(k in desired for k in binding_keys(PTT1_KEY)) else "up",
                        "PTT2:",
                        "DOWN" if all(k in desired for k in binding_keys(PTT2_KEY)) else "up",
                    )
                sent = desired
            except OSError:
                # Resynchronize the complete held state when USB is available again.
                sent = None
                time.sleep(0.100)

            time.sleep(POLL_SECONDS)
    finally:
        try:
            keyboard.release_all()
        except OSError:
            pass
        for button in buttons:
            button.io.deinit()


if __name__ == "__main__":
    main()
