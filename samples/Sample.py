################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time, pdb

sys.path.append("..\\lib")
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.append(arch_dir)

import Leap

# Globals for hacky data collection
data = {}
collection_letter = ""
lister = None
controller = None

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
        print "Connected"

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

        # print "collection_letter: '{}'".format(collection_letter)
        if len(data[collection_letter]) <= 10:
            data[collection_letter].append(collection_letter)
        else:
            print "Record collection limit reached. No longer collecting records for '{}'".format(collection_letter)
            controller.remove_listener(listener)
            return

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #       frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: %s" % (
            #     handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            # print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #     direction.pitch * Leap.RAD_TO_DEG,
            #     normal.roll * Leap.RAD_TO_DEG,
                # direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
            #     arm.direction,
            #     arm.wrist_position,
            #     arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type],
                #     finger.id,
                #     finger.length,
                #     finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #     self.bone_names[bone.type],
                    #     bone.prev_joint,
                    #     bone.next_joint,
                    #     bone.direction)

        # if not frame.hands.is_empty:
        #     print ""


def main():
    global collection_letter
    global letter
    global listener
    global controller
    global data

    # data_gatherer = DataGatherer()
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    
    letters = ['a', 'b', 'c', 'd', 'e']

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
        # Remove the sample listener when done
        controller.remove_listener(listener)

    print data


if __name__ == "__main__":
    main()
