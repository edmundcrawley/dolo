

from __future__ import division

from numba import double, int64

from numba import jit, njit

import numpy as np
from numpy import zeros, array

from math import floor
from numpy import empty


Ad = array([
#      t^3       t^2        t        1	
   [-1.0/6.0,  3.0/6.0, -3.0/6.0, 1.0/6.0],
   [ 3.0/6.0, -6.0/6.0,  0.0/6.0, 4.0/6.0],
   [-3.0/6.0,  3.0/6.0,  3.0/6.0, 1.0/6.0],
   [ 1.0/6.0,  0.0/6.0,  0.0/6.0, 0.0/6.0]
])

dAd = zeros((4,4))
for i in range(1,4):
	dAd[:,i] = Ad[:,i-1]*(4-i)


d2Ad = zeros((4,4))
for i in range(1,4):
	d2Ad[:,i] = dAd[:,i-1]*(4-i)


@njit
def vec_eval_cubic_multi_spline_1(a, b, orders, mcoefs, points, values):

    N = points.shape[0]

    for n in range(N):
        point = points[n, :]
        val = values[n, :]
        eval_cubic_multi_spline_1(a, b, orders, mcoefs, point, val, Ad, dAd)

@njit
def vec_eval_cubic_multi_spline_2(a, b, orders, mcoefs, points, values):


    N = points.shape[0]

    for n in range(N):
        point = points[n, :]
        val = values[n, :]
        eval_cubic_multi_spline_2(a, b, orders, mcoefs, point, val, Ad, dAd)

@njit
def vec_eval_cubic_multi_spline_3(a, b, orders, mcoefs, points, values):

    N = points.shape[0]

    for n in range(N):
        point = points[n, :]
        val = values[n, :]
        eval_cubic_multi_spline_3(a, b, orders, mcoefs, point, val, Ad, dAd)




# @jit("int64( double[:], double[:], int64[:], double[:,:], double[:], double[:], double[:,:], double[:,:])", nopython=True)
@njit
def eval_cubic_multi_spline_1(smin, smax, orders, coefs, svec, vals, Ad, dAd):

    n_vals = vals.shape[0]
        
    M0 = orders[0]
    start0 = smin[0]
    dinv0 = (orders[0]-1.0)/(smax[0]-smin[0])
    x0 = svec[0]
    u0 = (x0 - start0)*dinv0
    i0 = int( floor( u0 ) )
    i0 = max( min(i0,M0-2), 0 )
    t0 = u0-i0
    tp0_0 = t0*t0*t0;  tp0_1 = t0*t0;  tp0_2 = t0;  tp0_3 = 1.0;
        
    Phi0_0 = 0.0
    Phi0_1 = 0.0
    Phi0_2 = 0.0
    Phi0_3 = 0.0

    if t0 < 0:
        Phi0_0 = dAd[0,3]*t0 + Ad[0,3]
        Phi0_1 = dAd[1,3]*t0 + Ad[1,3]
        Phi0_2 = dAd[2,3]*t0 + Ad[2,3]
        Phi0_3 = dAd[3,3]*t0 + Ad[3,3]
    elif t0 > 1:
        Phi0_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t0-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi0_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t0-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi0_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t0-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi0_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t0-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi0_0 = (Ad[0,0]*tp0_0 + Ad[0,1]*tp0_1 + Ad[0,2]*tp0_2 + Ad[0,3]*tp0_3)
        Phi0_1 = (Ad[1,0]*tp0_0 + Ad[1,1]*tp0_1 + Ad[1,2]*tp0_2 + Ad[1,3]*tp0_3)
        Phi0_2 = (Ad[2,0]*tp0_0 + Ad[2,1]*tp0_1 + Ad[2,2]*tp0_2 + Ad[2,3]*tp0_3)
        Phi0_3 = (Ad[3,0]*tp0_0 + Ad[3,1]*tp0_1 + Ad[3,2]*tp0_2 + Ad[3,3]*tp0_3)
    
    for n in range(n_vals):
        vals[n] = Phi0_0*(coefs[n,i0+0]) + Phi0_1*(coefs[n,i0+1]) + Phi0_2*(coefs[n,i0+2]) + Phi0_3*(coefs[n,i0+3])

    return 0


# @jit("int64( double[:], double[:], int64[:], double[:,:,:], double[:], double[:], double[:,:], double[:,:])", nopython=True) #, device=True, target='gpu') 

