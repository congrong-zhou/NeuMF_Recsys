import sys
import numpy as np
from data_process import *

def main():
    path = "./spotify_data/data/"
    fileprefix = path + "mpd.slice."
    num_play_list = 1000
    data = Data()
    data.load_json_to_csv(fileprefix, num_play_list)


if __name__ == "__main__":
    main()


