from typing import Tuple, Optional
import numpy as np
from ._tools import cart2pol, mask_baricenter

class PupilMask:
    """ 
    mask (array of boulean): True for pixel inside the pupil False otherwise 
    radius (float): Typical radius size in pixel  
    center (tuple): (x0, y0) pixel center of the pupil
    angle (float, optional): Pupil rotation in rad. This will be the rotation 
           of zernike mode inside the pupil 
    flip (tuple, optional): The pupil flip, the flip of the zernike modes 
           created inside the pupil: 
           Allowed flip are:
            - (1,1) : no flip (default)
            - (-1,1) : Zernike polynoms will be flipped on X axis 
            - (1,-1) : Zernike polynoms will be flipped on Y axis  
            - (-1,-1) : Zernike polynoms will be flipped on both axes
    """
    def __init__(self, 
            mask: np.ndarray, 
            radius: float, 
            center: Tuple[float,float], 
            angle: float = 0.0, 
            flip: Tuple[int,int] = (1,1)
        ):
        self.mask = mask
        self.radius = radius
        self.center = center
        self.angle = angle
        self.flip = flip 
    
    def reconstruct(self, phases: np.ndarray, outside_value: float=np.nan) -> np.ndarray:
        """ Reconstruct a pupill image from a vector of array of phase vector 
        
        The sum of the mask array shall be equal to the last dimension of the phases input array 
        This is usefull when phases has been build from :func:`zernpol.zernpol_pupil` with the 
        option `inpupil_only=True`
        
        Args:
            phases (array like) : numpy array of phases vector The sum of the mask array shall be 
                                  equal to the last dimension of the phases input array 
            outside_value (float, optional): value to fill the image array for point outside the pupil 
                                  default is np.nan
        Returns:
            images (array): the last two dimensions will be the dimension of the mask
            
        Example:
        
        ::
        
            >>> from zernpol import zernpol, PupilDisk, zernpol_pupil
            >>> from matplotlib.pylab import plt
            >>> import numpy as np 
            >>> disk = PupilDisk(20)
            >>> mask = disk.make_mask([100,100])
            >>> zs = zernpol_pupil( zernpol(range(1,6)), mask, inpupil_only=True)
            >>> imgs = mask.reconstruct(zs)
            >>> fig, axs = plt.subplots(2,2)
            >>> for ax,img in zip(axs.flat, imgs):
            >>>    ax.imshow(img)
            >>> fig.show()
            
        """
        phases = np.asarray(phases)
        img = np.ndarray( phases.shape[:-1]+self.mask.shape, dtype=phases.dtype)
        img[...] = outside_value
        img[...,self.mask] = phases
        return img    
    
    def deconstruct(self, images: np.ndarray):
        """ From a cube of images return an array of vector contained inside the pupil 
        
        Args:
            images (array like): The last two dimensions are y,x axis of the image 
            
        Returns:
            vectors (array): The dimension will be images.shape[:-2]+(sum(self.mask),)
        
        """
        images = np.asarray(images)
        return images[...,self.mask]        
        
class PupilDefinition:
    def make_mask(self, 
          mask_size: Tuple[int,int],
          scale: float = 1.0, 
          center: Optional[Tuple[float,float]] = None,
          angle:float = 0.0, 
          flip: Tuple[int,int] = (1,1)
        ) -> PupilMask:
        """ make a pupil mask image 
        
        Args:
            mask_size (tuple): (ny,nx) image size in pixel 
            scale (float): pixel scale in UserUnit/pixel
            center (tuple): (x0, y0) pixel center of the pupil
            angle (float, optional): Pupil rotation in rad. This will be the rotation 
                   of zernike mode inside the pupil 
            flip (tuple, optional): The pupil flip, the flip of the zernike modes 
                   created inside the pupil: 
                   Allowed flip are:
                    - (1,1) : no flip 
                    - (-1,1) : Zernike polynoms will be flipped on X axis 
                    - (1,-1) : Zernike polynoms will be flipped on Y axis  
                    - (-1,-1) : Zernike polynoms will be flipped on both axes          
        """
        raise NotImplementedError('make_mask')


class PupilDisk(PupilDefinition):
    """ Define a physical pupil as a full disk """
    def __init__(self, diameter):
        self.diameter = diameter
    
    def make_mask(self, 
          mask_size: Tuple[int,int],
          scale: float = 1.0, 
          center: Optional[Tuple[float,float]] = None,
          angle:float = 0.0, 
          flip: Tuple[int,int] = (1,1)
        ) -> PupilMask:
        
        nY, nX =  mask_size
        if center is None:
            cX, cY = nX/2.0, nX/2.0 
        else:
            cX, cY = center
            
        X, Y = np.meshgrid(np.arange(nX), np.arange(nY))
        r = self.diameter/2./scale
        mask = ( (X-cX)**2 + (Y-cY)**2 ) <= (r**2)
        return PupilMask(mask, r, (cX, cY), angle, flip)        


def mask_from_image(
      img: np.ndarray, 
      vmin: float = None, 
      vmax: float = None, 
      angle: float = 0.0, 
      flip: Tuple[int,int] = (1,1)
    ) -> PupilMask:
    """ Create a :class:`PupilMask` from an 2d image
     
    The image is mostlikely an phase screen image filled with nan values for point outside the 
    illuminated area. 
    The illumated area is expected to be a disk, its center is extracted by barycenter of the masked area
    and a typical radius is also estimated.
     
    Args:
        img (array)
    
    ::
       
       >>> from zernpol import zernpol, PupilDisk, mask_from_image
       >>> mask = PupilDisk(25).make_mask([100,100],center=(70,30))
       >>> img = zernpol(4).func_pupil(mask)
       >>> mask2 = mask_from_image(img)
       
    """
    img = np.asarray(img)
    if img.dtype == bool:
        mask = img
    else:
        mask = ~np.isnan(img)
        if vmin is not None:
            mask[img<vmin] = False
        if vmax is not None:
            mask[img>vmax] = False
    x0,y0 = mask_baricenter(mask)
    
    xi, = np.where(mask.sum(axis=0))
    rx = max(xi)-min(xi)
    yi, = np.where(mask.sum(axis=1))
    ry = max(yi)-min(yi)
    return PupilMask(mask, np.mean([rx,ry])/2.0, (x0,y0))
    
    