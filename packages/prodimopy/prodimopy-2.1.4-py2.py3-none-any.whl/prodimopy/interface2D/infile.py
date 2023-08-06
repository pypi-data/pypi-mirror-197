'''
Created on 7 Sep 2022

@author: rab
'''

import numpy as np

# FIXME: not nice, but use the au to cm conversion constant from ProDiMo
# just to be consisten
autocm=1.495978700e+13


class Interface2Din(object):
  '''
  Some utility class to generate input files for the ProDiMo 2D interface.

  THIS IS STILL HIGHLY EXPERIMENTAL!

  '''

  def __init__(self,x,z,nHtot,vx,vy,vz,gd=None):
    self.x=x
    ''' array_like(dim=(nx,nz)) :
      x coordinates in cm
    '''
    self.z=z
    ''' array_like(dim=(nx,nz)) :
      z coordinates in cm
    '''
    self.nHtot=nHtot
    ''' array_like(dim=(nx,nz)) :
      total hydrogen number density
    '''
    self.vx=vx
    ''' array_like(dim=(nx,nz)) :
      velocity in x direction in cm/s
    '''
    self.vy=vy
    ''' array_like(dim=(nx,nz)) :
      velocity in y direction in cm/s
    '''
    self.vz=vz
    ''' array_like(dim=(nx,nz)) :
      velocity in z direction in cm/s
    '''
    self.gd=gd
    ''' array_like(dim=(nx,nz)) :
      gas to dust mass ratio at every point
    '''

    self.nx=x.shape[0]
    self.nz=x.shape[1]

  def toProDiMo(self,pmodel,outdir=".",imethod="linear"):
    '''
    Interpolates the given density/velocity structure onto the ProDiMo grid and writes
    the intput files for ProDimo.

    .. todo:

       - make it general (e.g. file names)

    '''
    from scipy.interpolate import griddata

    points=np.array([self.x.flatten()/autocm,self.z.flatten()/autocm]).T

    print(self.x.shape,self.z.shape,self.nHtot.shape,points.shape)

    # can only use nearest, because griddata does not extrapolatoin ... and that causes problems

    # f = interpolate.interp2d(self.x.flatten()/AU, self.z.flatten()/AU, self.nHtot.flatten(), kind='linear',copy=False)
    # pnHtot=f(pmodel.x.flatten(),pmodel.z.flatten())

    pnHtot=griddata(points,self.nHtot.flatten(),(pmodel.x,pmodel.z),method=imethod)
    pvx=griddata(points,self.vx.flatten(),(pmodel.x,pmodel.z),method=imethod)
    pvy=griddata(points,self.vy.flatten(),(pmodel.x,pmodel.z),method=imethod)
    pvz=griddata(points,self.vz.flatten(),(pmodel.x,pmodel.z),method=imethod)

    # assumes grid is from spherical so height cannot be larger then the radius
    # make some cutoff grid from spherical coordinates so height cannot be larger then the radius
    cutoff=np.max(self.x)/autocm
    print(cutoff)
    # print(pmodel.z)

    nz=len(pmodel.z[0,:])
    nx=len(pmodel.x[:,0])

    # Make sure the the midplane is filled
    # Another security check ... seems that in some grids the z=0 coordinate has Nhtot= or close to zero fis that
    # check if it all the points are or close to zero in the midplane.
#     if np.all(pnHtot[:,0]<1.e-2):
#       print("Fixing midplane ...")
#       pnHtot[:,0]=pnHtot[:,1]

    # Make sure that the outermost radial disk point is not empty
    # print(pnHtot[nx-1,0])
    if np.isnan(pnHtot[nx-1,0]):
      print("fix outer vertical column: ")
      for arr in [pnHtot,pvx,pvy,pvz]:
        # print(arr[nx-1,0],arr[nx-2,0])
        arr[nx-1,:]=arr[nx-2,:]

    cutmask=pmodel.z>(cutoff*1.1)
    for arr in [pnHtot,pvx,pvy,pvz]:
      arr[cutmask]=0.0

      if (np.isnan(arr).any()):
        print("Found NaNs set them to zero.")
        arr[np.isnan(arr)]=0.0

    # fix some stuff in the innner region ... because of the spherical grid of MOCASSIN/PLUTO
    #
    for ix in range(nx):
      # print(ix)
      izmax=np.min((nz-2,np.argmin(np.abs(pmodel.z[ix,:]-0.15))))
      # print("izmax: ",izmax)
      # print(izmax)
      for iz in range(izmax,-1,-1):  # from top to bottom
        # print(ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz])
        if pnHtot[ix,iz]<pnHtot[ix,iz+1]:
          print("Fix: ",ix,iz,pmodel.x[ix,iz],pmodel.z[ix,iz],"{:15.5e}".format(pnHtot[ix,iz]),"{:15.5e}".format(pnHtot[ix,iz+1]))
          pnHtot[ix,iz]=pnHtot[ix,iz+1]
          pvx[ix,iz]=pvx[ix,iz+1]
          pvz[ix,iz]=pvz[ix,iz+1]
        # check explicitlz for vy
        if pvy[ix,iz]<pvy[ix,iz+1]:
          pvy[ix,iz]=pvy[ix,iz+1]

    # print(pnHtot[:,0])
    np.savetxt(outdir+"/pluto_dens.dat",pnHtot)
    np.savetxt(outdir+"/pluto_vx.dat",pvx)
    np.savetxt(outdir+"/pluto_vy.dat",pvy)
    np.savetxt(outdir+"/pluto_vz.dat",pvz)

    if self.gd is not None:
      imethod="linear"
      pgd=griddata(points,self.gd.flatten(),(pmodel.x,pmodel.z),method=imethod)
      np.savetxt(outdir+"/pluto_gd.dat",pgd)
