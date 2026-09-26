# K1 Carrier - Revision C (80 x 80 mm)

Open `kicad/k1-carrier-rev-c.kicad_pro` in KiCad 10. This is a standalone snapshot of the 80 x 80 mm, two-layer Revision C engineering project. Earlier revisions are not needed or included. See `PROJECT-SNAPSHOT.md` for package contents and Git tracking notes. Connector assignments are unchanged from Revision B; the modules and mounting holes have been repositioned for the smaller outline.

KiCad 10.0.6 checks: 0 ERC violations, 0 DRC violations, 0 unconnected pads, and 0 schematic-parity issues. Reports are saved in `preview/`. The schematic and assembly previews accompany the editable project. These checks do not replace the prototype release checks below.

## Connector Configuration (Retained From Revision B)

| Reference | Assignment |
|---|---|
| J1 | Board-mounted USB-A receptacle, Molex 67643-0910, replacing the USB wire pads |
| J2 | Sound-card microphone pigtail, moved to the right perimeter |
| J3 | Sound-card headphone-left pigtail, beside J2 |
| J4 | Six-circuit, right-angle Micro-Fit 3.0 header, Molex 43045-0600, replacing both K1 pigtail connectors |
| J5 | Retired; its K1 contacts are now in J4 |
| J6 | One 1x4, 2.54 mm interface: VCC, IN, GND, GND, replacing separate amplifier power and input connections |
| J7 | Retired; its audio input is now J6 pin 2 |
| J8 | LM386 capacitor-coupled output and optional ground, located to the left of R1/R2 |

The two PTT pull-ups remain 10 kohm to the **KB2040 3V / 3.3 V output**, not USB 5 V. Both switches continue to pull D2/D3 to common ground. Existing firmware assignments are preserved.

## Placement

The CH334F module's USB-C socket faces the top edge. The KB2040 sits below and to its right. The USB-A receptacle faces the right edge, with both sound-card audio pigtails below it. The Micro-Fit faces the bottom edge. The LM386 lies horizontally in the lower mounting area, with the combined input/power harness to its left. J8 sits above the amplifier, to the left of R1/R2. The amplifier outline has moved 8 mm right, leaving 10.5 mm from the J6 pad centerline to the module's left edge.

The USB-A socket is intended to face an **internal enclosure bay**, not necessarily an external wall. Allow room to the right of the carrier for the complete sound adapter, its plugs and cable bends. A short USB extension can relocate the adapter. No sound-card body dimensions are assumed. The enclosure footprint will need clearance beyond the carrier's 80 x 80 mm outline.

Leave clearance below J4 for its mating housing, wires and latch release. The Micro-Fit is not a panel-mount connector; strain-relieve the K1 harness at the enclosure. The LM386 mounting area is for electrically insulating double-sided foam mounting tape, not direct metal-to-PCB contact. Choose sufficient thickness to keep underside solder joints clear of the carrier, and check adhesion and temperature suitability on the actual module. The four amplifier tie-down holes have been removed; the four enclosure mounting holes remain.

The upper-right mounting hole is inset to clear the USB-A body. Relative to the board's upper-left corner, the four enclosure mounting holes are at (4,4), (58,4), (4,76), and (76,76) mm. J4 pin 6 and U2 pin 4 use solid ground-plane connections rather than thermal spokes.

## Connections

### J4: Entire K1 Harness

Use Molex **43025-0600** six-circuit receptacle housing and suitable Micro-Fit female crimp contacts/pre-crimped leads. Select contacts for the actual wire gauge and insulation diameter. Read the numbered cavities: the cable mating view and PCB top view are mirrored. Do not infer numbering from wire colours or the order in a photograph.

| Pin | K1 contact | Signal |
|---:|---|---|
| 1 | 3.5 mm tip | PTT2 / D3 |
| 2 | 3.5 mm ring | Microphone |
| 3 | 3.5 mm sleeve | PTT1 / D2; NOT ground |
| 4 | 2.5 mm tip | Speaker |
| 5 | 2.5 mm ring | Unconnected on carrier; may be left unpopulated |
| 6 | 2.5 mm sleeve | Common ground |

### J6: LM386 Input Harness

| Pin | Carrier signal | Module marking |
|---:|---|---|
| 1 | USB 5 V | VCC / VDD |
| 2 | Sound-card headphone left | IN |
| 3 | Common ground | GND |
| 4 | Common ground | GND |

This is a **single-row 2.54 mm pitch** connector/pad pattern, suitable for a four-position female jumper housing or soldered short ribbon wires. It is not a 2x2 IDC connector. The footprint is unshrouded, so check pin 1 before connecting power. Fit a standard male header to the carrier if using a detachable harness.

J6 is alongside the amplifier's left/input end. Its four-pad row is centered across the nominal 14 mm module width so the harness can run straight across. Pin 1 is at board-relative (3.5, 61.19) mm, with subsequent pins spaced 2.54 mm downwards. This is nominal alignment of a flexible harness, not a verified rigid board-to-board mating footprint. The legend is above the amplifier area and remains visible after mounting.

ProtoSupplies' connection photograph and schematic confirm the VCC/IN/GND/GND order and the shared grounds. The 2.54 mm pitch is corroborated by a matching-style module listing, not a dimensioned drawing of the exact purchased board. Confirm 7.62 mm from the first to fourth pin on the actual module before selecting a rigid mating connector. Keep this harness short. Both ground conductors may be connected; they do not represent isolated analog and power grounds.

### J8: LM386 Output

