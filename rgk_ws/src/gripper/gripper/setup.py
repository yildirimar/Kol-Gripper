import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'gripper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'rk_demo'), glob('gripper/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.rviz')),        
    ],




    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arifey',
    maintainer_email='yildirimar25@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gui = gripper.gui:main',
            'arm_ui = gripper.arm_ui:main',
            'fk_node = gripper.fk_node:main',
            'ik_node = gripper.ik_node:main'
        ],
    },
)
