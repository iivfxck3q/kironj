
from math import cos, radians, sin
from .matrix import MatMGLW

from pyrr import Vector3, vector, vector3

class Camera:
    def __init__(self,obj) -> None:
        self._obj=obj

        self._x, self._y, self._z = 0, 0, 0
        self._up=Vector3([0,1,0])

        self._yaw, self._pitch, self._roll = 0, 0, 0
        self._dx, self._dy, self._dz = 0, 0, -1

        self._sensitivity=0.5
        self._velocity=0.1

        self._forward=False
        self._backward=False
        self._leftward=False
        self._rightward=False
        self._upping=False
        self._bottoming=False

    @property
    def move_hundler(self):
        dx=cos(radians(self._yaw))
        dz=sin(radians(self._yaw))
        if self._forward==True:
            self._z+=dz*self._velocity
            self._x+=dx*self._velocity
        if self._backward==True:
            self._z-=dz*self._velocity
            self._x-=dx*self._velocity
        
        if self._leftward==True:
            self._z-=dx*self._velocity
            self._x+=dz*self._velocity
        if self._rightward==True:
            self._z+=dx*self._velocity
            self._x-=dz*self._velocity
        
        if self._upping==True:
            self._y-=0.1
        if self._bottoming==True:
            self._y+=0.1
    
    @property
    def position(self) -> Vector3:
        return Vector3([self._x, self._y, self._z])
    
    @property
    def rotate(self) -> Vector3:
        return Vector3([self._yaw,self._pitch,self._roll])
    
    @property
    def direction(self) -> Vector3:
        return Vector3([self._dx, self._dy, self._dz])

    @property
    def _projection(self):
        return MatMGLW.perspective(75,848/480,0.1,50000)
    
    @property
    def _matrix(self):
        self._dx, self._dy, self._dz=(cos(radians(self._yaw)) * cos(radians(self._pitch)),
                           sin(radians(self._pitch)),
                           sin(radians(self._yaw)) * cos(radians(self._pitch)))
        
        target=self.position - self.direction

        z = vector.normalise(self.position - target)
        x = vector.normalise(vector3.cross(vector.normalise(self._up), z))
        y = vector3.cross(z, x)


        translate = MatMGLW.translate(self.position)
        rotate=MatMGLW.identity()
        rotate[0:3,0:3]=[
            [x[0], y[0], z[0]],
            [x[1], y[1], z[1]],
            [x[2], y[2], z[2]]
        ]
        matrix=translate @ rotate
        return matrix



    def key_input(self,key, action, modifiers):
        if action == self._obj.wnd.keys.ACTION_PRESS:
        #other
            if key == self._obj.wnd.keys.F1:
                self._obj.wnd.mouse_exclusivity=True if not self._obj.wnd.mouse_exclusivity else False

        #move
            if key == self._obj.wnd.keys.W:
                self._forward=True
            if key == self._obj.wnd.keys.A:
                self._leftward=True
            if key == self._obj.wnd.keys.S:
                self._backward=True
            if key == self._obj.wnd.keys.D:
                self._rightward=True
            if key == self._obj.wnd.keys.Q:
                self._upping=True
            if key == self._obj.wnd.keys.E:
                self._bottoming=True
            

        elif action == self._obj.wnd.keys.ACTION_RELEASE:
            if key == self._obj.wnd.keys.W:
                self._forward=False
            if key == self._obj.wnd.keys.A:
                self._leftward=False
            if key == self._obj.wnd.keys.S:
                self._backward=False
            if key == self._obj.wnd.keys.D:
                self._rightward=False
            if key == self._obj.wnd.keys.Q:
                self._upping=False
            if key == self._obj.wnd.keys.E:
                self._bottoming=False

    def mouse_position_input(self,dx,dy):
        if self._obj.wnd.mouse_exclusivity:
            if self._yaw>360 or self._yaw<-360:
                self._yaw=0

            if self._pitch>=89 and dy>0:
                self._pitch=89

            elif self._pitch<=-89 and dy<0:
                self._pitch=-89
            else:
                self._pitch+=dy*self._sensitivity

            # if self._pitch<=-89 and dy<0:
            #     self._pitch=-89
            # else:
            #     self._pitch+=dy*self._sensitivity

            self._yaw+=dx*self._sensitivity
            
