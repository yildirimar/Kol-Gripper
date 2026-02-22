# Assembly Robot Description - ROS2 Package

Bu paket, Assembly robot için URDF/xacro dosyalarını içeren bir ROS2 description paketidir. Joint State Publisher GUI ve RViz2 ile robotun görselleştirilmesini ve Gazebo simülasyonunu sağlar.

## 🚀 Hızlı Başlangıç

```bash
# Workspace'e git
cd ~/Desktop/Assembly_description

# Paketi build et
colcon build --packages-select Assembly_description

# Environment'ı source et
source install/setup.bash

# RViz2 + Joint State Publisher GUI ile launch et
ros2 launch Assembly_description display.launch.py

# VEYA Gazebo simülasyonu ile launch et
ros2 launch Assembly_description gazebo.launch.py
```

---

## 📁 Paket Yapısı

```
Assembly_description/
├── build/                    # Build dosyaları (colcon tarafından oluşturulur)
├── install/                  # Install dosyaları (colcon tarafından oluşturulur)
├── log/                      # Log dosyaları
└── src/                      # Kaynak dosyalar
    ├── CMakeLists.txt        # ROS2 ament_cmake build dosyası
    ├── package.xml           # ROS2 paket manifest dosyası
    ├── launch/
    │   ├── display.launch.py # ROS2 Python launch dosyası
    │   └── urdf.rviz         # ROS2 RViz2 config dosyası
    ├── urdf/
    │   ├── Assembly.xacro    # Robot URDF modeli (xacro)
    │   ├── Assembly.trans    # Transmission dosyası
    │   ├── Assembly.gazebo   # Gazebo eklentileri
    │   └── materials.xacro   # Malzeme tanımları
    └── meshes/               # STL mesh dosyaları
```

---

## 🔄 ROS1'den ROS2'ye Dönüşüm Rehberi

Eğer bir ROS1 description paketiniz varsa ve ROS2'ye dönüştürmek istiyorsanız, aşağıdaki adımları izleyin:

### 1. `package.xml` Güncellemesi

**ROS1 (catkin) formatından:**
```xml
<?xml version="1.0"?>
<package format="2">
  <name>Assembly_description</name>
  <buildtool_depend>catkin</buildtool_depend>
  <build_depend>rospy</build_depend>
  ...
</package>
```

**ROS2 (ament) formatına:**
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>Assembly_description</name>
  <version>0.0.1</version>
  <description>ROS2 description package for Assembly robot</description>
  <maintainer email="mehmetalihawk@email.com">Mehmet Ali Şahin</maintainer>
  <license>MIT</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>xacro</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>launch</exec_depend>
  <exec_depend>launch_ros</exec_depend>
  <exec_depend>urdf</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### 2. `CMakeLists.txt` Güncellemesi

**ROS1 (catkin) formatından:**
```cmake
cmake_minimum_required(VERSION 2.8.3)
project(Assembly_description)
find_package(catkin REQUIRED COMPONENTS rospy)
catkin_package()
```

**ROS2 (ament_cmake) formatına:**
```cmake
cmake_minimum_required(VERSION 3.8)
project(Assembly_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)

install(DIRECTORY
  launch
  urdf
  meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

### 3. Launch Dosyası Dönüşümü

**ROS1 XML launch dosyası (`display.launch`):**
```xml
<launch>
  <arg name="model" default="$(find Assembly_description)/urdf/Assembly.xacro"/>
  <param name="robot_description" command="$(find xacro)/xacro $(arg model)"/>
  <node name="joint_state_publisher_gui" pkg="joint_state_publisher_gui" type="joint_state_publisher_gui"/>
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(arg rvizconfig)"/>
</launch>
```

**ROS2 Python launch dosyası (`display.launch.py`):**
```python
#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('Assembly_description')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'Assembly.xacro')
    rviz_config = os.path.join(pkg_dir, 'launch', 'urdf.rviz')
    
    robot_description = Command(['xacro ', urdf_file])
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config]
        )
    ])
```

### 4. RViz Config Dosyası Güncellemesi

ROS1 RViz ve ROS2 RViz2 farklı plugin namespace'leri kullanır:

| ROS1 (rviz)        | ROS2 (rviz2)                    |
|--------------------|----------------------------------|
| `rviz/Grid`        | `rviz_default_plugins/Grid`     |
| `rviz/RobotModel`  | `rviz_default_plugins/RobotModel`|
| `rviz/TF`          | `rviz_default_plugins/TF`       |
| `rviz/Orbit`       | `rviz_default_plugins/Orbit`    |
| `rviz/MoveCamera`  | `rviz_default_plugins/MoveCamera`|
| `rviz/Interact`    | `rviz_default_plugins/Interact` |
| ...                | ...                              |

**Tüm `rviz/` prefix'lerini `rviz_default_plugins/` ile değiştirin.**

### 5. URDF/Xacro Dosyaları

URDF dosyaları genellikle değişiklik gerektirmez. Ancak xacro include ifadeleri için:

```xml
<!-- Bu sözdizimi hem ROS1 hem ROS2'de çalışır -->
<xacro:property name="package_path" value="$(find Assembly_description)" />
<xacro:include filename="${package_path}/urdf/materials.xacro" />
```

---

## 📦 Gerekli Paketler

ROS2 sisteminizde aşağıdaki paketlerin kurulu olduğundan emin olun:

```bash
sudo apt update
sudo apt install ros-${ROS_DISTRO}-robot-state-publisher \
                 ros-${ROS_DISTRO}-joint-state-publisher \
                 ros-${ROS_DISTRO}-joint-state-publisher-gui \
                 ros-${ROS_DISTRO}-xacro \
                 ros-${ROS_DISTRO}-rviz2
