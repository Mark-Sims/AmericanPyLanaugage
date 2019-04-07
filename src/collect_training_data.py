import json
import pandas
import os
import pdb
import sys
import time

from leapdata import create_frame_dict

# Add Leap libraries
sys.path.append("..\\lib")
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.append(arch_dir)
import Leap

# Create a controller
controller = Leap.Controller()

alphabet = map(chr, range(97, 123))
letter_index = 0

training_data = []
num_frames_required = 50

while letter_index < len(alphabet):
    try:
        if not controller.is_connected:
            print "No controller detected!"
            time.sleep(2)
            continue;
        print "Collecting training data for letter {}. Press ENTER to begin".format(alphabet[letter_index])
        sys.stdin.readline()

        num_frames_collected = 0
        previous_frame_id = -1
        while num_frames_collected < num_frames_required:
            frame, frame_id = create_frame_dict(controller)
            if frame is not None and frame_id is not None and frame_id != previous_frame_id:
                frame['letter'] = alphabet[letter_index]
                training_data.append(frame)
                num_frames_collected += 1
                previous_frame_id = frame_id
                
                # Basic progress indicator every 10% of progress we make
                if (num_frames_collected % (num_frames_required / 10)) == 0:
                    print "Collected {}/{} frames for letter {}".format(num_frames_collected, num_frames_required, alphabet[letter_index])

                if num_frames_collected >= num_frames_required:
                    letter_index += 1
    except KeyboardInterrupt:
        exit()

pdb.set_trace()
with open('data.json', 'w') as fp:
    json.dump(training_data, fp)