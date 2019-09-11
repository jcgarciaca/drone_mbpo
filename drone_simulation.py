#!/usr/bin/env python
import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, Pose, PoseArray
from std_msgs.msg import Header
from tf import transformations
from math import radians
from copy import deepcopy

points = [[0.0,0.0,0.0,0.0]]

def main():
    rospy.init_node("drone_simulation_node", anonymous = True)
    
    file_path = '/home/msdc/jcgarciaca/catkin_ws/src/general_tests/trajectory/trajectory.txt'
    f = open(file_path, 'r')
    for x in f:
        data_str = x.split(',')
        data = []
        for num, value in enumerate(data_str):
            data.append(float(value.split('\n')[0]))
        points.append(data)
    
    marker_points_pub = rospy.Publisher("points_marker", Marker, queue_size = 1)
    marker_lines_pub = rospy.Publisher("lines_marker", Marker, queue_size = 1)
    pose_pub = rospy.Publisher('drone_pose', PoseArray, queue_size = 1)

    origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
    frame_name_r = 'map'
    rospy.loginfo('Node started')
    
    points_r = Marker()    
    points_r.header.frame_id = frame_name_r
    points_r.header.stamp = rospy.Time.now()
    points_r.ns = "points_and_lines"
    points_r.action = Marker.ADD
    points_r.pose.orientation.w = 1.0
        
    lines_r = Marker()
    lines_r.header.frame_id = frame_name_r
    lines_r.header.stamp = rospy.Time.now()
    lines_r.ns = "points_and_lines"
    lines_r.action = Marker.ADD
    lines_r.pose.orientation.w = 1.0
            
    points_r.id = 0    
    lines_r.id = 1
        
    points_r.type = Marker.POINTS
    lines_r.type = Marker.LINE_STRIP
        
    points_r.scale.x = 0.04
    points_r.scale.y = 0.04        
    points_r.color.r = 1.0
    points_r.color.a = 1.0        
    
    lines_r.scale.x = 0.02
    lines_r.scale.y = 0.02        
    lines_r.color.g = 1.0
    lines_r.color.a = 1.0    
    
    max_num = len(points) + 1# 4

    while not rospy.is_shutdown():    
        points_r.points = []
        lines_r.points = []
        poses_array = PoseArray()
        poses_array.header.frame_id = 'map'
        ind = 0
        for point in points:
            point_tmp = Point()
            point_tmp.x = point[0]
            point_tmp.y = point[1]
            point_tmp.z = point[2]

            pose_ref = Pose()
            pose_ref.position = deepcopy(point_tmp)
            q = transformations.quaternion_about_axis(radians(point[3]), zaxis)
            pose_ref.orientation.x = q[0]
            pose_ref.orientation.y = q[1]
            pose_ref.orientation.z = q[2]
            pose_ref.orientation.w = q[3]
                        
            points_r.points.append(point_tmp)
            lines_r.points.append(point_tmp)
            poses_array.poses.append(pose_ref)
            
            marker_points_pub.publish(points_r)
            marker_lines_pub.publish(lines_r)
            pose_pub.publish(poses_array)
            
            if len(lines_r.points) == max_num:
                tmp_points = []
                for count, line_p in enumerate(lines_r.points):                    
                    if count > 0:
                        tmp_points.append(line_p)
                lines_r.points = []
                for d in tmp_points:
                    lines_r.points.append(d)
            ind += 1
            rospy.sleep(1.)
        rospy.sleep(1.)


if __name__ == "__main__":
    main()
    rospy.spin()
