import sys
import json
import numpy as np
import random

class Data(object):
    
    def __init__(self, path="./"):
        self.file_path = path

    def load_json_to_csv(self, file_prefix, num_play_list):
        out_filename = "./Data/ml-1m.train.rating"
        out_handler = open(out_filename, "w")
        play_lists = []
        track_uris = []
        track_uri2num = {}
        for i in range(num_play_list/1000):
            #mpd.slice.0-999
            filename = file_prefix+"%d-%d" % (i*1000,i*1000+999) + \
                    ".json"
            file_handler = open(filename, "r")
            print filename 
            data = json.load(file_handler)
            for play_list in data["playlists"]:
                print play_list["tracks"][-1]["track_uri"]
                play_lists.append(play_list)
                for track in play_list["tracks"]:
                    track_uris.append(track["track_uri"])

        track_uris = set(track_uris)
        for idx,track_uri in enumerate(list(track_uris)):
            track_uri2num[track_uri] = idx
        
        value = [track_uri2num[x] for x in track_uris]
        print "max value"
        print max(value)

        leave_one = []
        train_track = []
        for idx,play_list in enumerate(data["playlists"]):
            for track in play_list["tracks"][:-1]:
                train_track.append(track)
                ret = "%d\t%d\t1\t%d\n" % \
                (idx, track_uri2num[track["track_uri"]], 978824330)
                out_handler.write(ret)
            leave_one.append((idx,track_uri2num[play_list["tracks"][-1]["track_uri"]]))
        
        
        out_handler.close()
        out_filename = "./Data/ml-1m.test.rating"
        out_handler = open(out_filename, "w")
        for x in leave_one:
            ret = "%d\t%d\t5\t%d\n" % \
                   (x[0],x[1], 978824330)
            out_handler.write(ret)
        out_handler.close()
        
        out_filename = "./Data/ml-1m.test.negative"
        out_handler = open(out_filename,"w")
       
        value = [track_uri2num[track["track_uri"]] for track in train_track]
        print "max value"
        max_track_num =  max(value) 
        reduced_track_uris = []
        for track_uri in track_uris:
            if track_uri2num[track_uri] <= max_track_num:
                reduced_track_uris.append(track_uri)
        reduced_track_uris = set(reduced_track_uris)

        num_to_select = 99
        for idx,play_list in enumerate(play_lists):
            temp_set = set([x["track_uri"] for x in play_list["tracks"]])
            temp_set = track_uris - temp_set
            list_of_random_items = random.sample(list(temp_set), num_to_select)
            ret = "(%d,%d)" % (idx, leave_one[idx][1])
            for item in list_of_random_items:
                ret += "\t%d" % track_uri2num[item]
            ret += "\n"
            out_handler.write(ret)
        out_handler.close()


            
          
        
