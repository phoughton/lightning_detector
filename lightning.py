import os
import time
import cv2


if __name__ == '__main__':
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    cap = cv2.VideoCapture('/mnt/c/Users/pete_/OneDrive/Pictures/20200814_gopro/GP060259.MP4.avi')
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            print(f"ret is false, i:{i}")
            break
        time.sleep(0.5)
        cv2.imwrite('frames/frame_' + str(i) + '.jpg', frame)
        i += 1

    cap.release()
    cv2.destroyAllWindows()
