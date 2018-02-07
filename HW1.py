##Initial code courtesy of Daniel Garrett

from HW1_additions import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as an
from matplotlib import rc

def mapping(x,y,l,target=0.01,n=15,k=1.5):
    '''This function returns successive mappings of (3.7.1) for coordinates x
    and y as arrays.
    
    Args:
        x (float or ndarray): initial point(s) in x (same shape as y)
        y (float or ndarray): initial point(s) in y (same shape as x)
        n (int): number of iterations of map
        k (float): parameter in the map
        
    Returns:
        xns (ndarray): each iteration of map in x as rows
        yns (ndarray): each iteration of map in y as rows
    
    '''
    
    if not isinstance(x,np.ndarray):
        x = np.array(x,copy=False,ndmin=1)
    if not isinstance(y,np.ndarray):
        y = np.array(y,copy=False,ndmin=1)
    
    # make sure x and y are same shape
    assert x.shape == y.shape, 'initial x and y must have same shape'
    
    # perform iterations of mapping
    xn = active_region(x, l)
    yn = active_region(y, l)
    xns = x[:]
    yns = y[:]
    for i in xrange(n):
        yn1 = yn + k*xn*(xn-1.)
        xn1 = xn + yn1

        #New: rescaling
#        xn, yn = prune(xn, yn)
        xn1 = np.hstack((xns[-1:], xn1))
        yn1 = np.hstack((yns[-1:], yn1))
        xn1, yn1 = rescale(xn1, yn1, target)
        xn1 = xn1[1:]
        yn1 = yn1[1:]
 
       
        #Changed 'vstack' to 'hstack' -- makes plotting more straightforward
        xns = np.hstack((xns,xn1))
        yns = np.hstack((yns,yn1))
        
        yn = yn1[:]
        xn = xn1[:]
    
    return xns, yns

def invmapping(x,y,l,target=0.01,n=15,k=1.5):
    '''This function returns successive mappings of (3.7.4) (inverse map of
    (3.7.1)) for coordinates x and y as arrays.
    
    Args:
        x (float or ndarray): initial point(s) in x (same shape as y)
        y (float or ndarray): initial point(s) in y (same shape as x)
        n (int): number of iterations of map
        k (float): parameter in the map
        
    Returns:
        xns (ndarray): each iteration of map in x as rows
        yns (ndarray): each iteration of map in y as rows
    
    '''
    if not isinstance(x,np.ndarray):
        x = np.array(x,copy=False,ndmin=1)
    if not isinstance(y,np.ndarray):
        y = np.array(y,copy=False,ndmin=1)
    
    # make sure x and y are same shape
    assert x.shape == y.shape, 'initial x and y must have same shape'
    
    xn1 = active_region(x, l)
    yn1 = active_region(y, l)
    xns = x[:]
    yns = y[:]
    for i in xrange(n):
        xn = xn1 - yn1
        yn = yn1 - k*xn*(xn-1.)
        
        #New: rescaling
#        xn, yn = prune(xn, yn)
        xn = np.hstack((xns[-1:], xn))
        yn = np.hstack((yns[-1:], yn))
        xn, yn = rescale(xn, yn, target)
        xn = xn[1:]
        yn = yn[1:]
#        plt.plot(xn, yn)
#        plt.show()
        
        #Changed 'vstack' to 'hstack' -- makes plotting more straightforward
        xns = np.hstack((xns,xn))
        yns = np.hstack((yns,yn))
        
        xn1 = xn[:]
        yn1 = yn[:]
    
    return xns, yns

