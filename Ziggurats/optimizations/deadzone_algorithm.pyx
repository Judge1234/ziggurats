#defining NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#   Regular imports
import numpy as np

#   Compile-time information for Cython
cimport numpy as np 


#               KEY:
#
#   NO_DEADZONE =            0
#   P1_DEADZONE =            1
#   P2_DEADZONE =            2
#   MUTUAL_DEADZONE =        3
#   NO_OWNERSHIP =           0
#   P1_OWNERSHIP =           1
#   P2_OWNERSHIP =           2
#   UNOCCUPIED =             0
#   OCCUPIED =               1
#
#   A Square object is encoded into an array of three integers:
#
#   index[0] refers to deadzone booleans                | p1, p2, mutual, none
#   index[1] refers to ownership                        | p1, p2, none
#   index[2] indicates piece type                       | (enum from encoding)


cpdef np.ndarray convolve(np.ndarray matrix):
    cdef np.ndarray deltas = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int p1_supports = 0
    cdef int p2_supports = 0
    cdef int shape_1 = matrix.shape[0]-1
    cdef int shape_2 = matrix.shape[1]-1

    #   Pass 1: remove old deadzones
    for i in range(shape_1):
        for j in range(shape_2):
            matrix[i][j][0] = 0 
            if matrix[i][j][2] == 0: 
                matrix[i][j][1] = 0 
    #   Pass 2: create new deadzones
    for i in range(shape_1):
        for j in range(shape_2):
            for k in range(4):
                if matrix[i + deltas[k][0]][j + deltas[k][1]][1] == 1: 
                    p1_supports += 1
                if matrix[i + deltas[k][0]][j + deltas[k][1]][1] == 2: 
                    p2_supports += 1
            if p1_supports == 2 and p2_supports == 2:
                matrix[i][j][0] = 3 
                p1_supports = 0
                p2_supports = 0
                break
            if p1_supports >= 2:
                matrix[i][j][0] = 1 
                if matrix[i][j][1] == 2 and matrix[i][j][2] == 1: 
                    matrix[i][j][1] = 1 
                    matrix[i][j][2] = 0 
            if p2_supports >= 2:
                matrix[i][j][0] = 2 
                if matrix[i][j][1] == 1 and matrix[i][j][2] == 1: 
                    matrix[i][j][1] = 2 
                    matrix[i][j][2] = 0 

    return matrix    



