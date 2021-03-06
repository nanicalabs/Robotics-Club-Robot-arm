#!usr/bin/env python

#import files
import smbus, time

from RobotarmServo_module import pi_servo

#Initialise communication bus
bus = smbus.SMBus(1)
addr = 0x40

bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)
    

#START PROGRAM
if __name__ == "__main__":

    #initialise each joint
    q1 = pi_servo()
    q1._init_channel(0)
    q1._calibrate_servo(-45,0,45)
    q1.define_jointlimits(-50,50)
    
    q2 = pi_servo()
    q2._init_channel(1)
    q2._calibrate_servo(55,96,141)
    q2.define_jointlimits(40,150)
        
    q3 = pi_servo()
    q3._init_channel(2)
    q3._calibrate_servo(-25,-65,-110)
    q3.define_jointlimits(-120,-10)
        
    q4 = pi_servo()
    q4._init_channel(3)
    q4._calibrate_servo(-90,-45,-5)
    q4.define_jointlimits(-110,0)

    gripper = pi_servo()
    gripper._init_channel(4)
    gripper._calibrate_servo(0,30,60)
    gripper.define_jointlimits(0,60)

    #Start each joint
    q1.fstart(bus)
    q2.fstart(bus)
    q3.fstart(bus)
    q4.fstart(bus)
    gripper.fstart(bus)

    #Motion commands
    print('q1')
    q1.move_deg(-45,bus)
    input('PWM=836 angle should be -45')
    q1.move_deg(0,bus)
    input('PWM=1250 angle should be 0')
    q1.move_deg(45,bus)
    input('PWM=1664 angle should be 45')
    q1.move_pwm(1250,bus)
    time.sleep(1)
    
    print('q2')
    q4.move_pwm(1664,bus)
    q3.move_pwm(836,bus)
    time.sleep(0.5)
    q2.move_deg(45,bus)
    input('PWM=836 angle should be 45')
    q2.move_deg(90,bus)
    time.sleep(0.5)
    q4.move_pwm(836,bus)
    input('PWM=1250 angle should be 90')
    q2.move_deg(135,bus)
    input('PWM=1664 angle should be 135')

    print('q3 - has negative commands')
    q3.move_deg(-25,bus)
    input('PWM=836 angle should be -25')
    q3.move_deg(-60,bus)
    input('PWM=1250 angle should be -60')
    q3.move_deg(-105,bus)
    input('PWM=1664 angle should be -105')

    print('q4')
    q4.move_deg(-100,bus)
    input('PWM=836 angle should be -100')
    q4.move_deg(-55,bus)
    input('PWM=1250 angle should be -55')
    q4.move_deg(-10,bus)
    input('PWM=1664 angle should be -10')
    q4.move_pwm(836,bus)
    time.sleep(1)

    print('gripper action')
    gripper.move_pwm(1000,bus)
    print('PWM=1000 open')
    time.sleep(1)
    gripper.move_pwm(410,bus)
    print('PWM=550 closed')
    time.sleep(1)
    gripper.move_pwm(1000,bus)
    print('PWM=1000 open')
    time.sleep(1)
    gripper.move_pwm(410,bus)
    print('PWM=550 closed')
    time.sleep(1)

    #Reset
    print('RESETTING ROBOT')
    q1.move_deg(0,bus)
    q2.move_deg(135,bus)
    q3.move_deg(-105,bus)
    q4.move_deg(-100,bus)
    gripper.move_pwm(410,bus)
    time.sleep(1)
    
    print('Ending code')
    #Stop all joints
    q1.fstop(bus)
    q2.fstop(bus)
    q3.fstop(bus)
    q4.fstop(bus)
    gripper.fstop(bus)   
