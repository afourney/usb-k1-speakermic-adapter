"""Generate a reviewable KiCad carrier from the manufacturers' Eagle geometry."""
from pathlib import Path
import math
import uuid
import json
import xml.etree.ElementTree as ET
import pcbnew as p

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'kicad'
OUT.mkdir(exist_ok=True)
PROJECT='k1-carrier-rev-c'
LIB = OUT / 'Carrier.pretty'
LIB.mkdir(exist_ok=True)
board = p.BOARD()
board.SetCopperLayerCount(2)
netnames = ['GND', '+5V', '+3V3', 'USB_KB_P', 'USB_KB_N', 'USB_AUDIO_P', 'USB_AUDIO_N', 'PTT1', 'PTT2', 'MIC', 'HP_LEFT', 'SPK']
nets = {}
for name in netnames:
    net = p.NETINFO_ITEM(board, name)
    board.Add(net)
    nets[name] = net

def pt(x, y):
    return p.VECTOR2I(p.FromMM(x), p.FromMM(y))

def line(parent, a, b, layer, width=.15):
    s = p.PCB_SHAPE(parent)
    s.SetShape(p.SHAPE_T_SEGMENT)
    s.SetStart(pt(*a))
    s.SetEnd(pt(*b))
    s.SetLayer(layer)
    s.SetWidth(p.FromMM(width))
    parent.Add(s)

def text(value, x, y, size=1, layer=p.F_SilkS):
    t = p.PCB_TEXT(board)
    t.SetText(value)
    t.SetPosition(pt(x, y))
    t.SetTextSize(pt(size, size))
    t.SetTextThickness(p.FromMM(.15))
    t.SetLayer(layer)
    board.Add(t)

components = []
def footprint(ref, value, name, x, y, pads, outline):
    fp = p.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetFPID(p.LIB_ID('Carrier', name))
    fp.SetAttributes(p.FP_THROUGH_HOLE)
    fp.SetPosition(pt(x, y))
    fp.Reference().SetPosition(pt(x, y-3))
    fp.Reference().SetTextSize(pt(1, 1))
    fp.Value().SetVisible(False)
    for num, px, py, net in pads:
        pad = p.PAD(fp)
        pad.SetNumber(str(num))
        pad.SetAttribute(p.PAD_ATTRIB_PTH)
        pad.SetShape(p.PAD_SHAPE_CIRCLE)
        pad.SetSize(pt(1.8, 1.8))
        pad.SetDrillSize(pt(1, 1))
        layers=p.LSET.AllCuMask()
        layers.AddLayer(p.F_Mask)
        layers.AddLayer(p.B_Mask)
        pad.SetLayerSet(layers)
        pad.SetPosition(pt(x+px, y+py))
        if net:
            pad.SetNet(nets[net])
        fp.Add(pad)
    x0,y0,x1,y1 = outline
    for a,b in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:
        line(fp,(x+a[0],y+a[1]),(x+b[0],y+b[1]),p.F_Fab)
    for a,b in [((x0-.5,y0-.5),(x1+.5,y0-.5)),((x1+.5,y0-.5),(x1+.5,y1+.5)),((x1+.5,y1+.5),(x0-.5,y1+.5)),((x0-.5,y1+.5),(x0-.5,y0-.5))]:
        line(fp,(x+a[0],y+a[1]),(x+b[0],y+b[1]),p.F_CrtYd,.05)
    board.Add(fp)
    p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(LIB), fp)
    return fp

def eagle_pads(filename, selected, mapping, height):
    root = ET.parse(ROOT/'references'/filename).getroot()
    b = root.find('./drawing/board')
    packages = {(l.get('name'),pk.get('name')):pk for l in b.findall('./libraries/library') for pk in l.findall('./packages/package')}
    netmap = {(r.get('element'),r.get('pad')):s.get('name') for s in b.findall('./signals/signal') for r in s.findall('contactref')}
    result = []
    for el in b.findall('./elements/element'):
        if el.get('name') not in selected:
            continue
        angle = math.radians(float(el.get('rot','R0')[1:]))
        for pad in packages[(el.get('library'),el.get('package'))].findall('pad'):
            if not pad.get('name').isdigit():
                continue
            px,py = float(pad.get('x')),float(pad.get('y'))
            x = float(el.get('x')) + px*math.cos(angle)-py*math.sin(angle)
            y = float(el.get('y')) + px*math.sin(angle)+py*math.cos(angle)
            source = netmap.get((el.get('name'),pad.get('name')),'')
            num = selected[el.get('name')]+int(pad.get('name'))
            result.append((num,round(x,4),round(height-y,4),mapping.get(source,'')))
    return sorted(result)

