###useful astro functions I've written/collabed on over the years collected in one place

import numpy as np
from scipy.stats import distributions as dist
from astropy import units as u, cosmology as cos

####main functionality

class radio:
    ###functions specific to radio astronomy
    def __init__(self):
        ##set up cosmology parameters
        
        return

    
    def estimate_flux(nu_want, nu_known, s_known, a):
        'estimate the flux at a given frequency based on flux at known frequency and spectral index'
        
        flux_want = ((nu_want**a)/(nu_known**a))*s_known
        
        return flux_want


    def spec_idx(s1, s2, nu1, nu2, e_1=0, e_2=0, return_err=False):
        'estimate the spectral index of a source based on two flux measurements at different frequencies -- errors are only based on quad sum of flux errors, first order estimate only'
        
        s1,s2 = np.array(s1), np.array(s2)
    
        srat = s1/s2
        nurat = nu1/nu2
    
        alpha = np.log(srat)/np.log(nurat)
    
        if return_err==True:
            e_1, e_2 = np.array(e_1), np.array(e_2)
            erat = np.abs(srat)*(np.sqrt((e_1/s1)**2 + (e_2/s2)**2))
            e_alpha = np.abs(erat/(srat*np.log(10)))
            spidx = (alpha, e_alpha)
        else:
            spidx = alpha
        
        return spidx


    def radio_luminosity(flux, z, a=-0.7, sunit=u.mJy, lunit='W/Hz',
                         cosmology = cos.FlatLambdaCDM(H0=70, Om0=0.3),
                         badval=-99):
        'calculate the radio luminosity of a source based on flux, redshift, and assumed spectral index, returns log10 of value'
        
        ##convert to array(if not already)
        flux, z = np.array(flux), np.array(z)
    
        ###calulate luminosity distance in m (value to avoid dimensions when logging)
        dl = cosmology.luminosity_distance(z).to('m').value
        
        ###convert flux to W/Hz/m^2
        flux = flux*sunit.to(lunit + '/m2')
        
        ##radio power
        radpower = (flux*4*np.pi*dl**2)/((1+z)**a)
        print(type(radpower))
    
        ###filter bad values (flux has to be greater than 0)
        if type(radpower)==np.ndarray:
            radpower[flux<=0] = 1
        else:
            if radpower<=0:
                radpower = 1
    
        ###log10 of radio_power
        logrp = np.log10(radpower)
    
        ###filter bad values, outputs -99 as flag
        if type(radpower)==np.ndarray:
            logrp[flux==0] = badval
        else:
            if flux==0:
                logrp = badval
        
        return logrp



class stats:
    ###statistical functionality
    def __init__(self):
        return
    
    
    def summary(data, dp=3, flagval=None):
        'print out summary statistics for a given array; pd.describe for arrays instead of pandas data frames'
        
        n = len(data) ###keeps raw numbers of elements in array inc inf/nan
    
        ###remove nans/infs
        data = data[(np.isfinite(data))]
        
        n_notinf = len(data) ##new N
        n_naninf = n-n_notinf ##number of NaN/infs removed
        
        ###if there's a bad data value you want to exclude from your stats, remove this too
        if flagval is not None:
            data = data[(data!=flagval)]
            n_noflag = len(data)
            n_flag = n_notinf - n_noflag
            flagstring = str(flagval)
        else:
            n_flag = 0
            flagstring = 'na'
        
    
        ###final statement (define here to make length of ascii line)
        nanstate = ' ' + str(n_naninf) + ' non-finite values (not included in stats)'
        flagstate = (' ' + str(n_flag) + ' flagged as bad (value==' + flagstring +
                     '; not included in stats)')
        
        bllen = int(max([len(nanstate), len(flagstate)]))
        
        breakline = '-'*bllen
    
        ###print out stats
        print(breakline)
        print(' Data stats')
        print(' ')
        print(' N:        ', len(data))
        print(' Mean:     ', np.round(np.mean(data), dp))
        print(' Std dev.: ', np.round(np.std(data), dp))
        print(' Min:      ', np.round(np.min(data), dp))
        print(' P25:      ', np.round(np.percentile(data, 25), dp))
        print(' P50:      ', np.round(np.percentile(data, 50), dp))
        print(' P75:      ', np.round(np.percentile(data, 75), dp))
        print(' Max:      ', np.round(np.max(data), dp))
        print('')
        print(nanstate)
        print(flagstate)
        print(breakline)
        
        return
    
    
    def binom_frac(k, n, conf=0.683, nround=4):
        'return fraction and binomial errors based on confidence level'
        
        frac = k/n
        p_low = dist.beta.ppf((1-conf)/2, k+1, n-k+1)
        p_up = dist.beta.ppf(1-(1-conf)/2, k+1, n-k+1)
    
        el = p_low - frac
        eu = p_up - frac
        
        fracpluserrs = (np.round(frac, nround), np.round(el, nround), np.round(eu, nround))
        
        return fracpluserrs