@njit
def eval_cubic_multi_spline_2(smin, smax, orders, coefs, svec, vals, Ad, dAd):

    n_vals = vals.shape[0]
        
    M0 = orders[0]
    start0 = smin[0]
    dinv0 = (orders[0]-1.0)/(smax[0]-smin[0])
    M1 = orders[1]
    start1 = smin[1]
    dinv1 = (orders[1]-1.0)/(smax[1]-smin[1])
    x0 = svec[0]
    x1 = svec[1]
    u0 = (x0 - start0)*dinv0
    i0 = int( floor( u0 ) )
    i0 = max( min(i0,M0-2), 0 )
    t0 = u0-i0
    u1 = (x1 - start1)*dinv1
    i1 = int( floor( u1 ) )
    i1 = max( min(i1,M1-2), 0 )
    t1 = u1-i1
    tp0_0 = t0*t0*t0;  tp0_1 = t0*t0;  tp0_2 = t0;  tp0_3 = 1.0;
    tp1_0 = t1*t1*t1;  tp1_1 = t1*t1;  tp1_2 = t1;  tp1_3 = 1.0;
        
    Phi0_0 = 0.0
    Phi0_1 = 0.0
    Phi0_2 = 0.0
    Phi0_3 = 0.0

    if t0 < 0:
        Phi0_0 = dAd[0,3]*t0 + Ad[0,3]
        Phi0_1 = dAd[1,3]*t0 + Ad[1,3]
        Phi0_2 = dAd[2,3]*t0 + Ad[2,3]
        Phi0_3 = dAd[3,3]*t0 + Ad[3,3]
    elif t0 > 1:
        Phi0_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t0-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi0_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t0-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi0_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t0-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi0_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t0-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi0_0 = (Ad[0,0]*tp0_0 + Ad[0,1]*tp0_1 + Ad[0,2]*tp0_2 + Ad[0,3]*tp0_3)
        Phi0_1 = (Ad[1,0]*tp0_0 + Ad[1,1]*tp0_1 + Ad[1,2]*tp0_2 + Ad[1,3]*tp0_3)
        Phi0_2 = (Ad[2,0]*tp0_0 + Ad[2,1]*tp0_1 + Ad[2,2]*tp0_2 + Ad[2,3]*tp0_3)
        Phi0_3 = (Ad[3,0]*tp0_0 + Ad[3,1]*tp0_1 + Ad[3,2]*tp0_2 + Ad[3,3]*tp0_3)
        
    Phi1_0 = 0.0
    Phi1_1 = 0.0
    Phi1_2 = 0.0
    Phi1_3 = 0.0

    if t1 < 0:
        Phi1_0 = dAd[0,3]*t1 + Ad[0,3]
        Phi1_1 = dAd[1,3]*t1 + Ad[1,3]
        Phi1_2 = dAd[2,3]*t1 + Ad[2,3]
        Phi1_3 = dAd[3,3]*t1 + Ad[3,3]
    elif t1 > 1:
        Phi1_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t1-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi1_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t1-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi1_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t1-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi1_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t1-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi1_0 = (Ad[0,0]*tp1_0 + Ad[0,1]*tp1_1 + Ad[0,2]*tp1_2 + Ad[0,3]*tp1_3)
        Phi1_1 = (Ad[1,0]*tp1_0 + Ad[1,1]*tp1_1 + Ad[1,2]*tp1_2 + Ad[1,3]*tp1_3)
        Phi1_2 = (Ad[2,0]*tp1_0 + Ad[2,1]*tp1_1 + Ad[2,2]*tp1_2 + Ad[2,3]*tp1_3)
        Phi1_3 = (Ad[3,0]*tp1_0 + Ad[3,1]*tp1_1 + Ad[3,2]*tp1_2 + Ad[3,3]*tp1_3)
    
    for n in range(n_vals):
        vals[n] = Phi0_0*(Phi1_0*(coefs[n,i0+0,i1+0]) + Phi1_1*(coefs[n,i0+0,i1+1]) + Phi1_2*(coefs[n,i0+0,i1+2]) + Phi1_3*(coefs[n,i0+0,i1+3])) + Phi0_1*(Phi1_0*(coefs[n,i0+1,i1+0]) + Phi1_1*(coefs[n,i0+1,i1+1]) + Phi1_2*(coefs[n,i0+1,i1+2]) + Phi1_3*(coefs[n,i0+1,i1+3])) + Phi0_2*(Phi1_0*(coefs[n,i0+2,i1+0]) + Phi1_1*(coefs[n,i0+2,i1+1]) + Phi1_2*(coefs[n,i0+2,i1+2]) + Phi1_3*(coefs[n,i0+2,i1+3])) + Phi0_3*(Phi1_0*(coefs[n,i0+3,i1+0]) + Phi1_1*(coefs[n,i0+3,i1+1]) + Phi1_2*(coefs[n,i0+3,i1+2]) + Phi1_3*(coefs[n,i0+3,i1+3]))

    return 0



