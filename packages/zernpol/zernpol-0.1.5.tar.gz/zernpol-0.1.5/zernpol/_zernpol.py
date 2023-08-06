import numpy as np  
from collections import namedtuple
from typing import Iterable, Tuple, Union, Optional
from ._tools import cart2pol
from ._pupil import PupilMask 

# dictionary of zernike polynom informations 
_zerpol_info = {
 (0, 0):  {'long name': 'Piston', 'name': 'piston'}, #1 
 (1, -1): {'long name': 'Tilt', 'name': 'tilt'},    #3
 (2, 0):  {'long name': 'Defocus', 'name': 'defocus'}, #4
 (1, 1):  {'long name': 'Tip', 'name': 'tip'},         #2
 (2, -2): {'long name': 'Oblique astigmatism', 'name': 'astig_0'}, #5 
 (2, 2):  {'long name': 'Vertical astigmatism', 'name': 'astig_45'}, #6
 (3, -3): {'long name': 'Vertical trefoil', 'name': 'trifoll_0'}, #9
 (3, -1): {'long name': 'Vertical coma', 'name': 'comax'}, #7
 (3, 1):  {'long name': 'Horizontal coma', 'name': 'comay'}, #8
 (3, 3):  {'long name': 'Oblique trefoil', 'name': 'trifoll_30'}, #10
 (4, -4): {'long name': 'Oblique quadrafoil',
           'name': 'quadrafoil_0'}, #15
 (4, -2): {'long name': 'Oblique secondary astigmatism',
           'name': 'astig2_45'}, #13
 (4, 0):  {'long name': 'Primary spherical', 'name': 'spherical1'},#11
 (4, 2):  {'long name': 'Vertical secondary astigmatism',
          'name': 'astig2_0'}, #12
 (4, 4):  {'long name': 'Vertical quadrafoil',
          'name': 'quadrafoil_45'} #14
}
_zernpol_name_loockup = {_i['name']:_nm for _nm,_i in _zerpol_info.items()}


def zernpol_pyramid(N:int) -> list:
    """ Return a 'pyramid' or triangle of zernike polynoms as follow 
    
    :: 
    
        (0,0)  
        (1,-1) (1, 1)  
        (2,-2) (2, 0)  (2,2)  
        (3,-3) (3,-1)  (3,1)  (3,3)  
        etc ...
    
    Args:
        N: number of lines 
    
    Return:
        p : list of list of :class:`Zernpol` 
    
    Please have a look at https://oeis.org/A176988
    """
    return [[Zernpol(n,m) for m in range(-n,n+1,2)] for n in range(0,N)]


