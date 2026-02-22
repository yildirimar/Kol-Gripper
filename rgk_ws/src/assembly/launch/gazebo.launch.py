#!/usr/bin/env python3
"""
ROS2 Launch file for spawning Assembly robot in Gazebo with ros2_control and RViz
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction, SetEnvironmentVariable, ExecuteProcess, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():
    # Get the package directory
    pkg_dir = get_package_share_directory('assembly')
    
    # Paths
    urdf_file = os.path.join(pkg_dir, 'urdf', 'Assembly.xacro')
    rviz_config_file = os.path.join(pkg_dir, 'launch', 'urdf.rviz')
    controllers_file = os.path.join(pkg_dir, 'config', 'controllers.yaml')
    
    # Set GAZEBO_MODEL_PATH so Gazebo can find meshes
    gazebo_model_path = os.path.join(pkg_dir, '..')
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    z_pose = LaunchConfiguration('z_pose')
    
    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock'
    )
    
    declare_x_pose = DeclareLaunchArgument(
        'x_pose',
        default_value='0.0',
        description='X position for robot spawn'
    )
    
    declare_y_pose = DeclareLaunchArgument(
        'y_pose',
        default_value='0.0',
        description='Y position for robot spawn'
    )
    
    declare_z_pose = DeclareLaunchArgument(
        'z_pose',
        default_value='0.1',
        description='Z position for robot spawn'
    )
    
    # Set environment variable for Gazebo to find meshes
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[gazebo_model_path, ':', os.environ.get('GAZEBO_MODEL_PATH', '')]
    )
    
    # Robot description from xacro
    robot_description = Command(['xacro ', urdf_file])
    
    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time
        }]
    )
    
    # Start Gazebo with empty world (includes ground plane)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={
            'verbose': 'true'
        }.items()
    )
    
    # Spawn robot in Gazebo (with delay to ensure Gazebo is ready)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'assembly_robot',
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose
        ]
    )
    
    # Spawn controllers after robot is spawned
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
    )
    
    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
        output='screen',
    )
    
    # Delay controller spawners until spawn_entity is done
    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )
    
    delay_joint_trajectory_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[joint_trajectory_controller_spawner],
        )
    )
    
    # RViz node (with delay to ensure everything is ready)
    rviz_node = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                arguments=['-d', rviz_config_file],
                parameters=[{'use_sim_time': use_sim_time}]
            )
        ]
    )
    
    # Delay spawn_entity to wait for Gazebo
    delay_spawn = TimerAction(
        period=5.0,
        actions=[spawn_entity]
    )
    
    return LaunchDescription([
        set_gazebo_model_path,
        declare_use_sim_time,
        declare_x_pose,
        declare_y_pose,
        declare_z_pose,
        robot_state_publisher_node,
        gazebo,
        delay_spawn,
        delay_joint_state_broadcaster,
        delay_joint_trajectory_controller,
        rviz_node
    ])
