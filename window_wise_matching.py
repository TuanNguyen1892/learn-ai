import numpy as np
from PIL import Image

#kernel_size should be odd
def stereo_matching_window(left_img, right_img, kernel_size, disparity_range):

    left_img = Image.open(left_img).convert('L')
    left = np.asarray(left_img)
    right_img = Image.open(right_img).convert('L')
    right = np.asarray(right_img)

    height = 288
    width = 384

    depth = np.zeros((height, width), np.uint8)
    scale = 255/disparity_range
    kernel_half = int((kernel_size-1)/2)

    for y in range(kernel_half, height - kernel_half):
        print('.', end = ' ')

        for x in range(kernel_half, width-kernel_half):

            disparity = 0
            cost_min = 65534 #don't know why init cost_min = 2^16 - 2 ???

            for j in range(disparity_range): 
                ssd = 0
                ssd_temp = 0 
                
                for v in range(-kernel_half, kernel_half):
                    for u in range(-kernel_half, kernel_half):
                        ssd_temp = 255**2 
                        if (x+u-j) >= 0:
                            ssd_temp = (int(left[y+v, x+u]) - int(right[y+v, (x+u) - j]))**2 
                        ssd += ssd_temp         
                
                if ssd < cost_min:
                    cost_min = ssd
                    disparity = j
            
           
            depth[y, x] = disparity * scale
                                

    Image.fromarray(depth).save('disparity_map_ssd.png')
