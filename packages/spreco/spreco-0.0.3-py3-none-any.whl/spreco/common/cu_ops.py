from cupy.fft import fftshift, ifftshift, ifft2, fft2
import cupy as cp
import numpy as np

def mfft2(x, dims, axis=(0,1), center=False):
    nx, ny = dims
    if center:
        return ifftshift(fft2(fftshift(x), axes=axis))/cp.sqrt(nx*ny)
    else:
        return fftshift(fft2(fftshift(x), axes=axis))/cp.sqrt(nx*ny)

def mifft2(x, dims, axis=(0,1), center=False):
    nx, ny = dims
    if center:
        return fftshift(ifft2(ifftshift(x), axes=axis))*cp.sqrt(nx*ny)
    else:
        return fftshift(ifft2(fftshift(x), axes=axis))*cp.sqrt(nx*ny)

def A_cart(img, coilsen, mask, shape, axis=(0,1), center=False):
    """
    forward cartesian A 
    """
    coil_img = coilsen*img[..., cp.newaxis]
    kspace = mfft2(coil_img, shape, axis=axis, center=center)
    kspace = cp.multiply(kspace, mask[...,cp.newaxis])
    return kspace

def AT_cart(kspace, coilsen, mask, shape, axis=(0,1), center=False):
    """
    adjoint cartesian AT
    coil dimension should always be the last
    """
    coil_img = mifft2(kspace*mask[...,cp.newaxis], shape, axis=axis, center=center)
    coil_sum = cp.sum(coil_img*cp.conj(coilsen), axis=-1)

    return coil_sum

def AHA(x, coilsen, mask, shape, axis=(1,2), center=False):
    if isinstance(x, np.ndarray):
        x = cp.asarray(x)
    tmp = A_cart(x, coilsen, mask, shape, axis, center)
    ret = AT_cart(tmp, coilsen, mask, shape, axis, center)
    return ret