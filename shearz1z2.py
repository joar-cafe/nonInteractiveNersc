import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
import treecorr,time
import pickle,gc

#cat z1
#kappa=hp.fitsfunc.read_map(filename='/home/joar/temporal/NPCF_data/allsky/kappa.fits')
gamma1z1=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z9/gamma1.fits')
gamma2z1=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z9/gamma2.fits')
omegaz1=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z9/omega.fits')
#cat z2
gamma1z2=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z16/gamma1.fits')
gamma2z2=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z16/gamma2.fits')
omegaz2=hp.fitsfunc.read_map(filename='/global/cscratch1/sd/joar/sharing/allskyCatalogs/z16/omega.fits')
lenData=len(gamma1z1)

#omegaz1,omegaz2=np.ones(lenData),np.ones(lenData)

NSIDE=4096
tht,phi=hp.pix2ang(nside=NSIDE,ipix=range(hp.nside2npix(NSIDE)))# in radians
print("number of objects:",len(tht))

minArcmin=5.
maxArcmin=200.
minRad=minArcmin*np.pi/60/180
maxRad=maxArcmin*np.pi/60/180
print("minRad={:.5}, maxRad={:.5}".format(minRad,maxRad))

nSample=100#int(len(tht)/10) # max is len(tht)
np.random.seed(1080)
nDec=np.zeros(nSample)
nRac,nG1z1,nG2z1,nOmegaz1,nG1z2,nG2z2,nOmegaz2=nDec.copy(),nDec.copy(),nDec.copy(),nDec.copy(),nDec.copy(),nDec.copy(),nDec.copy()
t1=time.perf_counter()
for indx,ii in enumerate(np.random.choice(a=lenData,size=nSample,replace=False)):
    nDec[indx]=tht[ii]
    nRac[indx]=phi[ii]
    nG1z1[indx]=gamma1z1[ii]
    nG2z1[indx]=gamma2z1[ii]
    nOmegaz1[indx]=omegaz1[ii]
    if omegaz1[ii] < -3.57e-05:nOmegaz1[indx]=-2.43e-05
    else: nOmegaz1[indx]=omegaz1[ii]
    nG1z2[indx]=gamma1z2[ii]
    nG2z2[indx]=gamma2z2[ii]
    if omegaz2[ii] < -3.57e-05:nOmegaz2[indx]=-2.43e-05
    else: nOmegaz2[indx]=omegaz2[ii]
print("allocating sample of n={} from data, done in time={:.3} s".format(nSample,time.perf_counter()-t1))

# free memory of these not taken values from data
del(gamma1z1,gamma2z1,omegaz1,gamma1z2,gamma2z2,omegaz2)
gc.collect()

cat1=treecorr.Catalog(\
                      ra=nRac,dec=nDec,g1=nG1z1,g2=nG2z1,w=nOmegaz1,ra_units="rad",dec_units="rad")
cat2=treecorr.Catalog(\
                      ra=nRac,dec=nDec,g1=nG1z2,g2=nG2z2,w=nOmegaz2,ra_units="rad",dec_units="rad")

GG=treecorr.GGCorrelation(min_sep=minRad,max_sep=maxRad,verbose=2,nbins=20)

times={}
t1=time.perf_counter()
GG.process(cat1,cat2)
times[nSample]=round(time.perf_counter()-t1,ndigits=4)
print("walltime with perf_counter:",times)
with open('xip12N'+str(nSample)+'.pkl', 'wb') as f:
    pickle.dump(GG.xip, f)
with open('xim12N'+str(nSample)+'.pkl', 'wb') as f:
    pickle.dump(GG.xim, f)
with open('tht_arcmin12_rnom.pkl', 'wb') as f:
    pickle.dump(np.array(GG.rnom)*60*180/np.pi, f)
with open('times12.pkl','wb') as f:
    pickle.dump(times,f)