kb = eagle_pads('kb2040.brd',{'JP1':0,'JP2':13},{'RAW':'+5V','GND':'GND','3.3V':'+3V3','D+':'USB_KB_P','D-':'USB_KB_N','D2':'PTT1','D3':'PTT2'},17.78)
hub = eagle_pads('hub.brd',{'JP2':0,'JP1':4},{'VBUS':'+5V','GND':'GND','D+1':'USB_KB_P','D-1':'USB_KB_N','D+2':'USB_AUDIO_P','D-2':'USB_AUDIO_N'},22.86)
footprint('U1','KB2040','KB2040',48,49,kb,(0,0,33.02,17.78))
footprint('U2','CH334F_5999','CH334F_5999',30,24.5,hub,(0,0,20.32,22.86))

def standard(ref,value,library,name,x,y,angle,pin_nets):
    plugin=p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP)
    fp=plugin.FootprintLoad('C:/Program Files/KiCad/10.0/share/kicad/footprints/'+library+'.pretty',name)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetFPID(p.LIB_ID('Carrier',name))
    fp.SetOrientationDegrees(angle)
    fp.SetPosition(pt(x,y))
    fp.Value().SetVisible(False)
    for pad in fp.Pads():
        net=pin_nets.get(pad.GetNumber())
        if net: pad.SetNet(nets[net])
    board.Add(fp)
    plugin.FootprintSave(str(LIB),fp)
    components.append((ref,value,[(num,num,net) for num,net in pin_nets.items()],name))
    return fp

def connector(ref,value,x,y,pin_nets,label_x=None):
    pads = [(i+1,0,i*2.54,n) for i,n in enumerate(pin_nets)]
    footprint(ref,value,'Wire_'+str(len(pads)),x,y,pads,(-1.3,-1.3,1.3,(len(pads)-1)*2.54+1.3))
    if ref=='J6':
        text('1',x-1.8,y,.8)
        text('J6: 1=5V 2=IN 3/4=GND',46,75.5,.8)
    else:
        for i,n in enumerate(pin_nets):
            text(str(i+1)+' '+(n or 'NC'),label_x if label_x else x+8,y+i*2.54,.8)
    components.append((ref,value,[(i+1,str(i+1),net) for i,net in enumerate(pin_nets)],'Wire_'+str(len(pads))))

standard('J1','USB_A_67643_0910','Connector_USB','USB_A_Molex_67643_Horizontal',86,40,90,{'1':'+5V','2':'USB_AUDIO_N','3':'USB_AUDIO_P','4':'GND','SH':'GND'})
connector('J2','SOUNDCARD_MIC',96,54,['MIC','GND'],86)
connector('J3','SOUNDCARD_HEADPHONE',96,65,['HP_LEFT','GND'],86)
standard('J4','K1_MICROFIT_43045_0600','Connector_Molex','Molex_Micro-Fit_3.0_43045-0600_2x03_P3.00mm_Horizontal',88,94,180,{'1':'PTT2','2':'MIC','3':'PTT1','4':'SPK','5':'','6':'GND'})
connector('J6','LM386_VCC_IN_GND_GND',23.5,85.19,['+5V','HP_LEFT','GND','GND'])
connector('J8','LM386_OUTPUT_AC',59,70,['SPK','GND'],65)
for ref, y, net in [('R1',70,'PTT1'),('R2',75,'PTT2')]:
    footprint(ref,'10k','R_Axial_7.62',72,y,[(1,0,0,'+3V3'),(2,7.62,0,net)],(-1,-1.3,8.62,1.3))

