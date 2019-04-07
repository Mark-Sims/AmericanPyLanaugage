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

finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

def create_frame_dict(controller):

    dict = {}
    frame = controller.frame()

    if len(frame.hands) == 0:
        return None, None
    # Get hands
    for hand in frame.hands:
        handType = "Left hand" if hand.is_left else "Right hand"

        # Don't care about left hand just yet...
        if(handType=="Left hand"):
            return None, None

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        dict['hand_normal_x'] = float(normal.x)
        dict['hand_normal_y'] = float(normal.y)
        dict['hand_normal_z'] = float(normal.z)
        dict['hand_direction_x'] = float(direction.x)
        dict['hand_direction_y'] = float(direction.y)
        dict['hand_direction_z'] = float(direction.z)

        # Get arm bone
        arm = hand.arm

        # Get fingers
        for finger in hand.fingers:
            f = finger_names[finger.type]

            # Get bones
            for b in range(0, 4):
                bone = finger.bone(b)
                b = str(bone_names[bone.type])
                if(b != 'Metacarpal' or f != 'Thumb'):
                    dict[f + "_" + b + "_x"] = float(bone.direction.x)
                    dict[f + "_" + b + "_y"] = float(bone.direction.y)
                    dict[f + "_" + b + "_z"] = float(bone.direction.z)
    return dict, frame.id

# def main():
#     # Create a controller
#     controller = Leap.Controller()

#     while True:
#         if controller.is_connected:
#             print create_frame_dict(controller)
#         else:
#             print "No controller connected, sleeping..."
#         # Delay
#         time.sleep(1)
    # print json.dumps(data, fp)

    # print data


if __name__ == "__main__":
    main()
