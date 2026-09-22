# Maintainer notes

## Scope and provenance

This is a separate `usb-ptt-handset` repository prepared for the completed module-based hardware build, with the README serving as the main assembly guide. It has not been published to GitHub.

- `firmware/code.py` is the recovered current file, preserved byte-for-byte. Its bindings are F13 and Ctrl+Space, with external input pull-ups enabled electrically and internal pull-ups disabled in software.
- The SVG and PNG are the original recovered wiring diagram and its export. Their optional 9 V amplifier annotation is retained; the README documents the simpler 5 V build and clarifies functional USB power labels.
- `hardware/testing/` contains new, not-to-scale probe-placement diagrams for the two QHM22D resistance checks. Each is supplied as editable SVG and a PNG export, with the same contact pairs and expected readings as the testing table. Both exports were visually inspected.
- The earlier `kb2040-setup.md` described older F14/Space settings. Its useful installation/serial instructions were rewritten to agree with the current firmware.
- Prototype audio and repair results are the builder's previously reported observations. Repository preparation did not include new physical testing of the hardware.
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

Photos are unaltered copies under descriptive filenames. `IMG_8585.jpeg` (the Amazon screenshot) is excluded as requested. `IMG_8639.jpeg` is unused because its terminal screen includes unrelated project details; the Cabin Fever photo provides the application view.

## Remaining details for a public release

1. The `enclosure/` folder includes the body, lid, and mounting plate/standoff STLs, plus a Bambu Lab P1S 3MF project. See [enclosure notes](enclosure.md). Editable source CAD and exact fastener specifications remain to be documented.
2. Record the final USB audio adapter and connector/cable SKUs. The BOM already gives functional requirements and labels the earlier audio-adapter reference accurately.
3. Record the final working Claude Code / Windows Terminal / Teams configuration, including versions. Do not promote the Ctrl+Space example to a tested recipe without verifying press, hold, and release.
4. Choose licenses for firmware, documentation, photographs, and any future hardware/CAD files before advertising the repository as open source. No license grant has been invented here.

The physical pin mapping and main build sequence are complete; these outstanding details affect exact sourcing, enclosure reproduction, and distribution terms.
