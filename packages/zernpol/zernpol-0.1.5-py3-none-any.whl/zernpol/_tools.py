import numpy as np
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def nanrms(a, axis=None):
    a = np.asarray(a)
    return np.sqrt(np.nanmean(a**2, axis=axis))

def mask_baricenter(mask):
    ya,xa = np.where(mask)
    l = len(ya)
    return np.sum(xa)/l, np.sum(ya)/l

    