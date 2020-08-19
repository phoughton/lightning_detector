import os
import datetime
import argparse
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from progress.spinner import Spinner

parser = argparse.ArgumentParser(description='Extract lightning frames from a video.')
parser.add_argument('video_file_name', type=str,
                   help='The file with the lightning in it')
parser.add_argument('--threshold', dest='threshold', action='store',
                   default=10,
                   help='Use a non-default (default is 10) threshold for detirming what a lightning flash is.')
args = parser.parse_args()

THRESHOLD = args.threshold
VIDEO_FILE_NAME = args.video_file_name

print(f"Using Threshold: {THRESHOLD}")
print(f"Using Video File Name: {VIDEO_FILE_NAME}")


if __name__ == '__main__':

    if not os.path.isfile(VIDEO_FILE_NAME):
        print(f"File not found: {VIDEO_FILE_NAME}")
        print("Exiting...")
        exit(404)

    print(f"Starting at: {datetime.datetime.now().isoformat()}")    

    if not os.path.isdir("frames"):
        os.mkdir("frames")

    cap = cv2.VideoCapture(VIDEO_FILE_NAME)

    frame_num = 0
    frame_data = []
    spinner = Spinner('Processing ')

    while (cap.isOpened()):

        ret, frame = cap.read()
        if not ret:
            print(f"Looks like we are done at Frame number: {frame_num}")
            break

        mean_brightness = np.mean(frame)
        store_frame = mean_brightness > THRESHOLD

        if store_frame:
            cv2.imwrite('frames/frame_' + str(frame_num) + '.jpg', frame)

        frame_data.append([frame_num, mean_brightness, store_frame])
        frame_num += 1
        spinner.next()

    cap.release()
    cv2.destroyAllWindows()
    print(f"Ending at: {datetime.datetime.now().isoformat()}")
    
    if len(frame_data) == 0:
        print(f"Looks like no data was found, was this file location ok?:{VIDEO_FILE_NAME}")
        exit(400)
        
    df = pd.DataFrame(frame_data, columns=["frame_num", "brightness", "stored_image"] )

    print(df)
    df.to_csv("frame_brighness_data.csv", columns=["frame_num", "brightness", "stored_image"], index=False)

    df.plot(x="frame_num", y="brightness")
    plt.show()
    plt.savefig("frame_brighness_data.pdf")