def latex_formula(nm: Tuple[int,int]):
    """ Return the latex formula of zernike polynom 
    
    Args:
        nm (tuple, :class:`Zernpol`): zernike n,m polynom coeeficients 
    
    Return:
        formula (str): LaTex Formula
    
    .. note::
        
        The return formula is not bracketed by '$'
        
    Example:
    
    ::
    
        >>> from zernpol import latex_formula, Zernpol, zernikes
        >>> latex_formula( (5,3) )
        '\\sqrt{12} \\left(5 r^{5} -4 r^{3}\\right) \\ \\cos{\\,3\\theta}'
        
        >>> zernpol( (5,3) ).latex
        '\\sqrt{12} \\left(5 r^{5} -4 r^{3}\\right) \\ \\cos{\\,3\\theta}'
        
        >>> Zernpol.from_noll(15).latex
        '\\sqrt{10} r^{4} \\ \\sin{\\,4\\theta}'
        
        >>> [z.latex for z in zernpol([2,3,4])]
        ['2 r \\ \\cos{\\,\\theta}', '2 r \\ \\sin{\\,\\theta}', '\\sqrt{3} \\left(2 r^{2} -1\\right)']
    """
    n,m = nm 
    im, m = m, abs(m)
    f = np.math.factorial
    radials = []
    first = True
    for k in range((n-m)//2+1):
        num = (-1)**k * f(n-k) 
        den = f(k) * f((n+m)//2 -k )*f((n-m)//2-k)
        exp = n-2*k
        c = num//den
        
        sexp = {0:"1", 1:"r"}.get(exp, 'r^{%s}'%(exp,))
        
        if num/den == c:            
            if c==1:
                if first:
                    radials.append( '%s'%(sexp,) )
                else:
                    radials.append( '+%s'%(sexp,) )
            elif c==-1:
                radials.append( '-%s'%(sexp,) )
            else:
                if first:
                    radials.append( '%d %s'%(c, sexp) )
                else:                
                    radials.append( '%+d %s'%(c, sexp) )
        else:
            radials.append( '\\frac{%s}{%s} %s'%(num, den, sexp) )
        first = False
    form = " ".join(radials)
    
    
    if im>0:
        if m>1:
            pola = "\\ \\cos{\,%s\\theta}"%(m)
        else:
            pola = "\\ \\cos{\,\\theta}"
        if len(radials)>1:
            form = "\\left(%s\\right) %s"%(form, pola)
        else:
            form = "%s %s"%(form, pola)
    elif im<0:
        if m>1:
            pola = "\\ \\sin{\,%s\\theta}"%(m)
        else:        
            pola = "\\ \\sin{\,\\theta}"
        if len(radials)>1:
            form = "\\left(%s\\right) %s"%(form, pola)
        else:
            form = "%s %s"%(form, pola)
    else:
        if len(radials)>1:
            form = "\\left(%s\\right)"%(form)
        
    
    norm2 = (1+(m!=0))*(n+1)
    if norm2>1:
        norm = np.sqrt(norm2)
        if int(norm)==norm:
            form = "%s"%int(norm)+" "+form
        else:
            form = "\\sqrt{%s}"%norm2+" "+form
    
    return form or "1"
        
def zernpol_func1(nm, r, theta, normalized=True, masked=True):
    n,m = nm
    f = np.math.factorial
    im, m = m, abs(m)
    rnm = 0.0
    for k in range((n-m)//2+1):
        num = (-1)**k * f(n-k) 
        den = f(k) * f((n+m)//2 -k )*f((n-m)//2-k)
        rnm += num/den * r**(n-2*k)
    if normalized:            
        rnm *= np.sqrt((1+(m!=0))*(n+1))#/np.pi
    if im>0:
        rnm *= np.cos(theta*m)
    elif im<0:
        rnm *= np.sin(theta*m)
    if masked:        
        if rnm.shape:
            rnm[r>1.0] = np.nan
        else:
            rnm = np.nan if r>1.0 else rnm
    return rnm 


def zernpol_norm(nm):
    """ Return the normalisation factor for =1 normalisation 
    
    Args:
        nm (tuple) : zernike polynom coefficients
    
    Outpus:
        norm : float 
    
    """
    n,m = nm 
    return np.sqrt((1+(m!=0))*(n+1))#/np.pi


def zernpol_func(nma, r, theta, normalized=True, masked=True):
    """ Zernike Polynomial function from native polar coordinates
    
    Args:
        nma (tuple, array of tuple): define the zernike polynomials coefficient. 
             The last dimension must be 2  
        r, theta (float, array): radial and polar value. r and theta shall be broadcast together
        normalized (boolean, optional): if True (default), the polynom is normalized to 1
        masked (boolean, optional): if True all values outside the r=1 (above r>) is masked by nan values
     
    Return:
        z (array like): float of array with shape  ``nma.shape[:-1]+r.shape``  
    
    Example:
    
    ::
     
        >>> import numpy as np
        >>> from zernpol import zernpol, zernpol_func
        >>> r, theta = np.meshgrid( np.linspace(0, 1, 50), np.linspace(0, 2*np.pi, 50) )
        >>> nm = zernpol( range(1,10) )
        >>> Z = zernpol_func(nm, r, theta)
        >>> Z.shape
        (9, 50, 50)
        
    """
    nma, r, theta = (np.asarray(x) for x in (nma, r, theta))
    
    if not nma.shape or nma.shape[-1] != 2:
        raise ValueError("Last dimension of zernike polynom array is expected to be 2 got {0}".format(nma.shape))
    if len(nma.shape)==1:  
        return zernpol_func1(nma, r, theta, normalized=normalized, masked=masked)      
        
    ishape = nma.shape[:-1]
    nma = nma.reshape(-1,2)
                    
    z = np.ndarray(nma.shape[:-1]+r.shape)
    for j,nm in enumerate(nma):
        z[j,...] = zernpol_func1(nm, r, theta, normalized=normalized, masked=False)
    if masked and len(r.shape)>1:
        z[...,r>1] = np.nan
    
    return z.reshape(ishape+r.shape)

def zernpol_func_cart1(nm, x, y, normalized=True, masked=True):
    r, theta = cart2pol(x, y)
    z = zernpol_func1(nm, r, theta, normalized=normalized, masked=masked)
    return z

def zernpol_func_cart(nm, x, y, normalized=True, masked=True):
    """ Zernike Polynomial function cartezian coordinates
    
    Args:
        nma (tuple, array of tuple): define the zernike polynomials coefficient. 
             The last dimension must be 2  
        x,y (float, array): x and y coordinate of phase screen. x and y shall be broadcast together
        normalized (boolean, optional): if True (default), the polynom is normalized to 1
        masked (boolean, optional): if True all values outside the $r^2= x^2+y^2=1$ is masked by nan values
     
    Return:
        z (array like) : float of array with shape  nma.shape[:-1]+x.shape  
    
    Example:
    
    ::
     
        >>> import numpy as np
        >>> from matplotlib.pylab import plt 
        >>> from zernpol import zernpol, zernpol_func_cart
        >>> x, y = np.meshgrid( np.linspace(-1, 1, 50), np.linspace(-1, 1, 50) )
        >>> nm = zernpol( range(1,10) )
        >>> Z = zernpol_func_cart(nm, x, y)
        >>> plt.imshow( Z[3] )
            
    """
    r, theta = cart2pol(x, y)
    z = zernpol_func(nm, r, theta, normalized=normalized, masked=masked)    
    return z


_flip_func_loockup = {
(1,  1) : lambda t: t, 
(-1, 1) : lambda t: -t + np.pi,
(-1,-1) : lambda t: t  + np.pi,
(1, -1) : lambda t: -t,
}   
def reorient(theta, flip, offset_angle):
    try:
        f = _flip_func_loockup[tuple(flip)]
    except KeyError:
        raise ValueError(f"flip argument not understood got: {flip!r}")
    if offset_angle: # avoid to add 0.0 to a big theta array 
        return f(theta) + offset_angle
    else:
        return f(theta)
       
def zernpol_pupil(nma, pupil: PupilMask, inpupil_only=False, normalized: bool=True):
    """ Zernike Polynomial from a :class:`PupilMask`
    
    Args:
        nma (tuple, array of tuple): define the zernike polynomials coefficient. 
             The last dimension must be 2  
        pupil (:class:`PupilMask`): The pupil mask object define the mask array and how the zernike
              mode will be built inside the pupil image
        inpupil_only (boolean, optional): If True return only the coeeficient defined inside 
              the pupil mask. This allow to have smaller memory footprint when the illuminated 
              part of the pupil if much smaller than the full image. 
              An image can still be reconstructed from the pupil mask object with the reconstruct method
        normalized (boolean, optional): if True (default), the polynom is normalized to 1
     
    Return:
        z (array like) : float of array with shape:
                - nma.shape[:-1]+pupil.mask.shape if inpupil_only is False 
                - nma.shape[:-1] + (N,) Where N is the number of "illuminated" pixel in the pupil 
            
    
    Example:
    
    ::
    
        >>> from matplotlib.pylab import plt 
        >>> from zernpol import PupilDisk, zernpol, zernpol_pupil
        >>> disk = PupilDisk(100) # 100 diameter in user unit
        >>> disk_mask = disk.make_mask( (180,180), 1.0, center=(60.,90) )
        >>> z = zernpol_pupil( zernpol(5), disk_mask)
        >>> plt.imshow(z)
        >>> plt.show()
    
    ::

        >>> z1 = zernpol_pupil( zernpol(5), disk_mask)
        >>> z2 = zernpol_pupil( zernpol(5), disk_mask, inpupil_only=True)
        >>> print( z1.shape, z2.shape, disk_mask.reconstruct(z2).shape )

        
    """     
    mask = pupil.mask
    nY, nX =  mask.shape
    cx, cy = pupil.center
    rad = pupil.radius
    X, Y = np.meshgrid(np.arange(nX), np.arange(nY))
    
    r, theta = cart2pol((X-cx)/(rad) , (Y-cy)/(rad))    
    theta = reorient(theta, pupil.flip, pupil.angle)
    z =  zernpol_func(nma, r, theta, normalized=normalized, masked=True)
    if inpupil_only:
        return z[...,mask]
    z[...,~mask] = np.nan
    return z   
    

class Zernpol(namedtuple('BaseZernpolTuple',['n', 'm'])):
    """ Usefull class holding zernike polynoms coefficient 
    
    a Zernpol can also be build from Zernpol.from_* functions where * is the name of the indexing system
    
    :: 
    
       >>> Zernpol.from_noll(3) == Zernpol.from_ansi(1) 
       True
       >>> Zernpol.from_name('tilt')
       Zernpol(1, -1)
       
    Args:    
        n,m: Zernike polynom coefficients  
    
    Methods:
        func_pol : zernike polynom from polar coordinates
        func_cart : zernike polynom from cartezian coordinates 
        func_pupil: zernike polynom image from a :class:`PupilMask`
    Attributes:
        name, long_name (str): name and long name ( up to 'quadrafoil_0' noll=15)
        latex (str) : LateX formula (without the '$' bracket)
        noll (int): Noll index
        ansi (int): corresponding OSA/ANSI index
        fringe (int): corresponding fringe / University of Arizona index
        wyant (int): corresponding wyant index 
        info (dict) : a dictionary with all above information 
    
    Example:
    
    :: 
        
        >>> from zernpol import Zernpol, zernpol 
        >>> import numpy as np 
        >>> z = Zernpol(2,-2)
        >>> z.name, z.long_name  
        ('astig_0', 'Oblique astigmatism')
    
    ::
    
        >>> x,y = np.meshgrid( np.linspace(-1,1,50) , np.linspace(-1,1,50) )
        >>> phase_screen = z.func_cart(x,y)
    """
    name = ""
    long_name = ""
    def __init__(self, n,m):
        if m>n:
            raise ValueError(f"zernike polynom m>n : {m}>{n}")
        try:
            i = _zerpol_info[self]
        except KeyError:
            pass
        else:
            self.name, self.long_name  = i["name"], i["long name"]
    
    def __repr__(self):
        return self.__class__.__name__ + str(tuple(self))
    
    def __str__(self):
        return str(tuple(self))
    
    def func(self, r, theta, normalized=True, masked=True):
        """ Zernike Polynomial function from native polar coordinates
        
        If you look for the vectorialized counterpart function see :func:`zernpol_func`
        
        Args:        
            r, theta (float, array): radial and polar value. r and theta shall be broadcast together
            normalized (boolean, optional): if True (default), the polynom is normalized to 1
            masked (boolean, optional): if True all values outside the r=1 (above r>) is masked by nan values
         
        
        Return:
            z (array like): float of array with shape r.shape  
        
        Example:
        
        ::
         
            >>> import numpy as np
            >>> from zernpol import zernpol
            >>> r, theta = np.meshgrid( np.linspace(0, 1, 50), np.linspace(0, 2*np.pi, 50) )
            >>> z4 = zernpol(4)
            >>> z4.func(r, theta).shape
            (50, 50)
        
        Plot astig for several theta 
        
        ::
         
            
            >>> import numpy as np
            >>> from matplotlib.pylab import plt
            >>> from zernpol import zernpol
            >>> r, theta = np.meshgrid( np.linspace(0, 1, 50), [0, np.pi/8, np.pi/4] )
            >>> zp = zernpol('astig_0')
            >>> a = zp.func(r, theta)
            >>> [plt.plot(r[0], z) for z in a]
            
        """
        return zernpol_func(self, r, theta, normalized=normalized, masked=masked)
    
    def func_cart(self, x, y, normalized=True, masked=True):
        """ Zernike Polynomial function cartezian coordinates
        
        If you look for the vectorialized counterpart function see :func:`zernpol_func_cart`

        
        Args:        
            x,y (float, array): x and y coordinate of phase screen. x and y shall be broadcast together
            normalized (boolean, optional): if True (default), the polynom is normalized to 1
            masked (boolean, optional): if True all values outside the $r^2= x^2+y^2=1$ is masked by nan values
         
        Return:
            z (array like): float of array with shape x.shape  
        
        Example:
        
        ::
         
            >>> import numpy as np
            >>> from matplotlib.pylab import plt 
            >>> from zernpol import zernpol
            >>> x, y = np.meshgrid( np.linspace(-1, 1, 50), np.linspace(-1, 1, 50) )
            >>> nm = zernpol( range(1,10) )
            >>> z4 = zernpol(4)
            >>> plt.imshow( z4.func_cart(x,y) )
                
        """
        return zernpol_func_cart(self, x, y, normalized=normalized, masked=masked)
    
    def func_pupil(self, pupil: PupilMask, inpupil_only=False,  normalized: bool = True):
        """ Zernike Polynomial from a :class:`PupilMask`
    
        Args:
            pupil (:class:`PupilMask`): The pupil mask object define the mask array and how the zernike
                  mode will be built inside the pupil image
            inpupil_only (boolean, optional): If True return only the coeeficient defined inside 
                  the pupil mask. This allow to have smaller memory footprint when the illuminated 
                  part of the pupil if much smaller than the full image. 
                  An image can still be reconstructed from the pupil mask object with the reconstruct method
            normalized (boolean, optional): if True (default), the polynom is normalized to 1
         
        Return:
            z (array like) : float of array with shape:
                    - nma.shape[:-1]+pupil.mask.shape if inpupil_only is False 
                    - nma.shape[:-1] + (N,) Where N is the number of "illuminated" pixel in the pupil 
     
            return zernpol_pupil(self, pupil, inpupil_only=inpupil_only, normalized=normalized)
        """ 
    @property
    def info(self):
        """ All information inside a dictionary """
        return dict(
           coef= tuple(self), 
           name = self.name, 
           long_name = self.long_name, 
           latex = self.latex, 
           noll=self.noll, 
           ansi=self.ansi, 
           fringe=self.fringe, 
           wyant = self.wyant
        )
    
    @property
    def noll(self):
        """ Noll index """
        return zernpol_to_noll(self)
    @property
    def ansi(self):
        """ OSA/Ansi index """
        return zernpol_to_ansi(self)
    @property
    def fringe(self):
        """ Fringe/ University of Arizona index """
        return zernpol_to_fringe(self)
    @property
    def wyant(self):
        """ Wyant index """
        return zernpol_to_wyant(self)
    @property
    def latex(self):
        """ LaTeX Formula """
        return latex_formula(self)
            
    @classmethod
    def from_noll(cls,j):
        """ Create a :class:`Zernpol` from a Noll index  """
        return cls( *noll_to_zernpol(j) )
    
    @classmethod
    def from_ansi(cls,j):
        """ Create a :class:`Zernpol` from a Osa/Ansi index  """
        return cls( *ansi_to_zernpol(j) )
    
    @classmethod
    def from_fringe(cls,j):
        """ Create a :class:`Zernpol` from a Fringe index """
        return cls( *fringe_to_zernpol(j) )
    
    @classmethod
    def from_wyant(cls,j):
        """ Create a :class:`Zernpol` from a Wyant index """
        return cls( *wyant_to_zernpol(j) )
    
    @classmethod
    def from_name(cls, name):
        """ Create a :class:`Zernpol` from a zernike mode name """
        try:
            nm = _zernpol_name_loockup[name]
        except KeyError:
            raise ValueError(f"Unknown zernike polynom with name {name}")
        return cls(*nm)      

def _zerpol1(input, system):
    if isinstance(input, Zernpol):
        return input
    if isinstance( input, tuple):
        return Zernpol(*input)
    if isinstance(input, int):
        return system.i2z(input)    
    elif isinstance(input, str):
        try:
            nm = _zernpol_name_loockup[input]
        except KeyError:
            raise ValueError(f"Unknown zernike polynom with name {input}")
        return Zernpol(*nm)  
    else:
        raise ValueError(f'{input!r} is not a valid zernike input ')
        
def zernpol1(
        input: Union[int,Tuple[int,int]], 
        system: Optional["ZernpolSystem"] = None
    ) -> Zernpol:
    """ Parse a tuple or int into zernike polynomal coefficients 
    
    This is the scalar version of the vectorialized :func:`zernpol` function 
     
    Args:
        input (int, tuple, str) 
    
    Return:
        z : :class:`Zernpol`
    
    """    
    return _zerpol1(input,  ZIS._get(system))


def _zernpol_walk(input, system) -> list:
    if isinstance(input, Zernpol):
        return input
    elif isinstance(input, tuple):
        return Zernpol(*input)
    elif isinstance(input, int):
        return system.i2z(input)
    elif isinstance(input, str):
        try:
            nm = _zernpol_name_loockup[input]
        except KeyError:
            raise ValueError(f"Unknown zernike polynom with name {input}")
        return Zernpol(*nm)    
    elif hasattr(input, "__iter__"):            
        return [_zernpol_walk(i, system) for i in input]     
    raise ValueError(str(input))
        

def zernpol(input: Union[int,Tuple[int,int],list], 
           system:Optional["ZernpolSystem"] = None
        ) -> Union[list, Zernpol]:
    """ parse an input defining a zernike polynomial to its non-ambigus Zerpol(n,m) coeficients 
    

    Args:
        input: 
               - if integer, this is interpreted as an indice number of the chosen (or default) system
               - if a 2 tuple this is un-anbigously the zernike polynom coefficients
               - if str return the given zernike polynom coeficient (if known or raise error otherwhise)   
               - if iterable walk throug the item and interpret them 
        system: (ZIS, optional): used system If None the ZIS.Default is used as default system  
            
    
    Return:
        z : a list of a :class:`Zernpol` object function to input type  
    
    Example:
    
    :: 
     
        >>> from zernpol import zernpol, ZIS
        >>> zernpol(3) # default is the Noll indice system 
        Zernpol(1, -1)
        >>> zernpol(3, ZIS.Noll) 
        Zernpol(1, -1)
        >>> zernpol(3, ZIS.Ansi)
        Zernpol(2, -2)
        # system can be also a sting 
        >>> zernpol(3, 'Ansi')
        Zernpol(2, -2)
        >>> zernpol( 'tilt' )
        Zernpol(1, -1)
        >>> zernpol( (1,-1) )
        Zernpol(1, -1)
        >>> zernpol( ['tip', 'tilt', 'defocus'] )
        [Zernpol(1, 1), Zernpol(1, -1), Zernpol(2, 0)]
        
        >>> zernpol( range(1,6) , ZIS.Noll )
        [Zernpol(0, 0), Zernpol(1, 1), Zernpol(1, -1), Zernpol(2, 0), Zernpol(2, -2)]
        
        # is equivalent to :
        >>> [Zernpol.from_noll(z) for z in range(1,6)]
        
        >>> [z.name for z in zernpol( [1,2,3,4] )] 
        ['piston', 'tip', 'tilt', 'defocus']
        
        >>> zernpol( [[2,3],[4,8]] )
        [[Zernpol(1, 1), Zernpol(1, -1)], [Zernpol(2, 0), Zernpol(3, 1)]]
        
    .. seealso::
       
       function :func:`zernpol_pyramid`
       class :class:`Zernpol`
       
    """
    system = ZIS._get(system)
    return _zernpol_walk(input, system)

def zernrange(*args, system=None):
    """ Return an list on zernike polynomial coefficients 
    
    Args:
       *arg start,top,step: directly parsed 
    
    Return:
       zernikes (list) : list of :class:`zernpol.Zernike` zernike polynoms
       
    Example:
    
    ::
    
        >>> [z.name for z in zernrange(1, 5)] # default is Noll system 
        ['piston', 'tip', 'tilt', 'defocus']
        >>> [z.name for z in zernrange(1, 5, system='Ansi')]
        ['tilt', 'tip', 'astig_0', 'defocus']
    
    .. seealso::
    
       :func:`zernpol`
       :class:`Zernpol`
       
    """
    system = ZIS._get(system)
    return [_zerpol1(n, system) for n in range(*args)]

# this is used as 
_noll_pol_triangle = sum(zernpol_pyramid(100) , [])
def zernpol_to_noll(nm:Tuple[int,int]) -> int:
    """ convert zernike polynomials (n,m) to noll indice 
    
    Args:
        nm (tuple) :  (n,m) zernike polynom coef
    
    Return:
        j (int) : Noll indice number 
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials#Noll's_sequential_indices
    """
    n,m = nm
    if (n-m)%2:
        raise ValueError(f'{n},{m} has no index number')
    
    j = n*(n+1)//2+abs(m)
    if m>=0 and n%4 in [2,3]:
        j+=1
    elif m<=0 and n%4 in [0,1]:
        j+=1
    return j
    
# to lazy to invert the zernpol_to_noll just make a loockup with 5000+ modes ! 
_noll_to_zernpol_loockup = { zernpol_to_noll(nm):nm for nm in _noll_pol_triangle } 
def noll_to_zernpol(j: int) -> Tuple[int,int]:
    """ convert noll indice to zernike polynom coefficients 
    
    Args:
        j (int) : Noll indice number 
        
    Return:
        nm (tuple) :  (n,m) zernike polynom coef
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials#Noll's_sequential_indices
    """
    try:
        return _noll_to_zernpol_loockup[j]
    except KeyError:
        raise ValueError('Noll number <1 or above limit')

def zernpol_to_ansi(nm: Tuple[int,int]) -> int:
    """ convert zernike polynomials (n,m) to OSA/ANSI indice 
    
    Args:
        nm (tuple) :  (n,m) zernike polynom coef
    
    Return:
        j (int) : OSA/ANSI indice number
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials 
    """
    n,m = nm
    if (n-m)%2:
        raise ValueError(f'{n},{m} is not a valid zernike polynom pair')    
    return (n*(n+2)+m)//2
    
_ansi_to_zernpol_loockup = { zernpol_to_ansi(nm):nm for nm in _noll_pol_triangle } 
def ansi_to_zernpol(j):
    """ convert OSA/ANSI indice to zernike polynoms 
    
    Args:
        j (int): OSA/ANSI indice number
    
    Return:    
        nm (tuple): (n,m) zernike polynom coef
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials 
    """
    try:
        return _ansi_to_zernpol_loockup[j]
    except KeyError:
        raise ValueError('Ansi indice <0 or above limit')


def _zernpol_to_fringe_formula(n,m):
    # fringe system is defined up to 37 but the formulae is only valid up 
    # to 36 
    return (1+ (n+abs(m))//2)**2 -2*abs(m) + (1-np.sign(m))//2

def zernpol_to_fringe(nm):
    """ Convert zernike polynomials (n,m) to Fringe/University of Arizona indice 
    
    Args:
        nm (tuple) :  (n,m) zernike polynom coef
    
    Return:
        j (int) : Fringe/University of Arizona indice number
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials
    and https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2018/04/Schwiegerling-Zernike-2018.pdf

    """
    n,m = nm
    if (n-m)%2:
        raise ValueError(f'{n},{m} is not a valid zernike polynom pair') 
    j = _zernpol_to_fringe_formula(n,m) 
    # Fringe formulae is only valid up to 36 but an extra sherical aberation (37)
    # correspond to 49 as returned by the formula 
    if j==49:  
        return 37
    if j>36:
        raise ValueError(f'{n},{m} is not defined inside the Fringe indice system')
    return j 

_fringe_to_zernpol_loockup = { _zernpol_to_fringe_formula(*nm):nm for nm in _noll_pol_triangle } 
def fringe_to_zernpol(j):
    """ convert Fringe/University of Arizona indice to zernike polynoms 
    
    Args:
        j (int) : Fringe/University of Arizona indice number
    
    Return:    
        nm (tuple) :  (n,m) zernike polynom coef
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials
    """
    if j<1 or j>37:
        raise ValueError(f'Fringe indice must be between 1<=i<=37 got {j}')
    if j == 37:
       return Zernpol(12,0) # the loockup is good only until 36  
    try:
        return _fringe_to_zernpol_loockup[j]
    except KeyError:
        raise ValueError(f'BUG ! Fringe indice must be between 1<=i<=37 got {j}')

def zernpol_to_wyant(nm):
    """ convert zernike polynomials (n,m) to Wyant indice 
    
    Args:
        nm (tuple) :  (n,m) zernike polynom coef
    
    Return:
        j (int) : Fringe/University of Arizona indice number
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials 
    """
    return zernpol_to_fringe(nm)-1    

def wyant_to_zernpol(j):
    """ convert Wyant indice to zernike polynomials (n,m)
    
    Args:
        j (int) : Fringe/University of Arizona indice number
    
    
    Return:
        nm (tuple) :  (n,m) zernike polynom coef
    
    see https://en.wikipedia.org/wiki/Zernike_polynomials 
    """
    return fringe_to_zernpol(j+1)


def zernpol_info(nm: Tuple[int,int]) -> dict:
    """ return a dictionary containing informations about the zernike polynoms 
    
    Args:
        nm (tuple) :  (n,m) zernike polynom coefficients
    
    Return:
        info (dict) :  dictionary with keys 
           'coef', 'name', 'long_name', 
           'latex' (latex formula),
           'noll', 'ansi', 'fringe', 'wyant'
    """
    return zernpol(nm).info

class ZernpolSystem:
    """ Define an indexing convention for zernike polynomial  """
    def __init__(self):
        raise ValueError('ZernpolSystem class is not instanciable')
        
    name = ""
    @staticmethod
    def z2i(nm):
        """ Convert zernike polynomials to system indice """
        raise NotImplementedError('z2i')
    @staticmethod
    def i2z(nm):
        """ Convert to system indice to zernike polynomials """
        raise NotImplementedError('i2z')
 
class ZIS:
    """ A set of zernike polynomial indexing system """    
    Default = None
    def __init__(self):
        raise ValueError('ZIS is not instanciable')
        
    @classmethod
    def _get(cls, name):
        if name is None:
            return cls.Default
        if isinstance(name, type) and issubclass(name, ZernpolSystem):
            return name
        try:
            return getattr(cls, name)
        except AttributeError:
            valid = [s for s in cls.__dict__.keys() if not s.startswith("_")]
            raise ValueError("Unknown system {0}, must be one of '{1}'".format(name, "', '".join(valid)))        
            
    @classmethod
    def _set_default(cls, name_or_system):
        cls.Default = cls.get(name_or_system)

class Noll(ZernpolSystem):
    """ Define the zernike polynomials Noll indexing system  
    
    see:
     
    - https://en.wikipedia.org/wiki/Zernike_polynomials#Noll's_sequential_indices
    - https://oeis.org/A176988
    """
    name = "Noll"
    z2i = staticmethod(zernpol_to_noll)
    i2z = staticmethod(noll_to_zernpol)
ZIS.Noll = Noll
ZIS.noll = Noll
ZIS.Default = Noll ## Noll is the default system !!

class Ansi(ZernpolSystem):
    """ Define the zernike polynomials OSA/ANSI indexing system 
    
    see: https://en.wikipedia.org/wiki/Zernike_polynomials#OSA/ANSI_standard_indices
    """
    name = "Osa/Ansi"
    z2i = staticmethod(zernpol_to_ansi)
    i2z = staticmethod(ansi_to_zernpol)
ZIS.Ansi = Ansi
ZIS.ansi = Ansi
ZIS.Osa = Ansi
ZIS.osa = Ansi

class Fringe(ZernpolSystem):
    """ Define the zernike polynomials Fringe/University of Arizona indexing system 
    
    see:  https://en.wikipedia.org/wiki/Zernike_polynomials#Fringe/University_of_Arizona_indices
    """
    name = "Fringe/U Of Arizona"
    z2i = staticmethod(zernpol_to_fringe)
    i2z = staticmethod(fringe_to_zernpol)
ZIS.Fringe = Fringe
ZIS.fringe = Fringe
ZIS.Arizona = Fringe

            
class Wyant(ZernpolSystem):
    """ Define the zernike polynomials Wyant indexing system 
    
    see:  https://en.wikipedia.org/wiki/Zernike_polynomials#https://en.wikipedia.org/wiki/Zernike_polynomials#Wyant_indices """
    name = "Wyant"
    z2i = staticmethod(zernpol_to_wyant)
    i2z = staticmethod(wyant_to_zernpol)
ZIS.Wyant = Wyant
ZIS.wyant = Wyant
