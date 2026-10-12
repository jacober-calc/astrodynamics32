import os, json, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; PURPLE="#7048e8"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/ad_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
# Constants as stored by LBL A (registers -900 to -929)
K={-100:149597870.7,-900:1.327124400189e20,-903:3.9860044188e14,-910:696342000,-913:6378137,
   -921:57910000,-922:108200000,-923:149600000,-924:227900000,-925:778500000,-926:1433449370,-927:2871000000,-928:4500000000,-929:384400}
SID=86164.0905
mu,R=K[-903],K[-913]
def from_h(h): r=R+h; v=math.sqrt(mu/r); P=2*math.pi*math.sqrt(r**3/mu); return v,P/60,P/SID
def h_from_D(D): P=D*SID; return (mu*(P/(2*math.pi))**2)**(1/3)-R

# 1 Orbit curves around EARTH
hs=np.logspace(5,9,400)  # metres, 100 km to 1,000,000 km
v=np.sqrt(mu/(R+hs)); P=2*np.pi*np.sqrt((R+hs)**3/mu)
marks=[("ISS",407e3,BLUE),("GPS (D = 0.5)",h_from_D(.5),GREEN),("Geostationary (D = 1)",h_from_D(1),ORANGE),("MOON",K[-929]*1e3-R,PURPLE)]
fig,(ax,bx)=plt.subplots(1,2,figsize=(10.8,4.4))
ax.semilogx(hs/1e3,v/1e3,color=INK,lw=2.2); bx.loglog(hs/1e3,P/SID,color=INK,lw=2.2)
for lab,h,c in marks:
    vv,pm,dd=from_h(h)
    ax.plot(h/1e3,vv/1e3,"o",color=c,ms=8,zorder=5); bx.plot(h/1e3,dd,"o",color=c,ms=8,zorder=5)
offs_v={"ISS":(8,-26),"GPS (D = 0.5)":(8,6),"Geostationary (D = 1)":(-6,-28),"MOON":(8,10)}
offs_p={"ISS":(8,-4),"GPS (D = 0.5)":(-12,8),"Geostationary (D = 1)":(10,-10),"MOON":(-10,-18)}
for lab,h,c in marks:
    vv,pm,dd=from_h(h)
    ax.annotate(f"{lab}\n{vv:,.0f} m/s",xy=(h/1e3,vv/1e3),xytext=offs_v[lab],textcoords="offset points",fontsize=9,color=c,ha="right" if offs_v[lab][0]<0 else "left")
    tp=f"{pm:,.1f} min" if dd<.999 else (f"{dd:.3f} sidereal days" if dd<1.001 else f"{dd:.3g} sidereal days")
    bx.annotate(f"{lab}\n{tp}",xy=(h/1e3,dd),xytext=offs_p[lab],textcoords="offset points",fontsize=9,color=c,ha="right" if offs_p[lab][0]<0 else "left")
bx.axhline(1,color=ORANGE,ls=":",lw=1)
ax.set_xlabel("Height above EARTH, H (km)"); ax.set_ylabel("Velocity V (km/s)"); ax.set_title("Velocity: V = √(μ ÷ r)",loc="left",fontsize=12)
bx.set_xlabel("Height above EARTH, H (km)"); bx.set_ylabel("Period, sidereal days D"); bx.set_title("Period: P = 2π √(r³ ÷ μ)",loc="left",fontsize=12)
ax.set_xlim(100,1e6); bx.set_xlim(100,1e6)
fig.suptitle("Circular Orbits Around EARTH  (r = R + H)",x=.07,ha="left",fontweight="bold",fontsize=13); fig.tight_layout(); save(fig,"earth_orbits")

# 2 Register map
bodies=["SUN","MERCURY","VENUS","EARTH","MARS","JUPITER","SATURN","URANUS","NEPTUNE","MOON"]
fig,ax=plt.subplots(figsize=(11,3.6)); ax.axis("off"); ax.set_xlim(-2.2,10.05); ax.set_ylim(-.15,4.35)
rows=[("−90X","μ (m³/s²)",BLUE),("−91X","Radius (m)",GREEN),("−92X","Distance (km)",ORANGE)]
for j,b in enumerate(bodies):
    ax.text(j+.5,3.75,f"X = {j}",ha="center",fontsize=10,fontweight="bold"); ax.text(j+.5,3.38,b,ha="center",fontsize=8.6,color=GREY)
