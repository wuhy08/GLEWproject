# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build

# Utility rule file for run_tests_main_roslaunch-check_launch.

# Include the progress variables for this target.
include main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/progress.make

main/CMakeFiles/run_tests_main_roslaunch-check_launch:
	cd /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/main && ../catkin_generated/env_cached.sh /usr/bin/python /opt/ros/indigo/share/catkin/cmake/test/run_tests.py /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/test_results/main/roslaunch-check_launch.xml /usr/bin/cmake\ -E\ make_directory\ /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/test_results/main /opt/ros/indigo/share/roslaunch/cmake/../scripts/roslaunch-check\ -o\ '/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/test_results/main/roslaunch-check_launch.xml'\ '/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/main/launch'\ 

run_tests_main_roslaunch-check_launch: main/CMakeFiles/run_tests_main_roslaunch-check_launch
run_tests_main_roslaunch-check_launch: main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/build.make
.PHONY : run_tests_main_roslaunch-check_launch

# Rule to build all files generated by this target.
main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/build: run_tests_main_roslaunch-check_launch
.PHONY : main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/build

main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/clean:
	cd /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/main && $(CMAKE_COMMAND) -P CMakeFiles/run_tests_main_roslaunch-check_launch.dir/cmake_clean.cmake
.PHONY : main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/clean

main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/depend:
	cd /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/main /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/main /home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/build/main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : main/CMakeFiles/run_tests_main_roslaunch-check_launch.dir/depend