@njit
def eval_cubic_multi_spline_3(smin, smax, orders, coefs, svec, vals, Ad, dAd):

    n_vals = vals.shape[0]
        
    M0 = orders[0]
    start0 = smin[0]
    dinv0 = (orders[0]-1.0)/(smax[0]-smin[0])
    M1 = orders[1]
    start1 = smin[1]
    dinv1 = (orders[1]-1.0)/(smax[1]-smin[1])
    M2 = orders[2]
    start2 = smin[2]
    dinv2 = (orders[2]-1.0)/(smax[2]-smin[2])
    x0 = svec[0]
    x1 = svec[1]
    x2 = svec[2]
    u0 = (x0 - start0)*dinv0
    i0 = int( floor( u0 ) )
    i0 = max( min(i0,M0-2), 0 )
    t0 = u0-i0
    u1 = (x1 - start1)*dinv1
    i1 = int( floor( u1 ) )
    i1 = max( min(i1,M1-2), 0 )
    t1 = u1-i1
    u2 = (x2 - start2)*dinv2
    i2 = int( floor( u2 ) )
    i2 = max( min(i2,M2-2), 0 )
    t2 = u2-i2
    tp0_0 = t0*t0*t0;  tp0_1 = t0*t0;  tp0_2 = t0;  tp0_3 = 1.0;
    tp1_0 = t1*t1*t1;  tp1_1 = t1*t1;  tp1_2 = t1;  tp1_3 = 1.0;
    tp2_0 = t2*t2*t2;  tp2_1 = t2*t2;  tp2_2 = t2;  tp2_3 = 1.0;
        
    Phi0_0 = 0.0
    Phi0_1 = 0.0
    Phi0_2 = 0.0
    Phi0_3 = 0.0

    if t0 < 0:
        Phi0_0 = dAd[0,3]*t0 + Ad[0,3]
        Phi0_1 = dAd[1,3]*t0 + Ad[1,3]
        Phi0_2 = dAd[2,3]*t0 + Ad[2,3]
        Phi0_3 = dAd[3,3]*t0 + Ad[3,3]
    elif t0 > 1:
        Phi0_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t0-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi0_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t0-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi0_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t0-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi0_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t0-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi0_0 = (Ad[0,0]*tp0_0 + Ad[0,1]*tp0_1 + Ad[0,2]*tp0_2 + Ad[0,3]*tp0_3)
        Phi0_1 = (Ad[1,0]*tp0_0 + Ad[1,1]*tp0_1 + Ad[1,2]*tp0_2 + Ad[1,3]*tp0_3)
        Phi0_2 = (Ad[2,0]*tp0_0 + Ad[2,1]*tp0_1 + Ad[2,2]*tp0_2 + Ad[2,3]*tp0_3)
        Phi0_3 = (Ad[3,0]*tp0_0 + Ad[3,1]*tp0_1 + Ad[3,2]*tp0_2 + Ad[3,3]*tp0_3)
        
    Phi1_0 = 0.0
    Phi1_1 = 0.0
    Phi1_2 = 0.0
    Phi1_3 = 0.0

    if t1 < 0:
        Phi1_0 = dAd[0,3]*t1 + Ad[0,3]
        Phi1_1 = dAd[1,3]*t1 + Ad[1,3]
        Phi1_2 = dAd[2,3]*t1 + Ad[2,3]
        Phi1_3 = dAd[3,3]*t1 + Ad[3,3]
    elif t1 > 1:
        Phi1_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t1-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi1_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t1-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi1_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t1-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi1_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t1-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi1_0 = (Ad[0,0]*tp1_0 + Ad[0,1]*tp1_1 + Ad[0,2]*tp1_2 + Ad[0,3]*tp1_3)
        Phi1_1 = (Ad[1,0]*tp1_0 + Ad[1,1]*tp1_1 + Ad[1,2]*tp1_2 + Ad[1,3]*tp1_3)
        Phi1_2 = (Ad[2,0]*tp1_0 + Ad[2,1]*tp1_1 + Ad[2,2]*tp1_2 + Ad[2,3]*tp1_3)
        Phi1_3 = (Ad[3,0]*tp1_0 + Ad[3,1]*tp1_1 + Ad[3,2]*tp1_2 + Ad[3,3]*tp1_3)
        
    Phi2_0 = 0.0
    Phi2_1 = 0.0
    Phi2_2 = 0.0
    Phi2_3 = 0.0

    if t2 < 0:
        Phi2_0 = dAd[0,3]*t2 + Ad[0,3]
        Phi2_1 = dAd[1,3]*t2 + Ad[1,3]
        Phi2_2 = dAd[2,3]*t2 + Ad[2,3]
        Phi2_3 = dAd[3,3]*t2 + Ad[3,3]
    elif t2 > 1:
        Phi2_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t2-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
        Phi2_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t2-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
        Phi2_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t2-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
        Phi2_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t2-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
    else:
        Phi2_0 = (Ad[0,0]*tp2_0 + Ad[0,1]*tp2_1 + Ad[0,2]*tp2_2 + Ad[0,3]*tp2_3)
        Phi2_1 = (Ad[1,0]*tp2_0 + Ad[1,1]*tp2_1 + Ad[1,2]*tp2_2 + Ad[1,3]*tp2_3)
        Phi2_2 = (Ad[2,0]*tp2_0 + Ad[2,1]*tp2_1 + Ad[2,2]*tp2_2 + Ad[2,3]*tp2_3)
        Phi2_3 = (Ad[3,0]*tp2_0 + Ad[3,1]*tp2_1 + Ad[3,2]*tp2_2 + Ad[3,3]*tp2_3)
    
    for n in range(n_vals):
        vals[n] = Phi0_0*(Phi1_0*(Phi2_0*(coefs[n,i0+0,i1+0,i2+0]) + Phi2_1*(coefs[n,i0+0,i1+0,i2+1]) + Phi2_2*(coefs[n,i0+0,i1+0,i2+2]) + Phi2_3*(coefs[n,i0+0,i1+0,i2+3])) + Phi1_1*(Phi2_0*(coefs[n,i0+0,i1+1,i2+0]) + Phi2_1*(coefs[n,i0+0,i1+1,i2+1]) + Phi2_2*(coefs[n,i0+0,i1+1,i2+2]) + Phi2_3*(coefs[n,i0+0,i1+1,i2+3])) + Phi1_2*(Phi2_0*(coefs[n,i0+0,i1+2,i2+0]) + Phi2_1*(coefs[n,i0+0,i1+2,i2+1]) + Phi2_2*(coefs[n,i0+0,i1+2,i2+2]) + Phi2_3*(coefs[n,i0+0,i1+2,i2+3])) + Phi1_3*(Phi2_0*(coefs[n,i0+0,i1+3,i2+0]) + Phi2_1*(coefs[n,i0+0,i1+3,i2+1]) + Phi2_2*(coefs[n,i0+0,i1+3,i2+2]) + Phi2_3*(coefs[n,i0+0,i1+3,i2+3]))) + Phi0_1*(Phi1_0*(Phi2_0*(coefs[n,i0+1,i1+0,i2+0]) + Phi2_1*(coefs[n,i0+1,i1+0,i2+1]) + Phi2_2*(coefs[n,i0+1,i1+0,i2+2]) + Phi2_3*(coefs[n,i0+1,i1+0,i2+3])) + Phi1_1*(Phi2_0*(coefs[n,i0+1,i1+1,i2+0]) + Phi2_1*(coefs[n,i0+1,i1+1,i2+1]) + Phi2_2*(coefs[n,i0+1,i1+1,i2+2]) + Phi2_3*(coefs[n,i0+1,i1+1,i2+3])) + Phi1_2*(Phi2_0*(coefs[n,i0+1,i1+2,i2+0]) + Phi2_1*(coefs[n,i0+1,i1+2,i2+1]) + Phi2_2*(coefs[n,i0+1,i1+2,i2+2]) + Phi2_3*(coefs[n,i0+1,i1+2,i2+3])) + Phi1_3*(Phi2_0*(coefs[n,i0+1,i1+3,i2+0]) + Phi2_1*(coefs[n,i0+1,i1+3,i2+1]) + Phi2_2*(coefs[n,i0+1,i1+3,i2+2]) + Phi2_3*(coefs[n,i0+1,i1+3,i2+3]))) + Phi0_2*(Phi1_0*(Phi2_0*(coefs[n,i0+2,i1+0,i2+0]) + Phi2_1*(coefs[n,i0+2,i1+0,i2+1]) + Phi2_2*(coefs[n,i0+2,i1+0,i2+2]) + Phi2_3*(coefs[n,i0+2,i1+0,i2+3])) + Phi1_1*(Phi2_0*(coefs[n,i0+2,i1+1,i2+0]) + Phi2_1*(coefs[n,i0+2,i1+1,i2+1]) + Phi2_2*(coefs[n,i0+2,i1+1,i2+2]) + Phi2_3*(coefs[n,i0+2,i1+1,i2+3])) + Phi1_2*(Phi2_0*(coefs[n,i0+2,i1+2,i2+0]) + Phi2_1*(coefs[n,i0+2,i1+2,i2+1]) + Phi2_2*(coefs[n,i0+2,i1+2,i2+2]) + Phi2_3*(coefs[n,i0+2,i1+2,i2+3])) + Phi1_3*(Phi2_0*(coefs[n,i0+2,i1+3,i2+0]) + Phi2_1*(coefs[n,i0+2,i1+3,i2+1]) + Phi2_2*(coefs[n,i0+2,i1+3,i2+2]) + Phi2_3*(coefs[n,i0+2,i1+3,i2+3]))) + Phi0_3*(Phi1_0*(Phi2_0*(coefs[n,i0+3,i1+0,i2+0]) + Phi2_1*(coefs[n,i0+3,i1+0,i2+1]) + Phi2_2*(coefs[n,i0+3,i1+0,i2+2]) + Phi2_3*(coefs[n,i0+3,i1+0,i2+3])) + Phi1_1*(Phi2_0*(coefs[n,i0+3,i1+1,i2+0]) + Phi2_1*(coefs[n,i0+3,i1+1,i2+1]) + Phi2_2*(coefs[n,i0+3,i1+1,i2+2]) + Phi2_3*(coefs[n,i0+3,i1+1,i2+3])) + Phi1_2*(Phi2_0*(coefs[n,i0+3,i1+2,i2+0]) + Phi2_1*(coefs[n,i0+3,i1+2,i2+1]) + Phi2_2*(coefs[n,i0+3,i1+2,i2+2]) + Phi2_3*(coefs[n,i0+3,i1+2,i2+3])) + Phi1_3*(Phi2_0*(coefs[n,i0+3,i1+3,i2+0]) + Phi2_1*(coefs[n,i0+3,i1+3,i2+1]) + Phi2_2*(coefs[n,i0+3,i1+3,i2+2]) + Phi2_3*(coefs[n,i0+3,i1+3,i2+3])))

    return 0