for i,(x,y) in enumerate([(24,28),(78,28),(24,100),(96,100)]):
    fp=p.FOOTPRINT(board)
    fp.SetReference('H'+str(i+1))
    fp.SetValue('M3')
    fp.SetAttributes(p.FP_BOARD_ONLY | p.FP_EXCLUDE_FROM_BOM | p.FP_EXCLUDE_FROM_POS_FILES)
    fp.SetPosition(pt(x,y))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    pad=p.PAD(fp)
    pad.SetAttribute(p.PAD_ATTRIB_NPTH)
    pad.SetShape(p.PAD_SHAPE_CIRCLE)
    pad.SetSize(pt(3.2,3.2))
    pad.SetDrillSize(pt(3.2,3.2))
    pad.SetPosition(pt(x,y))
    layers=p.LSET.AllCuMask()
    layers.AddLayer(p.F_Mask)
    layers.AddLayer(p.B_Mask)
    pad.SetLayerSet(layers)
    fp.Add(pad)
    board.Add(fp)
for a,b in [((20,24),(100,24)),((100,24),(100,104)),((100,104),(20,104)),((20,104),(20,24))]:
    line(board,a,b,p.Edge_Cuts,.05)
text('CABIN FEVER | REV C',62,35,1.1)
text('ENGINEERING DRAFT',48,102,.8)
text('USB-C TO HOST',36,51, .8)
text('KB2040 - USB-C LEFT',63,45,.8)
text('USB-A TO AUDIO',89,48,.8)
text('K1 / MICRO-FIT 3.0',85,86,.8)
text('LM386 41 x 14',54.5,87,.8,p.Dwgs_User)
text('Insulating mounting tape',54.5,91,.8,p.Dwgs_User)
for a,b in [((34,82),(75,82)),((75,82),(75,96)),((75,96),(34,96)),((34,96),(34,82))]:
    line(board,a,b,p.Dwgs_User)
