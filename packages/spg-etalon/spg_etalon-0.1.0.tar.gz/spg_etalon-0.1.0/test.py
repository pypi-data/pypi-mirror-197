import sys
import spg_etalon
import numpy as np
sys.path.append('../functions')
import et_mueller2 as etm

tolerance = 1e-05

a=spg_etalon.EtalonProp()
a.show()

print('Asign a different value to wvl0')
a.wvl0 = 617.0e-9
print('new value ', a.wvl0)
a.show()

print('in python:')
etm.wvl0 = 617.0e-9
etm.m = round(2*etm.no*etm.h/etm.wvl0) #Order of the resonance peak
etm.wvl = etm.wvl0+etm.wvl0/(16*etm.no**2*etm.fnum**2) #Peak wavelength
etm.delta_h = (etm.m*etm.wvl-2*etm.no*etm.h)/(2*etm.no) #Variation of thickness to tune again to wvl0
print(etm.wvl0,etm.m,etm.wvl,etm.delta_h)
print('Finesse',etm.F , a.f)

print('----------')
x = spg_etalon.deltao(a,a.wvl0,0.1) 
y = etm.deltao(a.wvl0,0.1) 
print('Deltao matches Python: ',np.isclose(x,y, rtol= tolerance),x,y)

x = spg_etalon.deltae(a,a.wvl0,0.1,0.2) 
y = etm.deltae(a.wvl0,0.1,0.2) 
print('Deltae matches Python: ',np.isclose(x,y, rtol= tolerance),x,y)

print('----H11-H22------')

print('H11 - py', etm.H11(a.wvl0,0.1))
print('H11 - ru', spg_etalon.h11(a,a.wvl0,0.1) )
print('H22 - py', etm.H22(a.wvl0,0.1,0.1))
print('H22 - ru', spg_etalon.h22(a,a.wvl0,0.1,0.1) )

print('----H11pintr------')

#Spectral parameters
wvl0 = etm.wvl0 #Central wavelength (617.3 nm)
delta_1 = 60e-12 #Lower boundary of the wavelength range
delta_2 = 60e-12 #Upper boundary of the wavelength range
Nl = 121 #Number of wavelengths for the sampling of the profiles
wvlv = wvl0 + np.linspace(-delta_1, delta_2, Nl) #Wavelengths vector

#Simulation parameters
Rp=17.5e-3/2 #Pupil radius
fnum=etm.fnum #Telescope f-number
f=2*Rp*fnum #Focal

#llama a transm_fdt
#atilde=fdt.transm_fdt( x = 0.1, y = 0, wvlv ,tiltx = 0.0, tilty = 0.0 , teldegree = 0.23)

tiltx = 0
tilty = 0
theta3 = 0 #Optical axis direction of the etalon
teldegree=0.23

theta0x = tiltx * np.pi/180 #Chief ray angle incidence in X direction at etalon center
theta0y = tilty * np.pi/180 # Chief ray angle of incidene in Y direction at etalon center
theta_tel = teldegree*np.pi/180 #Nominal degree of telecentrism center-border

#Coordinates
xi0 = f * theta0x
eta0 = f * theta0y
xi_lim = f * theta_tel #FOV [m]
xi = x * xi_lim + xi0
eta = y * xi_lim + eta0

k = 2*np.pi/wvlv[0]

lims = [[0,Rp],[0,2*np.pi]]

Rp_lims = np.linspace(0,Rp, 100)
an_lims = np.linspace(0,2*np.pi, 100)

f1 = np.zeros((Nl,100,100))
f2 = np.zeros((Nl,100,100))
for i,ii in enumerate(Rp_lims):
    for j,jj in enumerate(Rp_lims):
        for ki,kki in enumerate(wvlv):
            f1[ ki, ii,jj ] = etm.H11pintr(i, j,  xi, eta, xi, eta, k, f, ki, theta3)
            f2[ ki, ii,jj ] = spg_etalon.h11pintr(a, i, j, xi, eta, xi, eta, ki, theta3)

py_H11pintr = etm.H11pintr(0, 0,  xi, eta, xi, eta, k, f, wvlv[0], theta3)
print('Python H11pintr: ',py_H11pintr)

ru_H11pintr = spg_etalon.h11pintr(a, 0, 0, xi, eta, xi, eta, wvlv[0], theta3)
print('Rust H11pintr:   ',ru_H11pintr)

    # """
    # Integrals to calculate a,b,c,d Mueller matrix coefficients
    # """
    # i=-1 #Spectral index
    # lims=[[0,Rp],[0,2*np.pi]]
    # atilde=np.zeros(wvl.shape[0])
    # if etm.ne != etm.no:
    #     btilde=atilde.copy()

    # print('Computation of integrals...')
    # wvli = wvl[0]
    
    # i+=1
    # k=2*np.pi/wvli

    # params=(xi,eta,xi,eta,k,f,wvli,theta3) #xi0=xi; eta0=eta
    # limit={'limit':50}
    # H11tr=intgrl.nquad(etm.H11pintr,lims,args=params,opts=limit)
    # H11ti = 0
    # # H11ti=intgrl.nquad(etm.H11pinti,lims,args=params,opts=limit)
    # H11t=(H11tr[0]+1j*H11ti[0])/(np.pi*Rp**2)
    # #abcd
    # atilde[i],btilde,ctilde,dtilde=etm.abcd(H11t,H11t)


sys.exit()