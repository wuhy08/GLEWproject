# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "ar_coord: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iar_coord:/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(ar_coord_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg" NAME_WE)
add_custom_target(_ar_coord_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "ar_coord" "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg" "std_msgs/Time:geometry_msgs/Pose2D"
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(ar_coord
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/std_msgs/cmake/../msg/Time.msg;/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ar_coord
)

### Generating Services

### Generating Module File
_generate_module_cpp(ar_coord
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ar_coord
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(ar_coord_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(ar_coord_generate_messages ar_coord_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg" NAME_WE)
add_dependencies(ar_coord_generate_messages_cpp _ar_coord_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ar_coord_gencpp)
add_dependencies(ar_coord_gencpp ar_coord_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ar_coord_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(ar_coord
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/std_msgs/cmake/../msg/Time.msg;/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ar_coord
)

### Generating Services

### Generating Module File
_generate_module_lisp(ar_coord
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ar_coord
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(ar_coord_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(ar_coord_generate_messages ar_coord_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg" NAME_WE)
add_dependencies(ar_coord_generate_messages_lisp _ar_coord_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ar_coord_genlisp)
add_dependencies(ar_coord_genlisp ar_coord_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ar_coord_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(ar_coord
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/std_msgs/cmake/../msg/Time.msg;/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ar_coord
)

### Generating Services

### Generating Module File
_generate_module_py(ar_coord
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ar_coord
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(ar_coord_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(ar_coord_generate_messages ar_coord_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/ar_coord/msg/ZumyCoord.msg" NAME_WE)
add_dependencies(ar_coord_generate_messages_py _ar_coord_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(ar_coord_genpy)
add_dependencies(ar_coord_genpy ar_coord_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS ar_coord_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ar_coord)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/ar_coord
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(ar_coord_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(ar_coord_generate_messages_cpp geometry_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ar_coord)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/ar_coord
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(ar_coord_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(ar_coord_generate_messages_lisp geometry_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ar_coord)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ar_coord\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/ar_coord
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(ar_coord_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(ar_coord_generate_messages_py geometry_msgs_generate_messages_py)
