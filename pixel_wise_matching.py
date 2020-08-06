import numpy as np
from PIL import Image

def stereo_matching(left_img, right_img, disparity_range):
    # doc anh va chuyen ve mode grayscale
    left_img = Image.open(left_img).convert('L')
    left = np.asarray(left_img)

    right_img = Image.open(right_img).convert('L')
    right = np.asarray(right_img)

    #chieu rong va chieu cao cua anh, duoc cho truoc

    height = 288
    width = 384

    #disparity map

    depth = np.zeros((height, width), np.uint8)
    scale = 255 / disparity_range

    for y in range(height):
        for x in range(width):

            disparity = 0
            cost_min = (int(left[y, x]) - int(right[y, x])) ** 2

            for j in range(1, disparity_range):
                if x < j:
                    cost = 255**2
                else:
                    cost = (int(left[y, x]) - int(right[y, x - j])) ** 2
                if cost < cost_min:
                    cost_min = cost
                    disparity = j

            depth[y, x] = disparity * scale

    Image.fromarray(depth).save('disparity_map.png')
    
