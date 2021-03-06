#!usr/bin/env python
"""
Robot arm Control Script
Script to control the Workshop arms so that they go to a point
Created for Semester 1 workshops 2018
@author: Andrew Razjigaev President of QUT Robotics Club
"""

import smbus, numpy, time, getch

from math import sin, cos, pi

from RobotarmServo_module import pi_servo, initialise_piHat

from RobotarmKinematics_module import update_joints, WorkspaceBoundaryCheck, measure_position_error, DH_matrix, ForwardKinematics, compute_error, compute_Jacobian, damped_least_squares

from RobotarmUtility_module import read_keyboard, move_arm, Move_arm_to_home, Reset_robot_arm, read_arm, Initialise_Robot_arm, robotarmLimits


# ***** MAIN ***** #
if __name__ == "__main__":

    print('STARTING ROBOT ARM...')
    
    ####INITIALISATION####
    #Initialise the Pi hat
    bus = smbus.SMBus(1) # the chip is on bus 1 of the available I2C buses
    addr = 0x40  # I2C address of the PWM chip.
    initialise_piHat()
    
    #Initialises the whole robot arm
    (m1,m2,m3,m4,m5) = Initialise_Robot_arm(bus)
    
    #Start arm at home position
    Move_arm_to_home(m1,m2,m3,m4,m5,bus)

    ####DEFINITIONS####
    #Measure arm segments l1,l2,l3,l4
    arm_lengths = (100,120,140,140)

    #Determine initial position set the desired pose there
    joint_values = read_arm(m1,m2,m3,m4)
    #initial conditions (0.0, 135.0, -100.0, -90.0)

    #Speed limit for velocity control:
    speedlimit = 10 # mm per dt

    #set pwmValues for gripper:
    closed_grip_value = 410
    open_grip_value = 900

    #Set Initial target to be its starting point
    Desired_pose = ForwardKinematics(joint_values,arm_lengths)

    #While loop for the control
    on = True
    #set gripper to initially be closed
    grip_value = closed_grip_value

    print('Running loop ... Press keys now')
    
    ####CONTROL LOOP####
    #Run loop to follow the desired pose updated by the keyboard
    while(on):

        #Compute the Current tool point Location
        tool_point = ForwardKinematics(joint_values,arm_lengths)
        
        #Read the keyboard presses and compute the new pose and gripper and
        #whether the user killed the robot
        (Desired_pose,grip_value,on) = read_keyboard(Desired_pose,grip_value,on,closed_grip_value,open_grip_value)


        #Check if the tool_point is within 2mm to the desired pose:
        if measure_position_error(Desired_pose,tool_point)>2:
            
            #Keep moving to target
            #compute the error vector and normalise it to the speed limit
            dX = compute_error(Desired_pose,tool_point,speedlimit)

            #compute the Jacobian / derivative of tool and joint
            J = compute_Jacobian(joint_values,arm_lengths)

            #Retrieve Joint Limits
            (joint_mins, joint_maxs) = robotarmLimits(m1,m2,m3,m4)
            
            #Compute the inverse Jacobian 
            inv_J = damped_least_squares(J, joint_values, joint_mins, joint_maxs)
            
            #Estimate the required joint update to reduce positon error
            dQ = numpy.dot(inv_J,dX)

            #update the joints
            new_joint_values = update_joints(joint_values,dQ)

            #Check if update is consistent with workspace:
            if WorkspaceBoundaryCheck(joint_values, new_joint_values, joint_mins, joint_maxs) is True:
                #Keep the user input inside workspace by setting it is the current tool point:
                Desired_pose = tool_point

            #Move the robot arm
            move_arm(new_joint_values,grip_value,m1,m2,m3,m4,m5,bus)

            #Read the current joint angles
            joint_values = read_arm(m1,m2,m3,m4)

        else:
            #Update only gripper
            #Move the robot arm
            move_arm(joint_values,grip_value,m1,m2,m3,m4,m5,bus)


    #END STATE    
    #When the user kills the while loop, reset the robot and turn off 
    Reset_robot_arm(m1,m2,m3,m4,m5,bus)
    print('ROBOT ARM PROGRAM HAS ENDED')
