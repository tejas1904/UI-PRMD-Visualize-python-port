import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from celluloid import Camera

def cartesian_frames(pos_file,ang_file):
    dfp = pd.read_csv(pos_file,sep=',')
    dfa = pd.read_csv(ang_file,sep=',')
    readpos = dfp.to_numpy()
    readang = dfa.to_numpy()

    for i in range(len(readpos[1, :])):
        readpos[:, i] = smooth(readpos[:, i], 5) #change last digit for smoothness

    for i in range(len(readang[1, :])):
        readang[:, i] = smooth(readang[:, i], 23) #change last digit for smoothness

    frames = np.shape(readpos)[0]
    skeleton_pos = np.zeros((22, 3, frames));
    skeleton_ang = np.zeros((22, 3, frames));

    tp = np.transpose(readpos)

    for i in range(frames):
        skeleton_pos[:, :, i] = tp[:, i].reshape((22, 3))

    ta = np.transpose(readang)
    for i in range(frames):
        skeleton_ang[:, :, i] = ta[:, i].reshape((22, 3))

    skel = np.zeros((22, 3, frames))
    rot = np.zeros((22, 3, frames))

    for i in range(frames):
        joint_pos = skeleton_pos[:, :, i]
        joint_ang = skeleton_ang[:, :, i]

        # chest,neck,head

        rot_1 = e2r(joint_ang[0, :].dot(np.pi / 180))
        joint_pos[1, :] = np.transpose(rot_1.dot(np.transpose(joint_pos[1, :]))) + joint_pos[0, :]

        rot_2 = rot_1.dot(e2r(joint_ang[1, :].dot(np.pi / 180)))
        joint_pos[2, :] = (np.transpose(rot_2.dot(np.transpose(joint_pos[2, :])))) + joint_pos[1, :]

        rot_3 = rot_2.dot(e2r(joint_ang[2, :].dot(np.pi / 180)))
        joint_pos[3, :] = (np.transpose(rot_3.dot(np.transpose(joint_pos[3, :])))) + joint_pos[2, :]

        rot_4 = rot_3.dot(e2r(joint_ang[3, :].dot(np.pi / 180)))
        joint_pos[4, :] = (np.transpose(rot_4.dot(np.transpose(joint_pos[4, :])))) + joint_pos[3, :]

        rot_5 = rot_4.dot(e2r(joint_ang[4, :].dot(np.pi / 180)))
        joint_pos[5, :] = (np.transpose(rot_5.dot(np.transpose(joint_pos[5, :])))) + joint_pos[4, :]

        # left arm
        rot_6 = e2r(joint_ang[2, :].dot(np.pi / 180))
        joint_pos[6, :] = (np.transpose(rot_6.dot(np.transpose(joint_pos[6, :])))) + joint_pos[2, :]

        rot_7 = rot_6.dot(e2r(joint_ang[6, :].dot(np.pi / 180)))
        joint_pos[7, :] = (np.transpose(rot_7.dot(np.transpose(joint_pos[7, :])))) + joint_pos[6, :]

        rot_8 = rot_7.dot(e2r(joint_ang[7, :].dot(np.pi / 180)))
        joint_pos[8, :] = (np.transpose(rot_8.dot(np.transpose(joint_pos[8, :])))) + joint_pos[7, :]

        rot_9 = rot_8.dot(e2r(joint_ang[8, :].dot(np.pi / 180)))
        joint_pos[9, :] = (np.transpose(rot_9.dot(np.transpose(joint_pos[9, :])))) + joint_pos[8, :]

        # right arm

        rot_10 = e2r(joint_ang[2, :].dot(np.pi / 180))
        joint_pos[10, :] = (np.transpose(rot_10.dot(np.transpose(joint_pos[10, :])))) + joint_pos[2, :]

        rot_11 = rot_10.dot(e2r(joint_ang[10, :].dot(np.pi / 180)))
        joint_pos[11, :] = (np.transpose(rot_11.dot(np.transpose(joint_pos[11, :])))) + joint_pos[10, :]

        rot_12 = rot_11.dot(e2r(joint_ang[11, :].dot(np.pi / 180)))
        joint_pos[12, :] = (np.transpose(rot_12.dot(np.transpose(joint_pos[12, :])))) + joint_pos[11, :]

        rot_13 = rot_12.dot(e2r(joint_ang[12, :].dot(np.pi / 180)))
        joint_pos[13, :] = (np.transpose(rot_13.dot(np.transpose(joint_pos[13, :])))) + joint_pos[12, :]

        # left leg
        rot_14 = e2r(joint_ang[0, :].dot(np.pi / 180))
        joint_pos[14, :] = (np.transpose(rot_14.dot(np.transpose(joint_pos[14, :])))) + joint_pos[0, :]

        rot_15 = rot_14.dot(e2r(joint_ang[14, :].dot(np.pi / 180)))
        joint_pos[15, :] = (np.transpose(rot_15.dot(np.transpose(joint_pos[15, :])))) + joint_pos[14, :]

        rot_16 = rot_15.dot(e2r(joint_ang[15, :].dot(np.pi / 180)))
        joint_pos[16, :] = (np.transpose(rot_16.dot(np.transpose(joint_pos[16, :])))) + joint_pos[15, :]

        rot_17 = rot_16.dot(e2r(joint_ang[16, :].dot(np.pi / 180)))
        joint_pos[17, :] = (np.transpose(rot_17.dot(np.transpose(joint_pos[17, :])))) + joint_pos[16, :]

        # right leg
        rot_18 = e2r(joint_ang[0, :].dot(np.pi / 180))
        joint_pos[18, :] = (np.transpose(rot_18.dot(np.transpose(joint_pos[18, :])))) + joint_pos[0, :]

        rot_19 = rot_18.dot(e2r(joint_ang[18, :].dot(np.pi / 180)))
        joint_pos[19, :] = (np.transpose(rot_19.dot(np.transpose(joint_pos[19, :])))) + joint_pos[18, :]

        rot_20 = rot_19.dot(e2r(joint_ang[19, :].dot(np.pi / 180)))
        joint_pos[20, :] = (np.transpose(rot_20.dot(np.transpose(joint_pos[20, :])))) + joint_pos[19, :]

        rot_21 = rot_20.dot(e2r(joint_ang[20, :].dot(np.pi / 180)))
        joint_pos[21, :] = (np.transpose(rot_21.dot(np.transpose(joint_pos[21, :])))) + joint_pos[20, :]

        skel[:, :, i] = joint_pos

    return frames,skel
