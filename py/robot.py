from uarm.wrapper import SwiftAPI
import time
import numpy as np
from camera import Camera


class Robot:
    def __init__(self):
        try:
            self.swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})                        # Robot serial number
            self.swift.waiting_ready(timeout=3)
                # print(swift.get_device_info())
            self.robot_status = self.swift.get_device_info()   
        except:
            pass      

        self.camera = Camera()      

    def status(self):
        try:
            self.swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})                        # Robot serial number
            self.swift.waiting_ready(timeout=3)
            # print(swift.get_device_info())
            robot_status = self.swift.get_device_info()            
            return "Connected", robot_status['device_type'], robot_status['hardware_version']                                            
        except:
            return "Not Connected", "---", "---"

    def get_position(self):
        robot_position = self.swift.get_position() 

        return robot_position

    def default_position(self):
        self.swift.reset()
    
    def detact_robot(self):
        self.swift.set_servo_detach()

    def attach_robot(self):
        self.swift.set_servo_attach()

    def move_robot(self, x, y, z, speed=30, wait=True):
        self.swift.set_position(x=x, y=y, z=z, speed=speed, wait=wait) 

    def pump(self, status=False):
        self.swift.set_pump(on=status)

    def test_robot(self):
        self.swift.set_wrist(90)

        time.sleep(2)

        self.swift.set_wrist(0)

        time.sleep(2)

        self.swift.set_wrist(90)

        time.sleep(2)

        self.swift.set_wrist(180)

        time.sleep(2)

        self.swift.set_wrist(90)

    def move_object(self, x_start, y_start, x_end, y_end, z=150, speed=30, wait=True):
        """
        Move object from original position to desire position

        Args:
            x_start (float) : original X coordinate 
            y_start (float) : original Y coordinate  
            z_start (float) : original Z coordinate   
            x_end (float) : Desire X coordinate  
            y_end (float) : Desire Y coordinate   
            z_end (float) : Desire Z coordinate   
            speed (int) : How fast robot movement
            wait (int) : Delay for every movement

        Returns:
            Robot coordinate (X, Y, Z)
        """
        status = self.terminal_robot.text + " | X: " + str(x_start) + " Y: " + str(y_start) + " Z: " + str(z) + "\n"
        self.terminal_robot.text = status

        # X, Y, Z, SPEED
        # goto X, Y position
        self.move_robot(x_start, y_start, z, speed=speed, wait=wait)
        time.sleep(1)

        # slide down to Z position
        status = self.swift.get_limit_switch()
        while (status != True):
            z_coor = z-1
            self.move_robot(x_start, y_start, z_coor, speed=speed/2, wait=wait)

        # Coordinate  
        # status = self.terminal_robot.text + " | X: " + str(x_end) + " Y: " + str(y_end) + " Z: " + str(z_coor) + "\n"
        # self.terminal_robot.text = status

        # turn on pump
        self.pump(True)
        time.sleep(1)
        # self.swift.set_position(self.robot_parkir[0], self.robot_parkir[1], self.robot_parkir[2], speed=speed, wait=wait)
        self.move_robot(x_start, y_start, z, speed=speed, wait=wait)
        time.sleep(1)

        # X, Y, Z, SPEED
        self.move_robot(x_end, y_end, z, speed=speed, wait=wait)
        time.sleep(1)
        
        # slide down to Z position
        status = self.swift.get_limit_switch()
        while (status != True):
            z_coor = z-1
            self.move_robot(x_end, y_end, z_coor, speed=speed/2, wait=wait)
        
        # Coordinate  
        # status = self.terminal_robot.text + " | X: " + str(x_end) + " Y: " + str(y_end) + " Z: " + str(z_coor) + "\n"
        # self.terminal_robot.text = status

        # turn off pump
        self.pump(False)
        time.sleep(1)
        self.move_robot(x_end, y_end, z, speed=speed, wait=wait)
        time.sleep(1)
        self.default_position()

    def robot_test_move(self, input_marker_id, coordinate_marker_for_robot, camera_tvec, T):
        """
        Test robot coordinate using Aruco Marker

        Args:
            T (matrix) : Translation matrix
            coordinate_marker_for_robot (list) : coordinate robot (X, Y, Z)

        Returns:
            Robot movement
        """
        if (len(coordinate_marker_for_robot) == 0):    # check if Transformation Matrix still not calculated
            # self.calculate_final_matrix()                   # Calculate Transformation Matrix
            coordinate_marker_for_robot = self.camera.final_matrix(camera_tvec, T)

        if int(input_marker_id) in coordinate_marker_for_robot:
            x = coordinate_marker_for_robot[int(input_marker_id)][0]
            y = coordinate_marker_for_robot[int(input_marker_id)][1]
            z = coordinate_marker_for_robot[int(input_marker_id)][2]
            # X, Y, Z, SPEED
            self.move_robot(x, y, z, speed=30, wait=True)                       # Send coordinate to robot
            time.sleep(2)                                                       # delay for 2 second
            self.default_position()                                             # reset robot position
    

if __name__ == '__main__':
    robot = Robot()
    status, device_info, hardware_version = robot.check()
    print(f'Status: {status}, Device info: {device_info}, Hardware version: {hardware_version}')
    time.sleep(2)
    position = robot.default_position()
    print(f'Posotion: {position}')
    robot.test_robot()

