"""Apply KiCad's exported net names, including its no-connect nets, to the PCB."""
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p
root=Path(__file__).resolve().parent
b=p.LoadBoard(str(root/'kicad/k1-carrier-rev-c.kicad_pcb'))
pads={}
for f in b.GetFootprints():
    for a in f.Pads(): pads.setdefault((f.GetReference(),a.GetNumber()),[]).append(a)
doc=ET.parse(root/'preview/netlist.xml')
for net in doc.findall('./nets/net'):
    name=net.get('name')
    targets=[pad for node in net.findall('node') for pad in pads[(node.get('ref'),node.get('pin'))]]
    old=targets[0].GetNetname()
    if old:
        ni=targets[0].GetNet()
        ni.SetNetname(name)
    else:
        ni=p.NETINFO_ITEM(b,name)
        b.Add(ni)
    for pad in targets: pad.SetNet(ni)
# Dense routing at these ground pads leaves insufficient room for thermal spokes.
# Solid ground connections avoid narrow thermal islands.
for pad in pads[('J4','6')]+pads[('U2','4')]:
    pad.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
p.ZONE_FILLER(b).Fill(b.Zones())
for fp in b.GetFootprints():
    if fp.GetReference()=='U1':
        fp.Reference().SetPosition(p.VECTOR2I(p.FromMM(44),p.FromMM(59)))
p.SaveBoard(str(root/'kicad/k1-carrier-rev-c.kicad_pcb'),b)
print('Schematic net names synchronized')
