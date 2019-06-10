import cv2

#"cam_list"にあるカメラそれぞれで、キャプチャして"rame_list"へ保存
def cap_func(cam_list, frame_list):
    for i, cam in enumerate(cam_list):
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        ret, frame_list[i] = cam.read()

#"frame"内にある、マーカーを検知し、あればIDとポジションを"marker_posi_id_list"へ保存
def detection_func(i, frame, marker_posi_id_list):
    dictionary_name = cv2.aruco.DICT_4X4_50
    dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)
    marker_posi_id_list[i] = cv2.aruco.detectMarkers(frame, dictionary)

#"marker_posi_id"内にある、マーカーIDから、"marker_num"と一致するものを見つけ、そのときのx,y座標を返す
def marker_selection(marker_num, marker_posi_id):
    x = None
    y = None
    for i, marker_id in enumerate(marker_posi_id[1]):
        if marker_id == marker_num :
            x = marker_posi_id[0][i][0][0][0]
            y = marker_posi_id[0][i][0][0][1]

    return x, y