# @jit("int64( double[:], double[:], int64[:], double[:,:,:,:,:], double[:], double[:], double[:,:], double[:,:])") #, device=True, target='gpu') 
# def eval_cubic_multi_spline_4(smin, smax, orders, coefs, svec, vals, Ad, dAd):

#    n_vals = vals.shape[0]
       
#    M0 = orders[0]
#    start0 = smin[0]
#    dinv0 = (orders[0]-1.0)/(smax[0]-smin[0])
#    M1 = orders[1]
#    start1 = smin[1]
#    dinv1 = (orders[1]-1.0)/(smax[1]-smin[1])
#    M2 = orders[2]
#    start2 = smin[2]
#    dinv2 = (orders[2]-1.0)/(smax[2]-smin[2])
#    M3 = orders[3]
#    start3 = smin[3]
#    dinv3 = (orders[3]-1.0)/(smax[3]-smin[3])
#    x0 = svec[0]
#    x1 = svec[1]
#    x2 = svec[2]
#    x3 = svec[3]
#    u0 = (x0 - start0)*dinv0
#    i0 = int( floor( u0 ) )
#    i0 = max( min(i0,M0-2), 0 )
#    t0 = u0-i0
#    u1 = (x1 - start1)*dinv1
#    i1 = int( floor( u1 ) )
#    i1 = max( min(i1,M1-2), 0 )
#    t1 = u1-i1
#    u2 = (x2 - start2)*dinv2
#    i2 = int( floor( u2 ) )
#    i2 = max( min(i2,M2-2), 0 )
#    t2 = u2-i2
#    u3 = (x3 - start3)*dinv3
#    i3 = int( floor( u3 ) )
#    i3 = max( min(i3,M3-2), 0 )
#    t3 = u3-i3
#    tp0_0 = t0*t0*t0;  tp0_1 = t0*t0;  tp0_2 = t0;  tp0_3 = 1.0;
#    tp1_0 = t1*t1*t1;  tp1_1 = t1*t1;  tp1_2 = t1;  tp1_3 = 1.0;
#    tp2_0 = t2*t2*t2;  tp2_1 = t2*t2;  tp2_2 = t2;  tp2_3 = 1.0;
#    tp3_0 = t3*t3*t3;  tp3_1 = t3*t3;  tp3_2 = t3;  tp3_3 = 1.0;
       
