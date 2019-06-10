import cv2
import math

from util import cap_func, detection_func, marker_selection
    
if __name__ == "__main__":
    cam_num_list = [0, 1] #"cameranumconfirm.py"にて確認した番号を用いる。
    cam_list = []
    frame_list = []
    cam_marker_posi_id_list = []
    main_frame = None

    for i in cam_num_list:
        cam_list.append(cv2.VideoCapture(cam_num_list[i]))
        frame_list.append(None)
        cam_marker_posi_id_list.append(None)
    while True:
        cap_func(cam_list, frame_list)
        for i, frame in enumerate(frame_list):
            detection_func(i, frame, cam_marker_posi_id_list)

        if cam_marker_posi_id_list[0][0] and cam_marker_posi_id_list[1][0]:
            frame_list[0] = cv2.aruco.drawDetectedMarkers(frame_list[0], cam_marker_posi_id_list[0][0], cam_marker_posi_id_list[0][1])
            frame_list[1] = cv2.aruco.drawDetectedMarkers(frame_list[1], cam_marker_posi_id_list[1][0], cam_marker_posi_id_list[1][1])            
            cal_posi_list = []
            for i in range(4):
                marker_posi_list = []
                for marker_posi_id in cam_marker_posi_id_list:
                    marker_posi_list.append(marker_selection(i, marker_posi_id))
                if marker_posi_list[0][0] != None and marker_posi_list[1][0] != None:
                    parallax_x = marker_posi_list[0][0] - marker_posi_list[1][0]
                    parallax_y = marker_posi_list[0][1] - marker_posi_list[1][1]
                    cal_posi_list.append([marker_posi_list[0][0], marker_posi_list[1][0], parallax_x, marker_posi_list[0][1], marker_posi_list[1][1], parallax_y, math.sqrt(parallax_x ** 2 + parallax_y ** 2) ])
            if len(cal_posi_list) >= 4:
                print("4 Points detected!!")
                print(cal_posi_list)
        else :
            pass

        frame1 = cv2.hconcat(frame_list)
        cv2.imshow('Edited Frame', frame1)

        k = cv2.waitKey(1)
        if k == 27:
            break