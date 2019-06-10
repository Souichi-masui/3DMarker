import cv2 

if __name__ == "__main__":

    aruco = cv2.aruco

    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    for i in range(4):  #必用なマーカー数に応じて変更　<例>5個ならば　for i in range(5):
        fileName = "ar_marker_" + str(i) + ".png"
        generator = aruco.drawMarker(dictionary, i, 100)
        cv2.imwrite(fileName, generator)