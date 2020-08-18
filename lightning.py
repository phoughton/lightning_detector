import os
import datetime
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


THRESHOLD = 10

if __name__ == '__main__':
    
    print(datetime.datetime.now().isoformat())    
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    cap = cv2.VideoCapture('/mnt/c/Users/pete_/OneDrive/Pictures/20200814_gopro/GP060259.MP4.avi')

    frame_num = 0
    frame_data = []

    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            print(f"Looks like we are done at Frame number: i:{frame_num}")
            break
        
        mean_brightness = np.mean(frame)
        store_frame = mean_brightness > THRESHOLD

        if store_frame:
            cv2.imwrite('frames/frame_' + str(frame_num) + '.jpg', frame)

        frame_data.append([frame_num, mean_brightness, store_frame])

        frame_num += 1

    cap.release()
    cv2.destroyAllWindows()
    print(datetime.datetime.now().isoformat())
    df = pd.DataFrame(frame_data, columns=["frame_num", "brightness", "stored_image"] )

    print(df)
    df.to_csv("frame_brighness_data.csv", columns=["frame_num", "brightness", "stored_image"], index=False)

    df.plot(x="frame_num", y="brightness")
    plt.show()
    plt.savefig("frame_brighness_data.pdf")
