import os
from PIL import ImageStat, Image
import re
import pandas as pd
import matplotlib.pyplot as plt

FRAMES_STORE = "frames"


def brightness(im_file):
    im = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

bright_df = pd.DataFrame(columns=["frame", "brightness"])


if __name__ == "__main__":
    frames_files_list = sorted(os.listdir(FRAMES_STORE))
    for frame_file_name in frames_files_list:
        bright_val = brightness(FRAMES_STORE + "/" + frame_file_name)
        number_in_name = re.search('frame_(\d+).jpg', frame_file_name)
        # print(number_in_name.group(1), bright_val)
        bright_df = bright_df.append({"frame": int(number_in_name.group(1)), "brightness": bright_val}, ignore_index=True)

print(bright_df.info())

bright_df.sort_values("frame", ascending=True, inplace=True)
bright_df = bright_df.reindex()
bright_df.to_csv("frame_brighness_data.csv", columns=["frame", "brightness"], index=False)

bright_df.plot(x="frame", y="brightness")
plt.show()
plt.savefig("frame_brighness_data.pdf")
