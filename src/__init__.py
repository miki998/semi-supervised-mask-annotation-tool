import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
from scipy import ndimage
import pylab
from skimage.color import rgb2gray
from copy import deepcopy
from tqdm import tqdm


##################IMAGE-PLOTTING#####################

def plot_levelset(Z, level=0, f=[]):
    """
    f is supposed to be of the same shape as Z
    f, Z : (nr,nc)
    Plot contour Z, on he same plot as the original image f, and print level of value 0 in red.
    """
    if len(f) == 0:
        f = np.copy(Z)
        
    n,p = np.shape(Z)
    X,Y = np.meshgrid(np.arange(0,p),np.arange(0,n))
    plt.contour(X, Y, Z,[level],linewidths=2, colors="red")
    imgplot = plt.imshow(f, interpolation='nearest')
    imgplot.set_cmap('gray')
    pylab.axis('off')
    
def initialization_square(I_gray,center,c):
    nr,nc = I_gray.shape
    n = nr
    Y,X = np.meshgrid(np.arange(1,n+1), np.arange(1,n+1))
    phi0 = np.maximum(abs(X-center[0]), abs(Y-center[1])) - c
    return phi0


def image_padding():
	#We also add padding at the beginning
	nr,nc = I_gray.shape
	new_I = np.hstack((I_gray,np.zeros((padnb,nr)).T))
	new_I = np.concatenate((new_I,np.zeros((padnb,nc+padnb))))

	new_I = np.hstack((np.zeros((padnb,nr+padnb)).T,new_I))
	nr,nc = new_I.shape
	new_I = np.concatenate((np.zeros((padnb,nr+padnb)),new_I))

	nr,nc = new_I.shape
  

#################COMPUTATION#########################

def W_map():
	pass

def grad(phi,v=2):
    #Apparently backward euler is enough for this task
    #central differences for gradient image
    if v==1:
        nr,nc = phi.shape
        gx = np.zeros((nr,nc))
        gy = np.zeros((nr,nc))
        gx[1:] = phi[1:] - phi[:-1]
        gy[:,1:] = phi[:,1:] - phi[:,:-1]
    
    else:
        nr,nc = phi.shape
        padx = np.array([np.zeros(nc)]) 
        pady = np.array([np.zeros(nr)])

        paddedx1 = np.concatenate((phi[1:,:],padx))
        paddedx2 = np.concatenate((padx,phi[:-1,:]))
        gx = (paddedx1-paddedx2)/2.

        paddedy1 = np.hstack((phi[:,1:],pady.T))
        paddedy2 = np.hstack((pady.T,phi[:,:-1]))
        gy = (paddedy1-paddedy2)/2.
        
    return gx,gy

def div(gx,gy,v=2):
    gxx,_ = grad(gx,v=2)
    _,gyy = grad(gy,v=2)
    
    return gxx+gyy


def mean_curv(phi0,tau,Tmax,I0,v=2):
    '''
    phi0 : your initial shape, size (nr,nc)
    tau : time step size, > 0, be careful to not have a too big time step !
    Tmax : maximum time of evolution
    I0 : your image to segment
    ------
    returns phi, contour matrix (nr,nc)
    
    '''
    def G(Phi,v=2):
    	#we compute here the function G
    	nr,nc = Phi.shape
    	g_phix,g_phiy = grad(Phi,v)
    	n_phi = np.sqrt(g_phix**2+g_phiy**2)
    	eps = 10E-10
    	#to avoid division by 0
    	n_phi = np.maximum(eps*np.ones((g_phix.shape[0],g_phix.shape[1])),n_phi)
    	g_phix, g_phiy = g_phix/n_phi, g_phiy/n_phi

    	K = - n_phi*div(g_phix, g_phiy,v)
    	return K

    phi = deepcopy(phi0)
    for i in range(int(Tmax//tau)):
        phi = phi - tau*G(phi,v)
    return phi



def geo_curv(phi0,tau,Tmax,I0,W):
    '''
    phi0 : your initial shape, size (nr,nc)
    tau : time step size, > 0, be careful to not have a too big time step !
    Tmax : maximum time of evolution
    I0 : your image to segment
    ------
    returns phi, contour matrix (nr,nc)
    
    '''

    nr,nc = I0.shape
    niter = int(Tmax/tau)
    phi = np.copy(phi0)
    k = 0
    gwx,gwy = grad(W)

    empirical = 10
    for i in tqdm(range(1,niter+1)):
        gx,gy = grad(phi)
        eps = 10E-10
        n_phi = np.maximum(eps*np.ones([nr,nc]), np.sqrt(gx**2+gy**2))
        g_phix,g_phiy = gx/n_phi,gy/n_phi
        G = - W*n_phi*div(g_phix, g_phiy) + gx*gwx + gy*gwy
        phi = phi - tau*G
        
        if (i % 25) == 0:
            phi[-1,:] = eps*empirical #you can  pad to the original image so to have this phi = 0 ignored
            phi[0,:] = eps*empirical
            phi[:,0] = eps*empirical
            phi[:,-1] = eps*empirical
        
    return phi