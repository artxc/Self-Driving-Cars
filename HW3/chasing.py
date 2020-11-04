#! /usr/bin/python

from geometry_msgs.msg import Twist
import numpy as np
import rospy
from turtlesim.msg import Pose


class Chaser:
    def __init__(self):
        self.subscriber_simulator = rospy.Subscriber('/turtle1/pose', Pose, self.chase)
        self.subscriber_chaser = rospy.Subscriber('/chaser/pose', Pose, self.update_pose)

        self.publisher_chaser = rospy.Publisher('/chaser/cmd_vel', Twist, queue_size=10)

        self.pose = Pose()

    def chase(self, pose):
        message = Twist()

        x_dist, y_dist = pose.x - self.pose.x, pose.y - self.pose.y

        distance = np.sqrt(x_dist ** 2 + y_dist ** 2)

        if distance > 0.01:
            theta = np.arctan2(y_dist, x_dist)
            angle = theta - self.pose.theta

            while angle > np.pi:
                angle -= 2 * np.pi
            while angle < -np.pi:
                angle += 2 * np.pi

            message.linear.x = min(distance, 1)
            message.angular.z = angle

            self.publisher_chaser.publish(message)

    def update_pose(self, pose):
        self.pose = pose


rospy.init_node('chasing')
Chaser()
rospy.spin()
