import cv2

#"cam_list"にあるカメラそれぞれで、キャプチャ、サイズ変更、数字添付して"rame_list"へ保存
def cap_func(cam_list, frame_list):
    for i, cam in enumerate(cam_list):
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        print(i,"H:",cam.get(cv2.CAP_PROP_FRAME_HEIGHT),"W:",cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        ret, frame_list[i] = cam.read()
        frame_list[i] = cv2.putText(frame_list[i], str(i), (0, 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
    
if __name__ == "__main__":
    cam_num_list = [0, 1]   #カメラに割り振られた番号を確認（接続台数を超えるとエラー）　<例>3台接続されているならcam_num_list = [0,1,2]
    cam_list = []
    frame_list = []

    for i in cam_num_list:
        cam_list.append(cv2.VideoCapture(cam_num_list[i]))
        frame_list.append(None)
    while True:
        cap_func(cam_list, frame_list)
        frame1 = cv2.hconcat(frame_list)
        cv2.imshow('Edited Frame', frame1)
        k = cv2.waitKey(1)
        if k == 27: #Escで終了
            break