for r,(code,lab,c) in enumerate(rows):
    y=2.25-r*1.05
    ax.text(-2.1,y+.45,code,fontsize=12,fontweight="bold",color=c,va="center"); ax.text(-1.25,y+.45,lab,fontsize=9.5,va="center")
    for j in range(10):
        reg=-(900+10*(r)+j) if True else 0
        reg=-(900+10*r+j)
        empty=(r==2 and j==0)
        ax.add_patch(FancyBboxPatch((j+.06,y+.06),.88,.8,boxstyle="round,pad=0,rounding_size=.06",fc="#f4f6f8" if empty else "white",ec=GREY if empty else c,lw=1.3))
        ax.text(j+.5,y+.62,f"−{abs(reg)}",ha="center",va="center",fontsize=9,fontweight="bold",color=GREY if empty else c)
        if not empty:
            val=K.get(reg)
            if r==0: s={-900:"1.3271E20",-903:"3.9860E14"}.get(reg,"")
            txt={-900:"1.33E20",-901:"2.20E13",-902:"3.25E14",-903:"3.99E14",-904:"4.28E13",-905:"1.27E17",-906:"3.79E16",-907:"5.79E15",-908:"6.84E15",-909:"4.90E12",
                 -910:"6.96E8",-911:"2.44E6",-912:"6.05E6",-913:"6.38E6",-914:"3.40E6",-915:"7.15E7",-916:"6.03E7",-917:"2.56E7",-918:"2.48E7",-919:"1.74E6",
                 -921:"5.79E7",-922:"1.08E8",-923:"1.50E8",-924:"2.28E8",-925:"7.79E8",-926:"1.43E9",-927:"2.87E9",-928:"4.50E9",-929:"3.84E5"}[reg]
            ax.text(j+.5,y+.3,txt,ha="center",va="center",fontsize=8.4)
        else: ax.text(j+.5,y+.3,"unused",ha="center",va="center",fontsize=8,color=GREY)
ax.text(9.5,-.08,"−929: distance from EARTH",ha="right",fontsize=8.6,color=ORANGE,va="center")
ax.text(-2.1,4.25,"Indirect Register Map  (−100 series: AU, sidereal days per year, speed of light)",fontsize=12.5,fontweight="bold",va="center")
save(fig,"register_map")

# 3 Planets
names=bodies[1:9]; d=np.array([K[-921-j] for j in range(8)])*1e3; vs=np.sqrt(K[-900]/d)
fig,ax=plt.subplots(figsize=(8.8,4.4))
rr=np.logspace(10.5,12.8,300); ax.loglog(rr/1e3/K[-100],np.sqrt(K[-900]/rr)/1e3,color=GREY,lw=1.2,ls="--",label="V = √(μ_SUN ÷ r)")
for n,dd,vv in zip(names,d,vs):
    c=BLUE if n=="EARTH" else ORANGE
    ax.plot(dd/1e3/K[-100],vv/1e3,"o",color=c,ms=9 if n=="EARTH" else 7,zorder=5)
    off={"VENUS":(-8,6),"MARS":(-8,-26)}.get(n,(7,4))
    ax.annotate(f"{n}\n{vv/1e3:.2f} km/s",xy=(dd/1e3/K[-100],vv/1e3),xytext=off,ha="right" if off[0]<0 else "left",textcoords="offset points",fontsize=8.8,color=c,fontweight="bold" if n=="EARTH" else "normal")
ax.set_xlabel("Distance from the SUN (AU; registers −921 to −928)"); ax.set_ylabel("Circular orbital velocity (km/s)")
ax.set_xlim(.25,45); ax.set_ylim(4,60); ax.legend(frameon=False,loc="lower left")
ax.set_xticks([.3,.5,1,2,5,10,20,40]); ax.set_xticklabels(["0.3","0.5","1","2","5","10","20","40"])
ax.set_yticks([5,10,20,30,50]); ax.set_yticklabels(["5","10","20","30","50"]); ax.minorticks_off()
ax.set_title("Circular Orbital Velocity of the Planets Around the SUN",loc="left"); save(fig,"planet_velocities")
print({n:round(v,1) for n,v in zip(names,vs)}, h_from_D(1)/1e3, h_from_D(.5)/1e3, from_h(K[-929]*1e3-R))
