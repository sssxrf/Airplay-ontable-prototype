import numpy as np
import math

def findparallel(lines, thres_dis, thres_paral):

        lines1 = []
        for i in range(len(lines)):
            for j in range(len(lines)):
                if (i == j):continue
                if lines[i][0][0] <= thres_dis or lines[j][0][1] <= thres_dis:continue
                if (abs(lines[i][0][1] - lines[j][0][1]) <= thres_paral):          
                     # found a parallel line!
                     lines1.append((i,j))


        return lines1

def findwheelcenter(box, half_disinpixel):

    #find the rightside(the line has the largest distance in x-axis)
    center_all4 = np.zeros((4,2))
    center_all4[0] = (box[0] + box[1]) / 2
    center_all4[1] = (box[1] + box[2]) / 2
    center_all4[2] = (box[2] + box[3]) / 2
    center_all4[3] = (box[3] + box[0]) / 2
    index_right = np.argmax(center_all4, axis = 0)
    index_xmax = index_right[0]
    if index_xmax == 3:
        center_right = (box[3] + box[0]) / 2
        #avoid divide by 0
        if box[3][0] == box[0][0]:
            cx = center_right[0] - half_disinpixel
            cy = center_right[1]
        else:
            grad_rightside = (box[3][1] - box[0][1]) / (box[3][0] - box[0][0])
            grad_center = -1 / grad_rightside
            cx = center_right[0] - half_disinpixel / math.sqrt(grad_center**2 + 1)
            cy = center_right[1] - half_disinpixel / math.sqrt(1 / grad_center**2 + 1)
    else:
        center_right = (box[index_xmax] + box[index_xmax + 1]) / 2
        if box[index_xmax][0] == box[index_xmax + 1][0]:
            cx = center_right[0] - half_disinpixel
            cy = center_right[1]
        else:
            grad_rightside = (box[index_xmax][1] - box[index_xmax + 1][1]) / (box[index_xmax][0] - box[index_xmax + 1][0])
            grad_center = -1 / grad_rightside
            cx = center_right[0] - half_disinpixel / math.sqrt(grad_center**2 + 1)
            cy = center_right[1] - half_disinpixel / math.sqrt(1 / grad_center**2 + 1)

    return cx, cy