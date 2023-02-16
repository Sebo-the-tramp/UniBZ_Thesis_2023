import numpy as np
import math

def angles2R(a):
    return np.dot(np.dot(Rx(a[0]), Ry(a[1])), Rz(a[2]))

def Rx(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def Ry(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def Rz(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def Rx_prime(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[0, 0, 0], [0, -s, -c], [0, c, -s]])

def Ry_prime(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[-s, 0, c], [0, 0, 0], [-c, 0, -s]])

def Rz_prime(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[-s, -c, 0], [c, -s, 0], [0, 0, 0]])

def v2t(v):
    T = np.eye(4)
    T[:3, :3] = angles2R(v[3:6])        
    T[:3, 3] = v[:3]
    return T