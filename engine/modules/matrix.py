from math import radians, sin, cos
import numpy as np

class MatMGLW:

    def identity(dtype='f4'):
        return np.identity(4,dtype=dtype)
    
    def perspective(fov,aspect,near,far):
        ymax = near * np.tan(fov * np.pi / 360.0)
        xmax = ymax * aspect
        left,right,bottom,top=-xmax, xmax, -ymax, ymax
        A = (right + left) / (right - left)
        B = (top + bottom) / (top - bottom)
        C = -(far + near) / (far - near)
        D = -2. * far * near / (far - near)
        E = 2. * near / (right - left)
        F = 2. * near / (top - bottom)
        return np.array((
            (E, 0., 0., 0.),
            (0.,  F, 0., 0.),
            (A,  B,  C,-1.),
            (0., 0.,  D, 0.),
        ))

    def rotatex(angle):
        theta=radians(angle)
        cosT = np.cos(theta)
        sinT = np.sin(theta)
        mat=MatMGLW.identity()
        mat[0:3,0:3]=np.array([
            [1.0, 0.0, 0.0],
            [0.0, cosT,-sinT],
            [0.0, sinT, cosT]
        ])
        return mat
    
    def rotatey(angle):
        theta=radians(angle)
        cosT = np.cos(theta)
        sinT = np.sin(theta)
        mat=MatMGLW.identity()
        mat[0:3,0:3]=np.array([
            [cosT, 0.0,sinT],
            [0.0, 1.0, 0.0],
            [-sinT, 0.0, cosT]
        ])
        return mat
    
    def rotatez(angle):
        theta=radians(angle)
        cosT = np.cos(theta)
        sinT = np.sin(theta)
        mat=MatMGLW.identity()
        mat[0:3,0:3]=np.array([
            [cosT,-sinT, 0.0],
            [sinT, cosT, 0.0],
            [0.0, 0.0, 1.0]
        ])
        return mat

    def rotatexyz(angle):
        ox,oy,oz=angle

        dx = MatMGLW.rotatex(ox)
        dy = MatMGLW.rotatey(oy)
        dz = MatMGLW.rotatez(oz)

        return dx@dy@dz

    def translate(coord):
        mat=MatMGLW.identity()
        mat[3,0:3]=coord[:3]
        return mat

    def scale(scale):
        mat = np.diagflat([scale[0], scale[1], scale[2], 1.0])
        return mat