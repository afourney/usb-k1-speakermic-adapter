# Maintainer notes

## Repository contents

This repository documents the USB K1 speaker-mic adapter, with the README serving as the main assembly guide.

- `firmware/code.py` supplies the button firmware. Its bindings are F13 and Ctrl+Space, with external input pull-ups enabled electrically and internal pull-ups disabled in software.
- The wiring diagram is supplied as SVG and PNG. It includes an optional 9 V amplifier annotation; the README documents the USB 5 V build and explains the USB power labels.
- `hardware/testing/` contains not-to-scale probe-placement diagrams for the two QHM22D resistance checks. Each is supplied as editable SVG and a PNG export, with the same contact pairs and expected readings as the testing table. Both exports were visually inspected.
- Firmware installation is covered in the README, with serial-console instructions in `docs/serial-console.md`.
- Prototype audio and repair results are the builder's reported observations.
- Firmware validation covers Python syntax and simulated debounce, held-key overlap, chord release, and recovery after a USB send error. It does not replace testing on CircuitPython and actual USB hosts.

## Photo inventory

| Repository file | Original upload | Use |
| --- | --- | --- |
| `cabin-fever-demo.jpg` | `IMG_8638.jpeg` | README hero |
| `finished-handset.jpg` | `IMG_8634.jpeg` | Complete assembly |
| `assembly.jpg` | `IMG_8630.jpeg` | Module layout |
| `enclosure-open.jpg` | `IMG_8631.jpeg` | Internal mounting |
| `enclosure-front.jpg` | `IMG_8636.jpeg` | Cable entry |
| `qhm22d-before.jpg` | `IMG_8586(1).jpeg` | Factory reversal |
| `qhm22d-after.jpg` | `IMG_8587.jpeg` | Repaired cable pads |

Photos are unaltered copies under descriptive filenames. `IMG_8585.jpeg` (the Amazon screenshot) is excluded. `IMG_8639.jpeg` is unused because its terminal screen includes unrelated project details; the Cabin Fever photo provides the application view.

## Documentation gaps

1. The `enclosure/` folder includes the body, lid, and mounting plate/standoff STLs, plus a Bambu Lab P1S 3MF project. See [enclosure notes](enclosure.md). Editable source CAD and exact fastener specifications remain to be documented.
2. Record the final USB audio adapter and connector/cable SKUs. The BOM gives functional requirements and a reference audio adapter.
3. Record the final working Claude Code / Windows Terminal / Teams configuration, including versions. Do not promote the Ctrl+Space example to a tested recipe without verifying press, hold, and release.

## License

The repository uses the [MIT License](../LICENSE), except for the adapted K1 accessory diagram, which retains its CC BY-SA 3.0 license. See the [README attribution](../README.md#k1-diagram-sources).