#    Phi0_0 = 0.0
#    Phi0_1 = 0.0
#    Phi0_2 = 0.0
#    Phi0_3 = 0.0

#    if t0 < 0:
#        Phi0_0 = dAd[0,3]*t0 + Ad[0,3]
#        Phi0_1 = dAd[1,3]*t0 + Ad[1,3]
#        Phi0_2 = dAd[2,3]*t0 + Ad[2,3]
#        Phi0_3 = dAd[3,3]*t0 + Ad[3,3]
#    elif t0 > 1:
#        Phi0_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t0-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
#        Phi0_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t0-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
#        Phi0_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t0-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
#        Phi0_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t0-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
#    else:
#        Phi0_0 = (Ad[0,0]*tp0_0 + Ad[0,1]*tp0_1 + Ad[0,2]*tp0_2 + Ad[0,3]*tp0_3)
#        Phi0_1 = (Ad[1,0]*tp0_0 + Ad[1,1]*tp0_1 + Ad[1,2]*tp0_2 + Ad[1,3]*tp0_3)
#        Phi0_2 = (Ad[2,0]*tp0_0 + Ad[2,1]*tp0_1 + Ad[2,2]*tp0_2 + Ad[2,3]*tp0_3)
#        Phi0_3 = (Ad[3,0]*tp0_0 + Ad[3,1]*tp0_1 + Ad[3,2]*tp0_2 + Ad[3,3]*tp0_3)
       
