import os
import json

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'..\\data\\')

files = [
    os.path.join(data_dir, "v.json"),
    os.path.join(data_dir, "x.json"),
    os.path.join(data_dir, "r.json"),
    os.path.join(data_dir, "x.r.messed.json")
]

loaded_frames = []
for file in files:
    with open(file, 'r') as fp:
        loaded_json = json.load(fp)
        if file == files[-1]:
            loaded_json = [d for d in loaded_json if str(d['letter']) != 'x']
            loaded_json = [d for d in loaded_json if str(d['letter']) != 'r']
            loaded_json = [d for d in loaded_json if str(d['letter']) != 'v']
        loaded_frames.extend(loaded_json)

with open('mine.json', 'w') as fp:
    json.dump(loaded_frames, fp)