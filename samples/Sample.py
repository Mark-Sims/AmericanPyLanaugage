################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, pdb, json

sys.path.append("..\\lib")
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.append(arch_dir)

import Leap

# Globals for hacky data collection
data = []
collection_letter = ""
lister = None
controller = None
iterations = 250

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    global data
    global collection_letter
    global lister
    global controller

    def on_init(self, controller):
        # print "Initialized"
        pass

    def on_connect(self, controller):
        print "In progress.."

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        # print "Exited"
        pass

    def on_frame(self, controller):

        # print "collection letter '{}'".format(collection_letter)
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        dict = {}

        dict['letter'] = collection_letter

        # print "collection_letter: '{}'".format(collection_letter)
        if len(data) >= iterations:
            print "Record collection limit reached. No longer collecting records for '{}'".format(collection_letter)
            controller.remove_listener(listener)
            return


        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"

            if(handType == "Left hand"):
                return None
            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            dict['hand_normal_x'] = float(normal.x)
            dict['hand_normal_y'] = float(normal.y)
            dict['hand_normal_z'] = float(normal.z)
            dict['hand_direction_x'] = float(direction.x)
            dict['hand_direction_y'] = float(direction.y)
            dict['hand_direction_z'] = float(direction.z)

            # Get fingers
            for finger in hand.fingers:
                f = self.finger_names[finger.type]

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    b = str(self.bone_names[bone.type])
                    if(b != 'Metacarpal' or f != 'Thumb'):
                        dict[f + "_" + b + "_x"] = float(bone.direction.x)
                        dict[f + "_" + b + "_y"] = float(bone.direction.y)
                        dict[f + "_" + b + "_z"] = float(bone.direction.z)
            data.append(dict)


def main():
    global collection_letter
    global letter
    global listener
    global controller
    global data
    global iterations

    # data_gatherer = DataGatherer()
    # Create a sample listener and controller
    listener = SampleListener()


    letters = ['a', 'b', 'c',
    'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z']
    for letter in letters:
        print "Sign: " + letter
        controller = Leap.Controller()
        controller.add_listener(listener)
        try:
            collection_letter = letter
            sys.stdin.readline()
            # for letter in letters:
            #     collection_letter = letter
            #     #print(data)
            #     # if(letter!=''):
            #     #     iterations+=200
            #     iterations+=100
            #     print "About to collect letter '{}'. Press ENTER to start.".format(letter)
            #     sys.stdin.readline()
            #     listener = SampleListener()
            #     controller.add_listener(listener)
            #     # Have the sample listener receive events from the controller
            #
            #
            #     print "Collecting letter '{}'.".format(letter)
            #     #time.sleep(1)
            #     #time.sleep(10) # 1 second delay since it takes a minute for the listener to get going
        except KeyboardInterrupt:
            print "interrupt"
            pass
        finally:
            # Remove the sample listener when done
            controller.remove_listener(listener)
        iterations+=500


    # end of stuff
    #print data
    #print(len(data))
    a_count=0
    b_count=0
    c_count=0
    '''
    for dict in data:
        if dict['letter'] == 'a':
            a_count+=1
        elif dict['letter'] == 'b':
            b_count +=1
        elif dict['letter'] == 'c':
            c_count +=1
    print("a_count: {}, b_count: {}, c_count: {}").format(a_count, b_count, c_count)
    '''
    with open('dat2.json', 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    main()
