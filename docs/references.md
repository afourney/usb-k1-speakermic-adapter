# References and evidence

[Back to the build guide](../README.md)

Links checked while preparing this repository on September 22, 2026. The source notes distinguish a reported defect from verified electrical requirements and this prototype's own observations.

## QHM22D wiring reversal

| Source | What it establishes |
| --- | --- |
| [Amazon customer review RETJVNP2EQFWO](https://www.amazon.com/gp/customer-reviews/RETJVNP2EQFWO) | The supplied screenshot identifies a September 4, 2022 review titled “repair the factory defect and then it works great.” It describes swapping reversed speaker leads to restore operation with external headphones. Direct Amazon retrieval failed during preparation; the exact permalink is independently linked by the Reddit thread below. The screenshot is not included. |
| [Comms at Home, QHM22D question](https://www.reddit.com/r/Baofeng/comments/123nzs1/comms_at_home_qhm22d_question/) | Independent owner describes PTT failure with an external headset, receives the Amazon repair link, and reports success after soldering the repair. Other comments suggest different causes, so this supports testing a unit rather than assuming a universal defect. |
| [Earlier QHM22D headset/PTT report](https://www.reddit.com/r/Baofeng/comments/lg8wdt/help_baofeng_qhm22d_dual_ptt_speaker_mic_stops/) | Related first-hand discussion, but the original post is deleted. Limited corroboration of the symptom, not confirmation of the yellow/brown fault. |
| [BTECH QHM22D product page and customer reviews](https://baofengtech.com/product/qhm22d/#reviews) | Product identity and Adam Fourney's September 8, 2026 account of the same photographed unit. It records the approximately 0 Ω/8 Ω readings and repair; it is not an independent sample or a manufacturer defect notice. |
| [Before photograph](images/qhm22d-before.jpg) / [after photograph](images/qhm22d-after.jpg) | Original photos of this build: cable-entry SP− changes yellow → brown; SP+ changes brown → yellow. The board is marked QHM22 V1.7, 2020-04-07. |

## Hardware and firmware

| Source | Use |
| --- | --- |
| [Miklor technical diagrams](https://www.miklor.com/COM/UV_Technical.php) | K1 speaker/microphone contact assignments and sleeve-to-sleeve PTT, with separate dual-PTT drawings. Background for interpreting measurements, not evidence of a BTECH manufacturing defect. |
| [Adafruit KB2040 product](https://www.adafruit.com/product/5302) and [pinout](https://learn.adafruit.com/adafruit-kb2040/pinouts) | Board identity, D2/D3, regulated 3V, BOOT input, USB data pads, and power-path distinctions. |
| [CH334F hub product](https://www.adafruit.com/product/5999) and [pinout](https://learn.adafruit.com/adafruit-ch334f-mini-4-port-usb-hub-breakout/pinouts) | Two downstream USB connections and their wiring. The shared guide covers both 2-port and 4-port boards. |
| [Adafruit USB audio adapter 1475](https://www.adafruit.com/product/1475) | Reference part linked during planning. This does not identify the exact cabled adapter visible in the final photos. |
| [ProtoSupplies LM386 module](https://protosupplies.com/product/lm386-audio-amplifier-module/) | Module source discussed during the build. The earlier product description specified an LM386M-1, 4–12 V operation, input trimmer, and 200× gain. Live retrieval returned HTTP 403 during preparation. |
| [TI LM386 datasheet](https://www.ti.com/lit/ds/symlink/lm386.pdf) | Gain-setting principle and output coupling requirement. It does not assign the module-specific reference designator R1. |
| [CircuitPython for KB2040](https://circuitpython.org/board/adafruit_kb2040/) and [library bundle](https://circuitpython.org/libraries) | Runtime and `adafruit_hid` installation. |
| [W3C Keyboard Event Viewer](https://w3c.github.io/uievents/tools/key-event-viewer.html) | Host-side inspection of keydown and keyup events. |

## K1 accessory diagram sources

The [README pinout section](../README.md#k1-accessory-pinout) embeds the [PNG](../hardware/k1-accessory-pinout.png) and links the [editable SVG](../hardware/k1-accessory-pinout.svg).

- [Original SVG, The (Chinese) Radio Documentation Project](https://github.com/radiodoc/uv-5r/blob/master/assets/images/kenwood-2pin-headset.svg), from the [UV-5R manual](https://radiodoc.github.io/uv-5r/). The adapted PNG and SVG retain [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Changes: removed +5 V, added cyan secondary PTT, revised labels and captions.
- [Miklor UV-82 dual-PTT instructions](https://www.miklor.com/COM/UV_Technical.php), [connector photograph](https://www.miklor.com/COM/images/dualPTT.jpg), and [Walt N3PLA circuit](https://www.miklor.com/COM/images/dualPTT-N3PLA.jpg): main PTT switches the 3.5 mm sleeve to the 2.5 mm sleeve; secondary PTT switches the 3.5 mm tip to that same ground.
- [Kenwood TH-F6A/TH-F7E manual, printed page 45](https://kasc.kenwood.com/files/images/products/product_id_268/file_category_10/TH-F6A_F7E_inst.pdf#page=50): conventional main-PTT and audio contacts; this model uses the 3.5 mm tip for 3.5 V, not secondary PTT.
- [UV-82HP manual, printed page 19](https://baofengtech.com/wp-content/uploads/2020/09/UV82HP_Manual_ReducedSize.pdf#page=26): upper/lower-channel PTT operation. Its accessory illustration is a generic single-PTT drawing, not evidence for the secondary-PTT pin assignment.

## Applications

- [Cabin Fever x86](https://github.com/afourney/cabin-fever-x86): companion game; consult its current controls for the PTT binding.
- [Claude Code voice dictation](https://code.claude.com/docs/en/voice-dictation) and [keyboard shortcuts](https://code.claude.com/docs/en/keybindings): `/voice hold`, the `Chat` context, and the `voice:pushToTalk` action. The repository's Ctrl+Space example has not been established as working in the original Windows Terminal/WSL2 setup.
- Teams guidance is intentionally conditional on the installed client's shortcut list. A current official Teams page could not be retrieved during preparation; there is no claim of a verified universal Teams/Claude binding.