def gen_stable_unstable_values(k,n,res=50,target=0.01):
    '''Generates (xn,yn)  by creating 100 points on an interval of length 
    0.0001 near the saddle point (1,0) and iterates for stable and unstable 
    manifolds for the mapping (3.7.1) and inverse mapping (3.7.4)
    
    Args:
        k (float): value of k parameter
        n (int): number of iterations to perform
    
    Returns:
        xu (ndarray): array of xn iterates for unstable manifold, t>0
        yu (ndarray): array of yn iterates for unstable manifold, t>0
        xs (ndarray): array of xn iterates for stable manifold, t<0
        ys (ndarray): array of yn iterates for stable manifold, t<0
    
    '''
    l = np.linspace(0.,0.0001/2.,res)
    #lambda values
    l1 = (2+k+np.sqrt(k*(k+4.)))/2
    l2 = (2+k-np.sqrt(k*(k+4.)))/2
    # unstable manifold points
    cu = (-k+np.sqrt(k*(k+4.)))/2.
    uu = l/np.sqrt(cu**1+1.)
    vu = cu*uu
    x0u = 1.-uu
    y0u = -vu
    ns = n
    xu,yu = mapping(x0u,y0u,l1,target,n=ns,k=k)
    # stable manifold points
    cs = (-k-np.sqrt(k*(k+4.)))/2.
    us = l/np.sqrt(cs**2+1.)
    vs = cs*us
    x0s = 1.-us
    y0s = -vs
    xs,ys = invmapping(x0s,y0s,l2,target,n=ns,k=k)
    
    return xu, yu, xs, ys

def kplot(k,n,res=50,target=0.01,sym='.'):
    '''Takes value for k and generates a plot of the stable and unstable
    manifolds for the mapping (3.7.1) and inverse mapping (3.7.4)
    
    Args:
        k (float): value of k parameter
        n (int): number of iterations to perform
    
    Returns:
        fig: matplotlib.pyplot figure object
        
    '''
    xu, yu, xs, ys = gen_stable_unstable_values(k,n,res,target)
    
    fig, ax = plt.subplots()
    ax.plot(xu,yu,'r'+sym,label=r'Unstable Manifold')
    ax.plot(xs,ys,'b'+sym,label=r'Stable Manifold')
#    ax.plot([-0.3676], [0.0014], 'ko', label=r'Original Homoclinic Point')
    ax.legend(fontsize=14,loc='upper right')
    ax.set_ylim(ymin=-2.,ymax=2.)
    ax.set_xlim(xmin=-1.,xmax=3.)
    ax.set_xlabel(r'x',fontsize=14)
    ax.set_ylabel(r'y',fontsize=14)
    ax.set_title(r'Homoclinic Tangle k = {}'.format(k),fontsize=16)
    
    return fig

"""
def gen_animation(k,n):
    '''Takes value for k and generates an animation of the stable and unstable
    manifolds for the mapping (3.7.1) and inverse mapping (3.7.4) for t>0
    
    Args:
        k (float): value of k parameter
    
    Returns:
        anim: matplotlib.animation.FuncAnimation object
    
    '''
    xu, yu, xs, ys = gen_stable_unstable_values(k,n)
    fig = plt.figure()
    ax = fig.add_subplot(111,xlim=(-1.,3.),ylim=(-2.,2.))
    upoints, = ax.plot([],[],'rx',label=r'Unstable Manifold')
    spoints, = ax.plot([],[],'b.',label=r'Stable Manifold')
    ax.legend(fontsize=14,loc='upper right')
    ax.set_title(r'Homoclinic Tangle k = {}, t > 0'.format(k),fontsize=16)
    ax.set_xlabel(r'x',fontsize=14)
    ax.set_ylabel(r'y',fontsize=14)
    iter_text = ax.text(0.02, 0.90, '', transform=ax.transAxes,fontsize=14)
    def init():
        upoints.set_data([],[])
        spoints.set_data([],[])
        iter_text.set_text('')
        return upoints, spoints, iter_text
    
    def animate(i):
        upoints.set_data(xu[i,:],yu[i,:])
        spoints.set_data(xs[-1-i,:],ys[-1-i,:])
        iter_text.set_text('Iteration: {}'.format(i))
        return upoints, spoints, iter_text
    
    anim = an.FuncAnimation(fig,animate,init_func=init,frames=n+1,interval=500,blit=True)
    #HTML(anim.to_html5_video())
    return anim

rc('animation', html='html5')
"""

