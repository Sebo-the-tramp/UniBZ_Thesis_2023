# libraries

import numpy as np
from utils import *
from geomutils import *
from scipy.spatial.transform import Rotation as Rotation
import matplotlib.pyplot as plt

def errorAndJacobian(x, P, Z):

    rx = Rx(x[3])
    ry = Ry(x[4])
    rz = Rz(x[5])

    t = x[:3]

    z_hat = np.dot(np.dot(rx, ry), rz) @ P.T + t

    e = Z - z_hat.T
    J = np.zeros((3,6))
    J[:3, :3] = np.eye(3)

    rx_prime = Rx_prime(x[3])
    ry_prime = Ry_prime(x[4])
    rz_prime = Rz_prime(x[5])

    J[:3, 3] = np.dot(np.dot(rx_prime, ry), rz) @ P.T
    J[:3, 4] = np.dot(np.dot(rx, ry_prime), rz) @ P.T
    J[:3, 5] = np.dot(np.dot(rx, ry), rz_prime) @ P.T

    return e, J

def errorAndJacobianLinear(x, P, Z):
    
    M = np.zeros((3,9))
    M[0, :3] = P[:3]
    M[1,3:6] = P[:3]
    M[2, 6:] = P[:3]

    h = np.dot(M, x[:9]) + x[9:] # 3x9 * 9x1 + 3x1 = 3x1    
    
    e = h - Z

    J = np.zeros((3,12))
    J[:3, :9] = M
    J[:3, 9:] = np.eye(3)    

    return e, J

def doICP(x_guess, points, Z, iterations, damping, kernel_threshold):
    x = x_guess
    chi_state = np.zeros(iterations)    
    num_inliers = np.zeros((iterations))

    for i in range(iterations):
        #print("Iteration number ", i)
        H = np.zeros((6,6))
        b = np.zeros((6))
        chi = 0

        for j in range(points.shape[0]):
            e, J = errorAndJacobian(x, points[j,:], Z[j,:])
            H += J.T @ J
            b += J.T @ e

            chi += e.T @ e            
            if(chi > kernel_threshold):
                e = math.sqrt(kernel_threshold/chi) * e
                chi = kernel_threshold

            else:
                num_inliers[i] += 1                         

        chi_state[i] = chi
        #print(chi_state[i])
        
        dx = np.linalg.solve(H, b.T)
        x = x + dx.T    
    return x, chi_state, num_inliers

def doICPLinear(x_guess, points, Z):        
    x = x_guess.copy()
    H = np.zeros((12,12))
    b = np.zeros((12))        

    for j in range(points.shape[0]):
        e, J = errorAndJacobianLinear(x, points[j,:], Z[j,:])
        H += J.T @ J
        b += J.T @ e

    dx = - np.linalg.solve(H, b.T)
    #print("dx\n", dx)
    x += dx.T    

    A = np.concatenate((x[:3], x[3:6], x[6:9]))
    
    A = A.reshape((3,3))
    #print("R\n", A)

    u, s, vh = np.linalg.svd(A, full_matrices=True)

    # if s is a diagonal matrix with 1s on the diagonal, then the matrix R is a rotation matrix

    res = np.allclose(A, np.dot(u*s, vh))
    #print("res", res)

    R = np.dot(u, vh)    
    t = x[9:]

    return R, t


def loadData():

    ## data

    n_points = 100

    # Generate random points in 3d
    points = np.random.random((n_points, 3))    

    # ideal position of the world in respect to the robot, in our case the HMD
    x_true = np.array([0, 0, 0, np.pi/2, np.pi/6, np.pi/3])    
    X_true = v2t(x_true)    

    # test with random initial guess
    x_gg = np.array([0.5, 0.5, 0.5, 0.1, 0.1, 0.1])

    x_guess = x_true + x_gg
    #print("x_guess\n", x_guess)
    X_guess = v2t(x_guess)
    #print("X_guess\n", X_guess)

    R_guess = X_guess[:3, :3]

    guess = np.reshape(R_guess, (9))
    guess = np.append(guess, X_guess[:3, 3])    

    n_points = points.shape[0]
    P_world_hom = np.ones((n_points, 4))
    P_world_hom[:, :3] = points
    Z_hom = np.dot(X_true, P_world_hom.T)
    Z = Z_hom[:3, :].T

    return points, Z, X_true, guess, x_true

def main():

    # load data
    points, points_trans, X_true, X_guess, x_true = loadData()

    # Initial guess    
    R, t = doICPLinear(X_guess, points, points_trans)
    
    # tranform initial guess to vector
    r = Rotation.from_matrix(R)
    angles = r.as_euler('zyx', degrees=False)[::-1]    
    
    x_guess = np.append(angles, t)        

    # do ICP iteratively
    
    iterations = 100
    damping = 100

    x, chi_stats, _ = doICP(x_guess, points, points_trans, iterations, damping, 1e9)

    print("Ground truth\n", x_true)
    print("Estimated\n", x)

    print("Error chi:" , chi_stats[-1])

    print("Difference\n", x_true - x)

    # write a file with the rotation matrix and the translation vector
    
    res = v2t(x)
    print("R\n", res)

    # save to a file the results
    np.savetxt("./output/rotomatrix.txt", res, delimiter=",")

if __name__ == "__main__":
    main()