Pin 1 receives the module's capacitor-coupled OUT terminal. Pin 2 is common ground and may be left unwired: the amplifier is already grounded through J6, and J4 pin 6 has its own carrier-ground connection. No downstream connection relies on an external wire at J8 pin 2. Never connect an uncoupled LM386 IC output directly to the speaker.

### J1, J2 and J3: Sound Card

J1 USB-A: pin 1 = 5 V, 2 = D-, 3 = D+, 4 = ground. Both shell mounting tabs are bonded to common ground. The socket uses the installed KiCad library footprint for the Molex 67643 family; the selected BOM part is 67643-0910.

J2: pin 1 = microphone signal, pin 2 = ground. Identify the actual mic-bias contact of the selected sound card before wiring its male 3.5 mm plug.

J3: pin 1 = headphone LEFT (3.5 mm tip), pin 2 = ground (sleeve). Leave the right-channel ring disconnected. Enable mono output at the host if needed. The USB-A socket and the two pigtails together permit removing the sound adapter without cutting wires.

## Changed Parts

- J1: Molex **67643-0910**, right-angle through-hole USB-A receptacle.
- J4: Molex **43045-0600**, right-angle 2x3 Micro-Fit 3.0 PCB header with plastic locating peg.
- Mating J4 harness: Molex **43025-0600** housing plus six appropriate female contacts, or five if the unused cavity is unpopulated.
- J6: 1x4, 2.54 mm male header and matching four-position cable housing, or direct wires.
- J2, J3 and J8: 1x2, 2.54 mm solder pads/optional headers.
- U1: Adafruit KB2040 5302 with 2x 1x13 headers/sockets, including its extra USB data pads.
- U2: Adafruit CH334F Mini 2-Port Hub 5999 with 2x 1x4 headers/sockets. The four-port model is not interchangeable.
- R1/R2: 10 kohm, 1/4 W axial, 7.62 mm lead spacing.

## Prototype Status

### 3D Preview

Revision C includes local KiCad library STEP models for the two 1x13 KB2040 female sockets, two 1x4 hub female sockets, and both axial resistors. These are generic nominal parts, not selected socket manufacturer models. The library models retain the KiCad library license noted below. J4 now uses the manufacturer model `models/430450600.stp`, supplied by the user from Molex's 430450600 STEP archive, replacing the approximate placeholder. The model is rotated and offset to align its solder tails and locating peg with the footprint. Manufacturer CAD remains subject to Molex's terms. The mating cable housing, daughterboards, amplifier and loose wiring are not modeled. Optional headers on solder-wire connections are not populated in this preview. Confirm actual assembly clearances before fabrication.

Run `add_models.py` with KiCad Python to reapply models without changing routing; the main build also applies them. Reopen the saved PCB and its 3D viewer to refresh an already-open view.

This revision implements the connector and placement changes. It is **not a fabrication release** and does not include ordering Gerbers. As in Revision A, the USB routing is not a validated impedance-controlled differential-pair layout; it requires review against the chosen stackup and exact audio adapter. A clean KiCad DRC does not establish USB signal integrity, electrical noise performance or mechanical fit.

Before fabrication, confirm the amplifier connector pitch, socket stack heights, Micro-Fit mating/latch space, the audio adapter's full envelope and USB speed, and the enclosure dimensions. Check aggregate USB current and inrush with the amplifier load; the amplifier does not independently enumerate. The carrier adds no dedicated ESD protection to the exposed audio/PTT interfaces.

Power only through the hub USB-C. Do not connect another USB cable to the installed KB2040; remove it for independent programming, or program through the hub. Do not apply 9 V. Retain the original module's common-ground/capacitor-coupled amplifier arrangement and verify its gain modification to 20x before assembly.

The module symbols use passive interface pins. ERC checks connectivity but does not model internal regulators, audio behaviour, USB negotiation, or supply load. Read the final reports in `preview/` for the checks actually performed.

## References and Licenses

- Original adapter: https://github.com/afourney/usb-k1-speakermic-adapter
- KB2040 manufacturer CAD: https://github.com/adafruit/Adafruit-KB2040-PCB
- CH334F manufacturer CAD: https://github.com/adafruit/Adafruit-CH334F-Breakout-PCB
- Amplifier connections: https://protosupplies.com/wp-content/uploads/2018/12/LM386-Audio-Amplifier-Module-Connections.jpg
- Amplifier schematic: https://protosupplies.com/wp-content/uploads/2018/12/LM386-Audio-Amplifier-Module-Schematic.jpg
- Matching-style module pitch: https://fluxworkshop.com/products/bjaa100037-lm386-200x-gain-amplifier-lc-blue
- Micro-Fit drawing: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/430/43045/430450600_sd.pdf
- Cable housing: https://www.molex.com/en-us/products/part-detail/430250600
- USB-A drawing: https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/676/67643/676430910_sd.pdf

Adafruit CAD: designed by Limor Fried/Ladyada for Adafruit Industries; Creative Commons Attribution/Share-Alike, with included license files. Support Adafruit and open-source hardware by purchasing their products. Original adapter copyright 2026 Adam Fourney, MIT, with separate artwork licensing described in its README. Standard connector footprints are copied from the installed KiCad library, licensed CC-BY-SA-4.0 with the KiCad libraries exception: https://www.kicad.org/libraries/license/

## Regeneration

The native KiCad project is editable and self-contained for symbols/footprints. The generation scripts only target this Revision C directory. Rebuilding overwrites Revision C, so preserve manual KiCad edits first. Run `build_carrier.py` and then `route_carrier.py` with KiCad's bundled Python, export a KiCad XML netlist to `preview/netlist.xml`, then run `sync_nets.py`. The scripts are retained for reproducibility, not required to open the project.