#    Phi1_0 = 0.0
#    Phi1_1 = 0.0
#    Phi1_2 = 0.0
#    Phi1_3 = 0.0

#    if t1 < 0:
#        Phi1_0 = dAd[0,3]*t1 + Ad[0,3]
#        Phi1_1 = dAd[1,3]*t1 + Ad[1,3]
#        Phi1_2 = dAd[2,3]*t1 + Ad[2,3]
#        Phi1_3 = dAd[3,3]*t1 + Ad[3,3]
#    elif t1 > 1:
#        Phi1_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t1-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
#        Phi1_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t1-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
#        Phi1_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t1-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
#        Phi1_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t1-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
#    else:
#        Phi1_0 = (Ad[0,0]*tp1_0 + Ad[0,1]*tp1_1 + Ad[0,2]*tp1_2 + Ad[0,3]*tp1_3)
#        Phi1_1 = (Ad[1,0]*tp1_0 + Ad[1,1]*tp1_1 + Ad[1,2]*tp1_2 + Ad[1,3]*tp1_3)
#        Phi1_2 = (Ad[2,0]*tp1_0 + Ad[2,1]*tp1_1 + Ad[2,2]*tp1_2 + Ad[2,3]*tp1_3)
#        Phi1_3 = (Ad[3,0]*tp1_0 + Ad[3,1]*tp1_1 + Ad[3,2]*tp1_2 + Ad[3,3]*tp1_3)
       
#    Phi2_0 = 0.0
#    Phi2_1 = 0.0
#    Phi2_2 = 0.0
#    Phi2_3 = 0.0

#    if t2 < 0:
#        Phi2_0 = dAd[0,3]*t2 + Ad[0,3]
#        Phi2_1 = dAd[1,3]*t2 + Ad[1,3]
#        Phi2_2 = dAd[2,3]*t2 + Ad[2,3]
#        Phi2_3 = dAd[3,3]*t2 + Ad[3,3]
#    elif t2 > 1:
#        Phi2_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t2-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
#        Phi2_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t2-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
#        Phi2_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t2-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
#        Phi2_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t2-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
#    else:
#        Phi2_0 = (Ad[0,0]*tp2_0 + Ad[0,1]*tp2_1 + Ad[0,2]*tp2_2 + Ad[0,3]*tp2_3)
#        Phi2_1 = (Ad[1,0]*tp2_0 + Ad[1,1]*tp2_1 + Ad[1,2]*tp2_2 + Ad[1,3]*tp2_3)
#        Phi2_2 = (Ad[2,0]*tp2_0 + Ad[2,1]*tp2_1 + Ad[2,2]*tp2_2 + Ad[2,3]*tp2_3)
#        Phi2_3 = (Ad[3,0]*tp2_0 + Ad[3,1]*tp2_1 + Ad[3,2]*tp2_2 + Ad[3,3]*tp2_3)
       
