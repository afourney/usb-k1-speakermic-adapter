# Enclosure and mounting

[Back to the build guide](../README.md)

The prototype uses a rectangular enclosure with a removable lid and an internal mounting plate. The K1 female pigtails and upstream USB cable leave through the front opening. The source CAD/STL files and exact enclosure dimensions were not available when this repository was prepared; this directory does not contain a printable replica.

<img src="images/finished-handset.jpg" alt="Complete handset, adapter enclosure, and USB cable" width="600">

## Fit a project box to the assembly

1. Arrange the amplifier, prototyping board, KB2040, hub, and audio adapter on an insulating plate before choosing the box size.
2. Include the full length of inserted audio and USB plugs in your measurements. Leave room for their cables to bend without pushing sideways on sockets.
3. Check lid clearance above the tallest part, including screw heads, cable ties, and any underside solder joints.
4. Plan access to the amplifier trimmer and the KB2040 BOOT/reset buttons. The hub connection can carry firmware updates, but physical button access is still useful for recovery.
5. Fix boards with suitable standoffs or nonconductive mounts. Secure the cased audio adapter separately so its mass cannot tug on USB solder joints.
6. Fit strain relief at cable exits. A pull on the outside cable should be taken by the enclosure or mounting plate, not by a PCB pad.
7. Keep analog microphone wiring away from USB data wiring and the amplifier power/output loop where practical.
8. Inspect for exposed conductors touching mounting hardware, then repeat the functional tests after assembly.

The two flying K1 sockets preserve access to the handset's existing plug. They also avoid needing to reproduce its exact two-plug spacing in a drilled panel.

![Open prototype enclosure](images/enclosure-open.jpg)

## CAD contributions

If adding the original enclosure later, include the editable source plus print-ready STL/3MF files, units, fastener and insert sizes, print orientation, and any fit adjustments. Publish measured dimensions and a tested fit; photos alone are not a dimensioned mechanical drawing.
