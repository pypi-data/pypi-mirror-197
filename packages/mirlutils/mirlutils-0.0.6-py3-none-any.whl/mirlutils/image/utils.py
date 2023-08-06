import os
import numpy as np
import SimpleITK as sitk 
import pydicom
import matplotlib.pyplot as plt
import torch
from typing import Optional

def imshow(array:np.array, vmin=None, vmax=None, title:str=None):
    """
    Show medical image
    """
    plt.figure(figsize=(6,6))
    if title:
        plt.title(title, fontsize=15)
    array = array.squeeze()
    if len(array.shape) == 2:
        plt.imshow(array, cmap='gray', vmin=vmin, vmax=vmax)
    else:
        plt.imshow(array)
    plt.axis('off')
    plt.tight_layout()
    plt.show()    

def dicom_to_nifti(src:str , dst:str):
    """
    src : dicom directory path
    dst : nifti save path with .nii suffix 
    """
    reader = sitk.ImageSeriesReader()
    dicoms = reader.GetGDCMSeriesFileNames(str(src))
    reader.SetFileNames(dicoms)
    image = reader.Execute()
    sitk.WriteImage(image, str(dst))

def get_array(file_path:str, dtype=np.float64):
    """
    Get numpy array from .img, .dcm, .hdr, .nii, or dicom directory
    file_path : path
    """
    if os.path.isdir(file_path):
        reader = sitk.ImageSeriesReader()
        dicoms = reader.GetGDCMSeriesFileNames(str(file_path))
        reader.SetFileNames(dicoms)
        temp = reader.Execute()
    else:
        temp = sitk.ReadImage(str(file_path))
    return sitk.GetArrayFromImage(temp).astype(dtype)

def windowing(array, wl, ww, normalize=True):
    """
    array : target array to adjust window setting
    wl : window level
    ww : window width
    normalize : return values in range (0-1) 
    """
    lower_bound = wl - ww/2
    upper_bound = wl + ww/2

    if normalize:
        return (np.clip(array, lower_bound, upper_bound) - lower_bound) / ww
    else:
        return np.clip(array, lower_bound, upper_bound) 

def save_dicom(src_dicom_path:str, pixel_array:np.array, dst_dicom_path:str):
    """
    Save output image to dicom
    """
    dcm = pydicom.dcmread(src_dicom_path, force=True)
    intercept = dcm.RescaleIntercept
    slope = dcm.RescaleSlope
    pixel_array = (pixel_array - intercept) / slope
    pixel_array = pixel_array.astype(np.int16)

    dcm.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    dcm.PixelData = pixel_array.squeeze().tobytes()

    if hasattr(dcm, 'SmallestImagePixelValue') and hasattr(dcm, 'LargestImagePixelValue'):
        dcm.SmallestImagePixelValue = pixel_array.min()
        dcm.LargestImagePixelValue = pixel_array.max()
        dcm[0x0028,0x0106].VR = 'US'
        dcm[0x0028,0x0107].VR = 'US'

    dcm.save_as(dst_dicom_path)

def flip_mask(src_mask_path:str, dst_mask_path:str):
    """
    Use when the mask is flipped by rows.
    """
    mask_arr = sitk.GetArrayFromImage(sitk.ReadImage(src_mask_path))

    if len(mask_arr.shape) == 3:
        fliped_image = sitk.GetImageFromArray(np.flip(mask_arr, axis=1))
    elif len(mask_arr.shape) == 2:
        fliped_image = sitk.GetImageFromArray(np.flip(mask_arr, axis=0))
        
    sitk.WriteImage(fliped_image, dst_mask_path)

def seg_mask_to_one_hot(mask:torch.Tensor, 
                      num_classes:int, 
                      device:Optional[torch.device]=None):
    
    if len(mask.shape) == 3:
        mask = mask.unsqueeze(1)
    
    one_hot = torch.zeros_like(mask, dtype=torch.float32).repeat(1, num_classes, 1, 1)
    one_hot.scatter_(1, mask, 1.0)
    return one_hot.to(device if device else 'cpu')