#    Phi3_0 = 0.0
#    Phi3_1 = 0.0
#    Phi3_2 = 0.0
#    Phi3_3 = 0.0

#    if t3 < 0:
#        Phi3_0 = dAd[0,3]*t3 + Ad[0,3]
#        Phi3_1 = dAd[1,3]*t3 + Ad[1,3]
#        Phi3_2 = dAd[2,3]*t3 + Ad[2,3]
#        Phi3_3 = dAd[3,3]*t3 + Ad[3,3]
#    elif t3 > 1:
#        Phi3_0 = (3*Ad[0,0] + 2*Ad[0,1] + Ad[0,2])*(t3-1) + (Ad[0,0]+Ad[0,1]+Ad[0,2]+Ad[0,3])
#        Phi3_1 = (3*Ad[1,0] + 2*Ad[1,1] + Ad[1,2])*(t3-1) + (Ad[1,0]+Ad[1,1]+Ad[1,2]+Ad[1,3])
#        Phi3_2 = (3*Ad[2,0] + 2*Ad[2,1] + Ad[2,2])*(t3-1) + (Ad[2,0]+Ad[2,1]+Ad[2,2]+Ad[2,3])
#        Phi3_3 = (3*Ad[3,0] + 2*Ad[3,1] + Ad[3,2])*(t3-1) + (Ad[3,0]+Ad[3,1]+Ad[3,2]+Ad[3,3])
#    else:
#        Phi3_0 = (Ad[0,0]*tp3_0 + Ad[0,1]*tp3_1 + Ad[0,2]*tp3_2 + Ad[0,3]*tp3_3)
#        Phi3_1 = (Ad[1,0]*tp3_0 + Ad[1,1]*tp3_1 + Ad[1,2]*tp3_2 + Ad[1,3]*tp3_3)
#        Phi3_2 = (Ad[2,0]*tp3_0 + Ad[2,1]*tp3_1 + Ad[2,2]*tp3_2 + Ad[2,3]*tp3_3)
#        Phi3_3 = (Ad[3,0]*tp3_0 + Ad[3,1]*tp3_1 + Ad[3,2]*tp3_2 + Ad[3,3]*tp3_3)
   
