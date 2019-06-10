import cv2
import math
import numpy as np
import util
import matplotlib.pyplot as plt

from util import cap_func, detection_func, marker_selection
from multiprocessing import Manager, Process
from mpl_toolkits.mplot3d import Axes3D

def init_ax(ax):
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Y")
    ax.set_xlim(0,700)
    ax.set_ylim(0,1000)
    ax.set_zlim(0,600)

if __name__ == "__main__":
    cam_num_list = [0, 1]   #"cameranumconfirm.py"にて確認した番号を用いる。
    cam_list = []
    cal_factor = 75000 
    mg = Manager()
    frame_list = mg.list()
    cam_marker_posi_id_list = mg.list()
    main_frame = None
    fig = plt.figure()
    ax = Axes3D(fig)
    Width = 640
    Height = 480

    for i in cam_num_list:
        cam_list.append(cv2.VideoCapture(cam_num_list[i]))
        frame_list.append(None)
        cam_marker_posi_id_list.append(None)

    while True:
        plt.cla()
        init_ax(ax)
        cap_func(cam_list, frame_list)
        jobs =[]

        for i, frame in enumerate(frame_list):
            detection_func(i, frame, cam_marker_posi_id_list)
        #     p = Process(target=detection_func, args=(i, frame, cam_marker_posi_id_list))
        #     jobs.append(p)
        #     p.start()
        
        # for job in jobs:
        #     job.join()

        if cam_marker_posi_id_list[0][0] and cam_marker_posi_id_list[1][0]:
            # frame1 = cv2.aruco.drawDetectedMarkers(frame_list[0], cam_marker_posi_id_list[0][0], cam_marker_posi_id_list[0][1])
            distance = []
            for i in range(4):
                marker_posi_list = []
                for marker_posi_id in cam_marker_posi_id_list:
                    marker_posi_list.append(marker_selection(i, marker_posi_id))
                if marker_posi_list[0][0] != None and marker_posi_list[1][0] != None:
                    parallax_x = marker_posi_list[0][0] - marker_posi_list[1][0]
                    parallax_y = marker_posi_list[0][1] - marker_posi_list[1][1]
                    distance.append([marker_posi_list[0][0], marker_posi_list[0][1], marker_posi_list[1][0], marker_posi_list[1][1], cal_factor / math.sqrt(parallax_x ** 2) ])
            
            if len(distance) >= 4:
                print("4 Points detected!!")
                print(distance)
                X = np.array([[distance[0][0], distance[1][0]],[distance[3][0], distance[2][0]]])
                Y = np.array([[Height - distance[0][1], Height - distance[1][1]],[Height - distance[3][1], Height - distance[2][1]]])
                Z = np.array([[distance[0][4],distance[1][4]],[distance[3][4],distance[2][2]]])
                ax.plot_surface(X,Z,Y,alpha = 0.3) 
            
        plt.pause(0.01)
        # frame1 = frame_list[0]
        # cv2.imshow('Edited Frame', frame1)
        # k = cv2.waitKey(1)
        # if k == 27:
        #     break