# Serial console and firmware troubleshooting

[Back to the build guide](../README.md)

The KB2040's CircuitPython console prints button changes and Python errors. It uses USB serial independently of the audio and HID keyboard interfaces.

## Connect on Windows

1. Start the board normally, without holding BOOT. `CIRCUITPY` should be visible.
2. Open **Device Manager → Ports (COM & LPT)**. Identify the USB serial port by unplugging/reconnecting the board after pending writes finish. `COM7` was used during development; use the port actually shown on your computer.
3. Open [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
4. On the **Session** page, choose the **Serial** connection-type radio button. Selecting “Serial” in the left navigation alone does not change the connection type.
5. Enter the COM port and speed **115200**. Under **Connection → Serial**, select 8 data bits, 1 stop bit, no parity, and **no flow control**.
6. Click **Open**. Close any other program that already owns that serial port.

If PuTTY is on PATH, the equivalent Windows command is:

```bat
putty.exe -serial COM7 -sercfg 115200,8,n,1,N
```

## Read the output

An initially blank console is normal: earlier log messages are not replayed. Press a handset button, or press **Ctrl+C**, then Enter if prompted, to reach the `>>>` REPL. **Ctrl+D** restarts the program and shows its startup message or traceback.

With the supplied firmware, normal output looks like:

```text
PTT ready.
PTT1: DOWN PTT2: up
PTT1: up PTT2: up
PTT1: up PTT2: DOWN
PTT1: up PTT2: up
```

Ctrl+C stops the PTT program until Ctrl+D or reset. A resulting `KeyboardInterrupt` is expected. These labels reflect the configured held keys; use a host keyboard-event viewer to verify the actual HID behavior.

## Common failures

| Failure | Resolution |
| --- | --- |
| `ImportError` for `adafruit_hid` | Copy the whole matching bundle folder to `CIRCUITPY/lib/adafruit_hid/`. |
| Syntax error after editing | Check indentation and the exact names `Keycode.SPACE` and `Keycode.LEFT_CONTROL`. |
| Wrong pin names | This file targets KB2040. Other RP2040 boards require different CircuitPython firmware and possibly different `board` names. |
| Only `RPI-RP2` appears | This is the UF2 bootloader. Install CircuitPython or restart without holding BOOT. |
| Access denied opening COM port | Close other serial monitors and verify the current COM number. |
| PuTTY beeps instead of opening the console | Select the Serial radio button on the Session page. |
| PuTTY beeps when pressing the PTT button | The HID keystroke may be going to PuTTY. Focus the browser key-event viewer while testing keys. |

During an unsoldered bench test, set `USE_INTERNAL_PULLUPS = True`; in the assembled build use the two external 10 kΩ pull-ups and the shipped `False` setting. BOOT always uses its own internal pull-up.

## Updating the program

Back up an existing program before replacing it. Edit `CIRCUITPY/code.py` as UTF-8 plain text. Saving normally triggers a reload. Installing a new runtime UF2 is unnecessary for ordinary keybinding changes.

References: [KB2040 CircuitPython installation](https://learn.adafruit.com/adafruit-kb2040/circuitpython), [CircuitPython libraries](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries), and [PuTTY serial documentation](https://the.earth.li/~sgtatham/putty/0.83/htmldoc/Chapter3.html#using-serial).
