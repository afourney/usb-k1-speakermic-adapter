# Revision C source snapshot

Open `kicad/k1-carrier-rev-c.kicad_pro` in KiCad 10.

This folder is a standalone snapshot suitable for adding to a Git branch. It does not contain or initialize a Git repository. The editable board and schematic, project settings, local symbol and footprint libraries, five required model files, build scripts, reference geometry and attribution, and review previews are included. No files in another revision are required to open this project. No caches, editor locks or local UI preferences are included.

All PCB and footprint 3D model paths use `${KIPRJMOD}/models/`. Model files include the Molex 430450600 manufacturer STEP model and the USB-A, female socket and resistor KiCad library models. Third-party files retain their respective terms; see README and reference licenses before publishing. The manufacturer CAD is not relicensed as original project source.

The PCB is 80 x 80 mm. J8 is left of R1/R2, the LM386 mounting outline has moved right, and amplifier tie-down holes are removed for insulating mounting tape. PTT pull-ups remain on the KB2040 3.3 V rail. This is still an engineering draft, not a fabrication release.

The saved KiCad files are the primary editable deliverable. The Python scripts are optional regeneration tools: rebuilding replaces manual edits, and the generator currently expects the Windows KiCad 10 installation path for Python bindings and standard footprints. Included local models are preferred when reapplying models. See README for the regeneration sequence and prototype limitations.
