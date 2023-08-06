import numpy as np
from scipy import ndimage

class GetMass:
    def __init__(self, threshold_air=-150, image_size=512):
        self.th_air = threshold_air
        self.image_size = image_size
        self.pad_size = image_size + 38

    def _get_body(self, img_in):    
        mask_out = np.copy(img_in)
        mask_out[mask_out > self.th_air] = 0
        mask_out[mask_out <= self.th_air] = 1

        img_labels, num_labels = ndimage.label(mask_out)
        sizes = ndimage.sum(mask_out, img_labels, range(num_labels+1))
        mask_out[img_labels != np.argmax(sizes)] = 0

        mask_out = 1 - mask_out
        img_labels, num_labels = ndimage.label(mask_out)
        sizes = ndimage.sum(mask_out, img_labels, range(num_labels+1))

        for i in range(len(sizes)):
            if sizes[i] / (self.pad_size*self.pad_size) < 0.1:
                mask_out[img_labels == i] = 0

        return mask_out
    
    def _get_mask_img(self, img):
        min_val = img.min()
        mask = self._get_body(img)
        img[mask != 1] = min_val
        return img
    
    def _padding(self, img):
        r, c = self.image_size, self.image_size
        new = np.zeros((self.pad_size,self.pad_size)) + img.min()
        rstart , cstart = int((self.pad_size - r)/2 - 1), int((self.pad_size - c)/2 - 1)
        new[rstart:r+rstart, cstart:c+cstart] = img
        return new
        
    def _padding_rev(self, img):
        r, c = self.image_size, self.image_size
        rstart , cstart = int((self.pad_size - r)/2 - 1), int((self.pad_size - c)/2 - 1)
        return img[rstart:r+rstart, cstart:c+cstart]
    
    def __call__(self, img):
        img = img.squeeze()
        img = self._padding(img)
        img = self._get_mask_img(img)
        img = self._padding_rev(img)
        return img
    
