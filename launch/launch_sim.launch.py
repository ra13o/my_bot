import os
 
from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():


    # Include robot_state_publisher launch file. 
    # Force use_sim_time to be enabled
    # Set package name correctly. In this case my_bot as the package name

    package_name='my_bot' # <-- Change this Name

    # rsp = Robot State Publisher
    rsp =  IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )


    # Include the Gazebo Launch File, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
                )])
    )


    # Run the spawner node from gazebo_ros package.
    # Entity name does not really matter
    spawn_entity = Node(
        package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'my_bot'],
        output='screen'
    )



    # Launch them all
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])