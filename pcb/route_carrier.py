"""Route the prototype carrier; KiCad DRC remains the final geometric check."""
from pathlib import Path
import math
import heapq
import pcbnew as p

root=Path(__file__).resolve().parent
path=root/'kicad/k1-carrier-rev-c.kicad_pcb'
b=p.LoadBoard(str(path))
step=.25
def pos(v): return (p.ToMM(v.x),p.ToMM(v.y))
def point(x,y): return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def grid(x,y): return (round(x/step),round(y/step))
shapes=[]
by_net={}
for fp in b.GetFootprints():
    for pad in fp.Pads():
        x,y=pos(pad.GetPosition())
        net=pad.GetNetname()
        radius=max(p.ToMM(pad.GetSize().x),p.ToMM(pad.GetSize().y))/2
        shapes.append((x,y,radius,net or str(pad.m_Uuid),None))
        if net and net!='GND': by_net.setdefault(net,[]).append((x,y))

def obstacles(net,width):
    blocked=[set(),set()]
    for x,y,r,owner,layer in shapes:
        if owner==net: continue
        radius=r+.3+width/2+.05
        gx,gy=grid(x,y)
        span=math.ceil(radius/step)+1
        cells={(ix,iy) for ix in range(gx-span,gx+span+1) for iy in range(gy-span,gy+span+1) if math.hypot(ix*step-x,iy*step-y)<radius}
        for z in ([0,1] if layer is None else [layer]): blocked[z].update(cells)
    return blocked

def route(net,start,end,width):
    blocked=obstacles(net,width)
    a=grid(*start); target=grid(*end)
    for z in (0,1):
        blocked[z].discard(a); blocked[z].discard(target)
    goal=None
    queue=[]
    dist={}
    prev={}
    for z in (0,1):
        key=(*a,z); dist[key]=z*.2
        heapq.heappush(queue,(math.dist(a,target),z*.2,key))
    while queue:
        _,cost,state=heapq.heappop(queue)
        if dist.get(state)!=cost: continue
        x,y,z=state
        if (x,y)==target: goal=state; break
        moves=[(x+dx,y+dy,z,math.hypot(dx,dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
        # Via clearance is checked on both layers with an extra neighborhood.
        if all((x+dx,y+dy) not in blocked[zz] for zz in (0,1) for dx in (-1,0,1) for dy in (-1,0,1)):
            moves.append((x,y,1-z,24))
        for xx,yy,zz,extra in moves:
            if not (84<xx<396 and 100<yy<412) or (xx,yy) in blocked[zz]: continue
            if xx!=x and yy!=y and ((xx,y) in blocked[zz] or (x,yy) in blocked[zz]): continue
            new=(xx,yy,zz)
            nc=cost+extra*(1 if zz==0 else 1.05)
            if nc<dist.get(new,float('inf')):
                dist[new]=nc; prev[new]=state
                heapq.heappush(queue,(nc+math.hypot(xx-target[0],yy-target[1]),nc,new))
    if goal is None: raise RuntimeError('No route for '+net)
    nodes=[goal]
    while nodes[-1] in prev: nodes.append(prev[nodes[-1]])
    nodes.reverse()
    coords=[(x*step,y*step,z) for x,y,z in nodes]
    coords[0]=(*start,coords[0][2]); coords[-1]=(*end,coords[-1][2])
    simple=[coords[0]]
    for i in range(1,len(coords)-1):
        aa,bb,cc=coords[i-1:i+2]
        if aa[2]!=bb[2] or bb[2]!=cc[2] or abs((bb[0]-aa[0])*(cc[1]-bb[1])-(bb[1]-aa[1])*(cc[0]-bb[0]))>1e-7:
            simple.append(bb)
    simple.append(coords[-1])
    code=b.FindNet(net).GetNetCode()
    for aa,bb in zip(simple,simple[1:]):
        if aa[2]!=bb[2]:
            via=p.PCB_VIA(b); via.SetPosition(point(*aa[:2])); via.SetWidth(p.FromMM(.8)); via.SetDrill(p.FromMM(.4)); via.SetViaType(p.VIATYPE_THROUGH); via.SetLayerPair(p.F_Cu,p.B_Cu); via.SetNetCode(code); b.Add(via)
            shapes.append((*aa[:2],.4,net,None))
        elif aa[:2]!=bb[:2]:
            t=p.PCB_TRACK(b); t.SetStart(point(*aa[:2])); t.SetEnd(point(*bb[:2])); t.SetWidth(p.FromMM(width)); t.SetLayer(p.F_Cu if aa[2]==0 else p.B_Cu); t.SetNetCode(code); b.Add(t)
            count=max(1,math.ceil(math.dist(aa[:2],bb[:2])/.15))
            for k in range(count+1):
                shapes.append((aa[0]+(bb[0]-aa[0])*k/count,aa[1]+(bb[1]-aa[1])*k/count,width/2,net,aa[2]))

order=sorted(by_net,key=lambda n:(0 if 'USB' in n else 2 if n=='+5V' else 1,n))
for net in order:
    pins=by_net[net]
    connected=[pins[0]]; pending=pins[1:]
    while pending:
        _,start,end=min((math.dist(a,c),a,c) for a in connected for c in pending)
        route(net,start,end,.7 if net in ('+5V','SPK') else .3)
        connected.append(end); pending.remove(end)
    print('Routed',net,flush=True)

for layer in (p.F_Cu,p.B_Cu):
    zone=p.ZONE(b); zone.SetLayer(layer); zone.SetNetCode(b.FindNet('GND').GetNetCode()); zone.SetLocalClearance(p.FromMM(.3)); zone.SetThermalReliefGap(p.FromMM(.3)); zone.SetThermalReliefSpokeWidth(p.FromMM(.4)); zone.SetPadConnection(p.ZONE_CONNECTION_THERMAL)
    poly=zone.Outline(); poly.NewOutline()
    for x,y in [(20.5,24.5),(99.5,24.5),(99.5,103.5),(20.5,103.5)]: poly.Append(int(p.FromMM(x)),int(p.FromMM(y)))
    b.Add(zone)
filler=p.ZONE_FILLER(b)
filler.Fill(b.Zones())
p.SaveBoard(str(path),b)
print('Saved routed board',flush=True)
