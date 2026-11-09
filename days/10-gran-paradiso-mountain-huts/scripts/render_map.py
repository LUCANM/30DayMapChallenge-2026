from pathlib import Path
import json
import numpy as np
import rasterio
from pyproj import Transformer
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
out=Path(__file__).resolve().parents[1]
D=out/'data'
(out/'maps').mkdir(exist_ok=True)
with rasterio.open(D/'elevation.tif') as ds:
 dem=ds.read(1);xmin,ymin,xmax,ymax=ds.bounds;tr=ds.transform
xx,yy=np.meshgrid(xmin+(np.arange(dem.shape[1])+.5)*tr.a,ymax+(np.arange(dem.shape[0])+.5)*tr.e)
rgb=np.array(Image.open(D/'relief.png').convert('RGB'))/255.
features=[]
for cat in ['alpine_hut','wilderness_hut']:features+=json.loads((D/(cat+'.geojson')).read_text(encoding='utf-8'))['features']
peak=json.loads((D/'peak.geojson').read_text(encoding='utf-8'))['features'][0]
fwd=Transformer.from_crs(4326,32632,always_xy=True).transform
assert len(features)==49
bg='#101b30';ink='#f5eee1';muted='#a9bdca';gold='#f5bb72';ice='#8ce1e2'
fig=plt.figure(figsize=(16,15),facecolor=bg);fig.text(.055,.952,'10 / PROMPTING ONLY',fontsize=12,fontweight='bold',color=ice);fig.text(.945,.952,'#30DayMapChallenge 2026',ha='right',fontsize=11,color=muted)
fig.text(.055,.895,'GRAN PARADISO',fontsize=38,fontweight='bold',color=ink);fig.text(.055,.85,'MOUNTAIN HUTS',fontsize=25,color=ink);fig.text(.945,.85,'ITALIAN ALPS',ha='right',fontsize=15,color=muted)
ax=fig.add_axes([.055,.255,.89,.55]);ax.imshow(rgb,extent=(xmin,xmax,ymin,ymax));ax.set_aspect('equal');ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax);ax.set_facecolor(bg)
ax.contour(xx,yy,dem,levels=np.arange(1000,4500,500),colors=ink,linewidths=.25,alpha=.22)
for cat,c,m in [('alpine_hut',gold,'o'),('wilderness_hut',ice,'D')]:
 pts=np.array([fwd(*f['geometry']['coordinates']) for f in features if f['properties']['tourism']==cat]);ax.scatter(pts[:,0],pts[:,1],s=115,c=bg,alpha=.45,zorder=5);ax.scatter(pts[:,0],pts[:,1],s=31,c=c,marker=m,edgecolors=bg,linewidths=.65,zorder=6)
px,py=fwd(*peak['geometry']['coordinates']);ax.scatter([px],[py],marker='^',s=55,color=ink,zorder=7)
# Selected source names. Test text bounding boxes before placing each label.
fig.canvas.draw();renderer=fig.canvas.get_renderer();occupied=[]
labels=[(px,py,'Gran Paradiso',True)]
for f in features:
 name=f['properties']['name']
 if 'invernale' not in name.lower() and any(t in name.lower() for t in ['chabod','vittorio emanuele','sella','pontese']):
  x,y=fwd(*f['geometry']['coordinates']);labels.append((x,y,name,False))
for x,y,name,ispeak in labels:
 for dx,dy in [(9,10),(9,-17),(-9,12),(-9,-20),(9,30),(-9,-38),(24,46),(-24,-54)]:
  a=ax.annotate(name,(x,y),xytext=(dx,dy),textcoords='offset points',ha='left' if dx>0 else 'right',fontsize=8.5,color=ink,fontweight='bold' if ispeak else 'normal',path_effects=[pe.withStroke(linewidth=2.5,foreground=bg)],arrowprops={'arrowstyle':'-','color':muted,'lw':.5},zorder=8)
  fig.canvas.draw();bb=a.get_window_extent(renderer).expanded(1.04,1.25)
  if not any(bb.overlaps(b) for b in occupied):occupied.append(bb);break
  a.remove()
 else: raise RuntimeError('Could not place label: '+name)
ax.plot([xmin+2300,xmin+12300],[ymin+2000,ymin+2000],c=ink,lw=2);ax.text(xmin+7300,ymin+2600,'10 km',ha='center',color=ink,fontsize=9)
ax.annotate('GRID N',xy=(xmax-2500,ymax-2200),xytext=(xmax-2500,ymax-6500),ha='center',color=ink,fontsize=9,arrowprops={'arrowstyle':'-|>','color':ink,'lw':1})
ax.set_xticks([]);ax.set_yticks([])
for s in ax.spines.values():s.set_color('#41546a');s.set_linewidth(.6)
fig.text(.06,.202,'49',fontsize=43,color=ink,fontweight='bold');fig.text(.148,.208,'MAPPED HUTS\nin the study extent',fontsize=11,color=muted,linespacing=1.5)
fig.text(.45,.213,'●  36 Alpine huts',color=gold,fontsize=14);fig.text(.70,.213,'◆  13 Wilderness huts',color=ice,fontsize=14)

fig.text(.06,.116,'PROMPTING ONLY  Map produced in Python through written instructions.',fontsize=10,color=muted)
fig.text(.06,.093,'Study: 7.05–7.65° E / 45.35–45.75° N · Hut inventory reflects OSM mapping, not completeness or current opening status.',fontsize=9,color=muted)
fig.text(.06,.071,'DATA  © OpenStreetMap contributors, ODbL · AWS / Mapzen Terrain · Copernicus EU-DEM (EU funded); USGS SRTM / GMTED.',fontsize=8,color=muted)
fig.text(.06,.05,'EPSG:32632',fontsize=8,color=muted)
fig.text(.06,.033,'openstreetmap.org/copyright | opendatacommons.org/licenses/odbl/1.0/',fontsize=8,color=muted)
fig.savefig(out/'maps/Gran_Paradiso_Day10.png',dpi=200,facecolor=bg)
fig.savefig(out/'maps/preview.png',dpi=80,facecolor=bg)
plt.close(fig)
print('Rendered 49 huts to maps/Gran_Paradiso_Day10.png')
