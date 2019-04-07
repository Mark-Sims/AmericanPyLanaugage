################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, json
import pdb

sys.path.append("..\\lib")
sys.path.append("..\\lib\\x64")

letter = 'a'

import Leap

# Globals for hacky data collection
data = {}
collection_letter = ""
lister = None
controller = None

class SampleListener(Leap.Listener):
    list = []
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
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print len(self.list)
        print "Completed"

    def on_frame(self, controller):

        # print "collection letter '{}'".format(collection_letter)
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        dict={}
        dict['letter'] = chr(letter)
        # Get hands
        for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"


            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)
            dict['handType'] = str(handType)
            dict['hand.id'] = str(hand.id)
            dict['hand.palm_position'] = str(hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            dict['hand_normal'] = str(normal)
            dict['hand_direction'] = str(direction)

            # Calculate the hand's pitch, roll, and yaw angles
            # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
            #     direction.yaw * Leap.RAD_TO_DEG)

            dict['pitch'] = str(direction.pitch * Leap.RAD_TO_DEG)
            dict['roll'] = str(normal.roll * Leap.RAD_TO_DEG)
            dict['yaw'] = str(direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            #     arm.direction,
            #     arm.wrist_position,
            #     arm.elbow_position)

            #dict['arm'] = str(arm)
            dict['wrist_pos'] = str(arm.wrist_position)
            dict['elbow_pos'] = str(arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type],
                #     finger.id,
                #     finger.length,
                #     finger.width)
                dict['finger_'+str(finger.id)] = self.finger_names[finger.type]
                dict['finger_id_'+str(finger.id)] = str(finger.id)
                #dict['finger_length_'+str(finger.id)] = str(finger.length)
                dict['finger_width_'+str(finger.id)] = str(finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #     self.bone_names[bone.type],
                    #     bone.prev_joint,
                    #     bone.next_joint,
                    #     bone.direction)
                    dict['bone'] = str(self.bone_names[bone.type])
                    dict['bone_start_'+ str(self.bone_names[bone.type])] = str(bone.prev_joint)
                    dict['bone_end_' + str(self.bone_names[bone.type])] = str(bone.next_joint)
                    dict['bone_direction_' + str(self.bone_names[bone.type])] = str(bone.direction)


        if not frame.hands.is_empty:
            print(len(self.list))
            if(len(self.list) < 3000):
                self.list.append(dict)


def main(letter):
    # Create a sample listener and controller

    listener = SampleListener()
    controller = Leap.Controller()
    
    letters = ['a', 'b', 'c', 'd', 'e']

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)




    #Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        for letter in letters:
            collection_letter = letter
            data[collection_letter] = []

            print "About to collect letter '{}'. Press ENTER to start.".format(letter)
            sys.stdin.readline()
            # Have the sample listener receive events from the controller    
            controller.add_listener(listener)

            print "Collecting letter '{}'.".format(letter)
            time.sleep(1) # 1 second delay since it takes a minute for the listener to get going
    except KeyboardInterrupt:
        pass
    finally:
        #Remove the sample listener when done
        list = listener.list
    #controller.remove_listener(listener)
    return list

    print data


if __name__ == "__main__":
    dict = {}
    for let in range(ord('a'),ord('c')+1):
        raw_input("Sign letter '{}' and press enter".format(chr(let)))
        letter = let
        lst = main(chr(let))
    with open('data.json', 'w') as fp:
        json.dump(lst, fp)