def e2r(x):
    g = x[0]
    b = x[1]
    a = x[2]
    R = rotz(a).dot(roty(b)).dot(rotx(g))
    return R
def rotx(t):
    ct = math.cos(t)
    st = math.sin(t)
    r = [[1, 0, 0],
         [0, ct, -st],
         [0, st, ct]]

    return np.array(r)
def roty(t):
    ct = math.cos(t)
    st = math.sin(t)
    r = [[ct, 0, st],
         [0, 1, 0],
         [-st, 0, ct]]

    return np.array(r)
def rotz(t):
    ct = math.cos(t)
    st = math.sin(t)
    r = [[ct, -st, 0],
         [st, ct, 0],
         [0, 0, 1]]

    return np.array(r)
def smooth(a,WSZ):
    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((  start , out0, stop  ))

def main():
    ##### this is the part where the number of frames in the excercise and the skeleton is returned
    pos = "data/m02_s01_e01_positions.txt"
    angles = "data/m02_s01_e01_angles.txt"
    frames, skel = cartesian_frames(pos, angles)
    #########

    J = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
         [4, 7], [7, 8], [8, 9], [9, 10],
         [4, 11], [11, 12], [12, 13], [13, 14],
         [1, 19], [19, 20], [20, 21], [21, 22],
         [1, 15], [15, 16], [16, 17], [17, 18]]

    J = np.array(J) - 1

    maxX, minX = skel[:, 0, :].max(), skel[:, 0, 0].min()
    maxY, minY = skel[:, 1, :].max(), skel[:, 0, 0].min()
    # maxZ,minZ=skel[:,2,:].max(),skel[:,0,0].min()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    camera = Camera(fig)
    for i in range(frames):
        x = skel[:, 0, i]
        y = skel[:, 1, i]
        z = skel[:, 2, i]

        ax.scatter(maxY, maxY)
        ax.scatter(minY, minY)
        ax.scatter(x, z, y, c='b')

        for p in J:
            p1, p2 = p[0], p[1]
            ax.plot([x[p1], x[p2]], [z[p1], z[p2]], [y[p1], y[p2]], c='b')

        ax.view_init(30, 60)
        camera.snap()
    animation = camera.animate()
    plt.show()

main()