```

---

## 🤖 Robot Jointleri

Bu robot 5 revolute joint içermektedir:

| Joint Adı      | Tip        | Parent Link | Child Link |
|----------------|------------|-------------|------------|
| Revolute 20    | continuous | base_link   | link1_1    |
| Revolute 21    | continuous | link1_1     | link2_1    |
| Revolute 22    | continuous | link2_1     | link3_1    |
| Revolute 23    | continuous | link3_1     | link4_1    |
| Revolute 24    | continuous | link4_1     | link5_1    |

---

## 🛠️ Sorun Giderme

### "Unknown substitution: find" Hatası
- Eski ROS1 `.launch` dosyasını değil, yeni `.launch.py` dosyasını kullandığınızdan emin olun
- Doğru komut: `ros2 launch Assembly_description display.launch.py`

### RViz2 Plugin Hataları
- `urdf.rviz` dosyasının ROS2 formatında olduğundan emin olun
- Tüm `rviz/` prefix'leri `rviz_default_plugins/` olmalı

### Robot Görünmüyor
1. Fixed Frame'in `base_link` olarak ayarlandığını kontrol edin
2. RobotModel display'in aktif olduğunu kontrol edin
3. `/robot_description` topic'inin yayınlandığını kontrol edin:
   ```bash
   ros2 topic echo /robot_description --once
   ```

---

## 📝 Lisans

MIT License

---

## 🎮 Gazebo Simülasyonu

### Gazebo'da Robotu Spawn Etme

```bash
# Gazebo simülasyonunu başlat
ros2 launch Assembly_description gazebo.launch.py

# Özel spawn pozisyonu ile başlat
ros2 launch Assembly_description gazebo.launch.py x_pose:=1.0 y_pose:=0.5 z_pose:=0.5
```

### Gazebo Launch Parametreleri

| Parametre     | Varsayılan | Açıklama                        |
|---------------|------------|----------------------------------|
| `use_sim_time`| `true`     | Gazebo simülasyon saatini kullan|
| `x_pose`      | `0.0`      | Spawn X pozisyonu               |
| `y_pose`      | `0.0`      | Spawn Y pozisyonu               |
| `z_pose`      | `0.5`      | Spawn Z pozisyonu               |

---

## 🔄 ROS1'den ROS2'ye Gazebo Dönüşümü

### 1. Gazebo Plugin Güncellemesi

**ROS1 Gazebo plugin (`Assembly.gazebo`):**
```xml
<gazebo>
  <plugin name="control" filename="libgazebo_ros_control.so"/>
</gazebo>
```

**ROS2 Gazebo plugin:**
```xml
<gazebo>
  <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
    <robot_param>robot_description</robot_param>
    <robot_param_node>robot_state_publisher</robot_param_node>
  </plugin>
</gazebo>

<!-- Joint State Publisher Plugin -->
<gazebo>
  <plugin name="gazebo_ros_joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <update_rate>50</update_rate>
    <joint_name>Revolute 20</joint_name>
    <joint_name>Revolute 21</joint_name>
    <!-- ... diğer jointler -->
  </plugin>
</gazebo>
```

### 2. Gazebo Launch Dosyası Dönüşümü

**ROS1 XML launch dosyası (`gazebo.launch`):**
```xml
<launch>
  <include file="$(find gazebo_ros)/launch/empty_world.launch"/>
  <param name="robot_description" command="$(find xacro)/xacro $(arg model)"/>
  <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" 
        args="-param robot_description -urdf -model assembly"/>
</launch>
```

**ROS2 Python launch dosyası (`gazebo.launch.py`):**
```python
#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('Assembly_description')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'Assembly.xacro')
    
    robot_description = Command(['xacro ', urdf_file])
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )
    
    # Gazebo Server
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 
                         'launch', 'gzserver.launch.py')
        ])
    )
    
    # Gazebo Client
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 
                         'launch', 'gzclient.launch.py')
        ])
    )
    
    # Spawn Entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'assembly_robot',
            '-x', '0.0', '-y', '0.0', '-z', '0.5'
        ]
    )
    
    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        spawn_entity
    ])
```

### 3. package.xml'e Gazebo Bağımlılığı Ekleme

```xml
<exec_depend>gazebo_ros</exec_depend>
```

---

## 📦 Gazebo İçin Gerekli Paketler

```bash
sudo apt update
sudo apt install ros-${ROS_DISTRO}-gazebo-ros \
                 ros-${ROS_DISTRO}-gazebo-ros2-control \
                 ros-${ROS_DISTRO}-gazebo-plugins
```

---

## 🛠️ Gazebo Sorun Giderme

### Robot Gazebo'da Görünmüyor
1. `/robot_description` topic'inin yayınlandığını kontrol edin:
   ```bash
   ros2 topic echo /robot_description --once
   ```
2. Spawn entity log'larını kontrol edin
3. Mesh dosyalarının doğru yolda olduğunu doğrulayın

### Robot Düşüyor veya Sallanıyor
- `z_pose` değerini artırarak robotu zemin seviyesinin üstüne spawn edin
- Inertia değerlerinin doğru olduğundan emin olun

### "Service not available" Hatası
- Gazebo'nun tamamen başladığından emin olun
- `gazebo_ros` paketinin kurulu olduğunu kontrol edin