p.SaveBoard(str(OUT/(PROJECT+'.kicad_pcb')),board)
(OUT/'fp-lib-table').write_text('(fp_lib_table (lib (name "Carrier")(type "KiCad")(uri "${KIPRJMOD}/Carrier.pretty")(options "")(descr "Module and wire footprints")))\n')
(OUT/(PROJECT+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':PROJECT+'.kicad_pro','version':1}},indent=2))

# A native schematic with explicit module pins and labelled wire connections.
def uid(): return str(uuid.uuid4())
def effects(size=1.27): return f'(effects (font (size {size} {size})))'
rootid=uid()
symbols=[]
instances=[]
decor=[]

def symbol(ref,value,pins,x,y,foot):
    x=round(x/1.27)*1.27
    y=round(y/1.27)*1.27
    # Pins are (number, name, net); unused module contacts receive no-connects.
    h=(len(pins)+1)*2.54
    libid='Carrier:'+value
    pinsexpr=''.join(f'(pin passive line (at -10.16 {-2.54*(i+1)} 0) (length 2.54) (name "{name}" {effects(.9)}) (number "{num}" {effects(.9)}))' for i,(num,name,net) in enumerate(pins))
    symbols.append(f'(symbol "{libid}" (pin_names (offset 0.508)) (in_bom yes) (on_board yes) (property "Reference" "{ref}" (at 0 2.54 0) {effects()}) (property "Value" "{value}" (at 0 0 0) {effects()}) (symbol "{value}_0_1" (rectangle (start -7.62 0) (end 15.24 {-h}) (stroke (width .254) (type default)) (fill (type background)))) (symbol "{value}_1_1" {pinsexpr}))')
    sid=uid()
    display_value='10k' if ref.startswith('R') else value
    for fp in board.GetFootprints():
        if fp.GetReference()==ref:
            path=p.KIID_PATH()
            path.push_back(p.KIID(rootid))
            path.push_back(p.KIID(sid))
            fp.SetPath(path)
            fp.SetValue(display_value)
    instances.append(f'(symbol (lib_id "{libid}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{sid}") (property "Reference" "{ref}" (at {x} {y-5.08} 0) {effects()}) (property "Value" "{display_value}" (at {x} {y-2.54} 0) {effects()}) (property "Footprint" "Carrier:{foot}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide)) (instances (project "{PROJECT}" (path "/{rootid}" (reference "{ref}") (unit 1)))))')
    for i,(num,name,net) in enumerate(pins):
        yy=y+2.54*(i+1)
        if net:
            decor.append(f'(wire (pts (xy {x-20.32} {yy}) (xy {x-10.16} {yy})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
            decor.append(f'(label "{net}" (at {x-20.32} {yy} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid()}"))')
        else:
            decor.append(f'(no_connect (at {x-10.16} {yy}) (uuid "{uid()}"))')

kbnames=['D10','MOSI','MISO','CLK','A0','A1','A2','A3','3V','RST','GND','RAW','D-','D+','TX','RX','GND','GND','D2','D3','D4','D5','D6','D7','D8','D9']
symbol('U1','KB2040',[(num,kbnames[num-1],net) for num,px,py,net in kb], fifty:=50,40,'KB2040')
symbol('U2','CH334F_5999',[(num,['P1_5V','P1_D+','P1_D-','P1_GND','P2_5V','P2_D+','P2_D-','P2_GND'][num-1],net) for num,px,py,net in hub],115,40,'CH334F_5999')
positions=[(175,40),(175,70),(175,90),(245,40),(115,90),(115,120)]
for (ref,value,pins,foot),(x,y) in zip(components,positions):
    symbol(ref,value,pins,x,y,foot)
for ref,net,x in [('R1','PTT1',175),('R2','PTT2',245)]:
    symbol(ref,'10k_'+ref,[(1,'1','+3V3'),(2,'2',net)],x,115,'R_Axial_7.62')
notes=[(30,22,'K1 SPEAKER-MIC CARRIER / REV B / ENGINEERING DRAFT'),(30,151,'J4: Micro-Fit 43045-0600. Cable housing 43025-0600. Use cavity numbers, not a guessed viewing order.'),(30,157,'J4 pins 1/2/3 = K1 3.5 mm tip/ring/sleeve; pins 4/5/6 = 2.5 mm tip/ring/sleeve. Pin 5 unused.'),(30,163,'J6: 2.54 mm pitch, 1=5V, 2=audio IN, 3=GND, 4=GND. Matches amplifier VCC/IN/GND/GND order.'),(30,169,'J8 receives capacitor-coupled speaker output. Pin 2 is optional common ground; return exists through J6.'),(30,175,'PTT pull-ups are 10k to KB2040 3V output, never 5V. J5 and J7 retired in Rev B.'),(30,181,'J1 USB-A connects the sound adapter. J2/J3 connect its audio plugs. Shield bonded to GND.'),(30,187,'Power through hub USB-C only. No second USB cable to installed KB2040. No 9V input.'),(30,193,'Review USB signal integrity, current budget and actual mechanical fit before fabrication.')]
for x,y,s in notes:
    decor.append(f'(text "{s}" (at {x} {y} 0) (effects (font (size 1.1 1.1)) (justify left)) (uuid "{uid()}"))')
sch=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{rootid}") (paper "A4") (lib_symbols {"".join(symbols)}) {"".join(instances)} {"".join(decor)} (sheet_instances (path "/" (page "1"))))'
(OUT/(PROJECT+'.kicad_sch')).write_text(sch.replace('REV B','REV C'))
(OUT/'Carrier.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor") '+''.join(s.replace('"Carrier:', '"',1) for s in symbols)+')')
(OUT/'sym-lib-table').write_text('(sym_lib_table (lib (name "Carrier")(type "KiCad")(uri "${KIPRJMOD}/Carrier.kicad_sym")(options "")(descr "Carrier module interfaces")))\n')
for fp in board.GetFootprints():
    if fp.GetReference() in ('R1','R2'):
        fp.Reference().SetPosition(pt(83,p.ToMM(fp.GetPosition().y)))
    if fp.GetReference()=='J4': fp.Reference().SetPosition(pt(85,88))
    if fp.GetReference()=='J1': fp.Reference().SetPosition(pt(81,39))
    if fp.GetReference()=='J8': fp.Reference().SetPosition(pt(55,70))
    if fp.GetReference()=='U2': fp.Reference().SetPosition(pt(27,36))
    if fp.GetReference()=='U1': fp.Reference().SetPosition(pt(44,59))
p.SaveBoard(str(OUT/(PROJECT+'.kicad_pcb')),board)
from add_models import apply as apply_models
apply_models(board)
p.SaveBoard(str(OUT/(PROJECT+'.kicad_pcb')),board)
print('Generated',OUT)