#    for n in range(n_vals):
#        vals[n] = Phi0_0*(Phi1_0*(Phi2_0*(Phi3_0*(coefs[n,i0+0,i1+0,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+0,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+0,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+0,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+0,i1+0,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+0,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+0,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+0,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+0,i1+0,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+0,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+0,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+0,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+0,i1+0,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+0,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+0,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+0,i2+3,i3+3]))) + Phi1_1*(Phi2_0*(Phi3_0*(coefs[n,i0+0,i1+1,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+1,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+1,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+1,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+0,i1+1,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+1,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+1,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+1,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+0,i1+1,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+1,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+1,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+1,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+0,i1+1,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+1,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+1,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+1,i2+3,i3+3]))) + Phi1_2*(Phi2_0*(Phi3_0*(coefs[n,i0+0,i1+2,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+2,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+2,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+2,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+0,i1+2,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+2,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+2,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+2,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+0,i1+2,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+2,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+2,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+2,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+0,i1+2,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+2,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+2,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+2,i2+3,i3+3]))) + Phi1_3*(Phi2_0*(Phi3_0*(coefs[n,i0+0,i1+3,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+3,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+3,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+3,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+0,i1+3,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+3,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+3,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+3,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+0,i1+3,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+3,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+3,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+3,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+0,i1+3,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+0,i1+3,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+0,i1+3,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+0,i1+3,i2+3,i3+3])))) + Phi0_1*(Phi1_0*(Phi2_0*(Phi3_0*(coefs[n,i0+1,i1+0,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+0,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+0,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+0,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+1,i1+0,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+0,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+0,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+0,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+1,i1+0,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+0,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+0,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+0,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+1,i1+0,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+0,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+0,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+0,i2+3,i3+3]))) + Phi1_1*(Phi2_0*(Phi3_0*(coefs[n,i0+1,i1+1,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+1,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+1,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+1,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+1,i1+1,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+1,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+1,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+1,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+1,i1+1,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+1,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+1,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+1,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+1,i1+1,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+1,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+1,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+1,i2+3,i3+3]))) + Phi1_2*(Phi2_0*(Phi3_0*(coefs[n,i0+1,i1+2,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+2,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+2,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+2,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+1,i1+2,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+2,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+2,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+2,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+1,i1+2,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+2,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+2,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+2,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+1,i1+2,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+2,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+2,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+2,i2+3,i3+3]))) + Phi1_3*(Phi2_0*(Phi3_0*(coefs[n,i0+1,i1+3,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+3,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+3,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+3,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+1,i1+3,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+3,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+3,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+3,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+1,i1+3,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+3,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+3,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+3,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+1,i1+3,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+1,i1+3,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+1,i1+3,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+1,i1+3,i2+3,i3+3])))) + Phi0_2*(Phi1_0*(Phi2_0*(Phi3_0*(coefs[n,i0+2,i1+0,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+0,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+0,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+0,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+2,i1+0,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+0,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+0,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+0,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+2,i1+0,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+0,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+0,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+0,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+2,i1+0,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+0,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+0,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+0,i2+3,i3+3]))) + Phi1_1*(Phi2_0*(Phi3_0*(coefs[n,i0+2,i1+1,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+1,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+1,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+1,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+2,i1+1,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+1,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+1,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+1,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+2,i1+1,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+1,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+1,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+1,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+2,i1+1,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+1,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+1,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+1,i2+3,i3+3]))) + Phi1_2*(Phi2_0*(Phi3_0*(coefs[n,i0+2,i1+2,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+2,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+2,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+2,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+2,i1+2,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+2,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+2,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+2,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+2,i1+2,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+2,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+2,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+2,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+2,i1+2,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+2,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+2,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+2,i2+3,i3+3]))) + Phi1_3*(Phi2_0*(Phi3_0*(coefs[n,i0+2,i1+3,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+3,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+3,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+3,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+2,i1+3,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+3,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+3,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+3,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+2,i1+3,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+3,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+3,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+3,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+2,i1+3,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+2,i1+3,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+2,i1+3,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+2,i1+3,i2+3,i3+3])))) + Phi0_3*(Phi1_0*(Phi2_0*(Phi3_0*(coefs[n,i0+3,i1+0,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+0,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+0,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+0,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+3,i1+0,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+0,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+0,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+0,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+3,i1+0,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+0,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+0,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+0,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+3,i1+0,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+0,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+0,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+0,i2+3,i3+3]))) + Phi1_1*(Phi2_0*(Phi3_0*(coefs[n,i0+3,i1+1,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+1,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+1,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+1,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+3,i1+1,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+1,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+1,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+1,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+3,i1+1,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+1,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+1,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+1,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+3,i1+1,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+1,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+1,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+1,i2+3,i3+3]))) + Phi1_2*(Phi2_0*(Phi3_0*(coefs[n,i0+3,i1+2,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+2,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+2,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+2,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+3,i1+2,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+2,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+2,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+2,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+3,i1+2,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+2,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+2,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+2,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+3,i1+2,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+2,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+2,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+2,i2+3,i3+3]))) + Phi1_3*(Phi2_0*(Phi3_0*(coefs[n,i0+3,i1+3,i2+0,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+3,i2+0,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+3,i2+0,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+3,i2+0,i3+3])) + Phi2_1*(Phi3_0*(coefs[n,i0+3,i1+3,i2+1,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+3,i2+1,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+3,i2+1,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+3,i2+1,i3+3])) + Phi2_2*(Phi3_0*(coefs[n,i0+3,i1+3,i2+2,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+3,i2+2,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+3,i2+2,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+3,i2+2,i3+3])) + Phi2_3*(Phi3_0*(coefs[n,i0+3,i1+3,i2+3,i3+0]) + Phi3_1*(coefs[n,i0+3,i1+3,i2+3,i3+1]) + Phi3_2*(coefs[n,i0+3,i1+3,i2+3,i3+2]) + Phi3_3*(coefs[n,i0+3,i1+3,i2+3,i3+3]))))

#    return 0

