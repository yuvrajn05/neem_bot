from ament_index_python import get_package_share_directory
import launch
from launch import LaunchDescription
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
import launch_ros
from launch_ros.actions import Node
import os
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    world_path=os.path.join(get_package_share_directory('tortoisebot_gazebo'), 'worlds/room2.sdf'),
    
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Launch configuration variables specific to simulation
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    # Declare the launch arguments
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='0.0',
        description='Specify namespace of the robot')

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='Specify namespace of the robot')

    start_gazebo_ros_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'tortoisebot_simple',
            '-topic', 'robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'
        ],
        output='screen',
    )

    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    
    count=3
    x_val_pose = [0.0,-2.0,2.0]
    y_val_pose =[0.0,0.0,0.0]
    #x_val_pose = [-1.52139,-0.34,-0.65829,-5.32867]
    #y_val_pose = [13.8566,9.271,3.772,3.5]
    for i in range(count):
        robot_name = "robot_" + str(i+1)
        x_val = str(float(x_val_pose[i]))
        y_val = str(float(y_val_pose[i]))
        node = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', robot_name,
                '-topic', 'robot_description',
                '-x', x_val,
                '-y', y_val,  # Adjust the Y position as needed
                '-z', '0.01',
                '-robot_namespace', robot_name
            ],
            output='screen',
        )
        ld.add_action(TimerAction(period=0.1 + float(i * 2), actions=[node],))
    

    # Add any conditioned actions
    ld.add_action(start_gazebo_ros_spawner_cmd)

    return ld




    # # world_path= os.path.join(get_package_share_directory('ttb_description'), 'models/worlds/house_env.world'),
    # world_path=os.path.join(get_package_share_directory('tortoisebot_gazebo'), 'worlds/room2.sdf'),
    
    # use_sim_time = LaunchConfiguration('use_sim_time')

    # return launch.LaunchDescription([
    #     launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 
    #                                         'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',world_path], 
    #                                        output='screen'),
    #     launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
    #                             description='Flag to enable use_sim_time'),
    #     Node(
    #         package='gazebo_ros',
    #         executable='spawn_entity.py',
    #         arguments=['-entity', 'tortoisebot_simple', '-topic', 'robot_description', '-robot_namespace', 'robot1'],
    #         parameters= [{'use_sim_time': use_sim_time}],
    #         output='screen'),
    # ])
    