"""Attach carrier hardware models without changing electrical or placement data."""
from pathlib import Path
import shutil
import pcbnew as p

ROOT = Path(__file__).resolve().parent
LIB = Path('C:/Program Files/KiCad/10.0/share/kicad/3dmodels')
MODELS = ROOT / 'kicad/models'
MODELS.mkdir(exist_ok=True)

def add(fp, source, x=0, y=0, rotation=0, z=0, tilt=0):
    if not (MODELS / source.name).exists():
        shutil.copy2(source, MODELS / source.name)
    model = p.FP_3DMODEL()
    model.m_Filename = '${KIPRJMOD}/models/' + source.name
    model.m_Offset.x = x
    model.m_Offset.y = -y
    model.m_Offset.z = z
    model.m_Rotation.x = tilt
    model.m_Rotation.z = rotation
    fp.Add3DModel(model)

def apply(board):
    source_molex = MODELS / '430450600.stp'
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref in ('U1', 'U2', 'R1', 'R2', 'J4', 'J1'):
            fp.Models().clear()
        if ref == 'J1':
            add(fp, LIB / 'Connector_USB.3dshapes/USB_A_Molex_67643_Horizontal.step')
        elif ref == 'J4':
            # Manufacturer coordinates: Y is vertical; center the six tails on the pads.
            add(fp, source_molex, 3, -3.965, 180, z=3.94, tilt=-90)
        elif ref == 'U1':
            source = LIB / 'Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x13_P2.54mm_Vertical.step'
            for y in (1.27, 16.51):
                add(fp, source, 1.27, y, -90)
        elif ref == 'U2':
            source = LIB / 'Connector_PinSocket_2.54mm.3dshapes/PinSocket_1x04_P2.54mm_Vertical.step'
            for x in (2.54, 17.78):
                add(fp, source, x, 7.62)
        elif ref in ('R1', 'R2'):
            add(fp, LIB / 'Resistor_THT.3dshapes/R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal.step')
        if ref in ('U1', 'U2', 'R1', 'R2', 'J4', 'J1'):
            p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(ROOT / 'kicad/Carrier.pretty'), fp)

if __name__ == '__main__':
    path = ROOT / 'kicad/k1-carrier-rev-c.kicad_pcb'
    board = p.LoadBoard(str(path))
    apply(board)
    p.SaveBoard(str(path), board)
    print('3D models added; electrical layout preserved')
