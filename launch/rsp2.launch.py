import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import time
import xacro

def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('neem_bot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    # Create the robot_state_publisher nodes for both robots
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}

    # Robot 1 state publisher
    node_robot_state_publisher1 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='robot1',
        output='screen',
        parameters=[params]
    )

    # Robot 2 state publisher
    node_robot_state_publisher2 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='robot2',
        output='screen',
        parameters=[params]
    )

    # Include Gazebo launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'headless': 'false', 'verbose': 'true'}.items()  # Can adjust these parameters
    )

    # Spawn robot 1 at position (x=0, y=0, z=0)
    spawn_robot1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot1',
        arguments=[
            '-topic', 'robot1/robot_description',
            '-entity', 'robot1',
            '-x', '0',
            '-y', '0',
            '-z', '0',
            '-R', '0',
            '-P', '0',
            '-Y', '0',
        ],
        output='screen'
    )

    # Spawn robot 2 at position (x=2, y=2, z=0)
    spawn_robot2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_robot2',
        arguments=[
            '-topic', 'robot2/robot_description',
            '-entity', 'robot2',
            '-x', '2',
            '-y', '2',
            '-z', '0',
            '-R', '0',
            '-P', '0',
            '-Y', '0',
        ],
        output='screen'
    )

    # Introduce a delay to allow Gazebo to start properly
    wait_for_gazebo = LogInfo(
        msg="Waiting for Gazebo to start..."
    )

    # Launch all components
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        # Launch the robot state publisher nodes
        node_robot_state_publisher1,
        node_robot_state_publisher2,

        # Include Gazebo launch
        gazebo,

        # Add a wait to ensure Gazebo is ready before spawning entities
        wait_for_gazebo,

        # Spawn robots in Gazebo at different positions
        spawn_robot1,
        spawn_robot2
    ])
