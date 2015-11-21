# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "move_zumy: 0 messages, 1 services")

set(MSG_I_FLAGS "-Igeometry_msgs:/opt/ros/indigo/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/indigo/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(move_zumy_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv" NAME_WE)
add_custom_target(_move_zumy_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "move_zumy" "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv" "geometry_msgs/Pose2D"
)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(move_zumy
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/move_zumy
)

### Generating Module File
_generate_module_cpp(move_zumy
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/move_zumy
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(move_zumy_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(move_zumy_generate_messages move_zumy_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv" NAME_WE)
add_dependencies(move_zumy_generate_messages_cpp _move_zumy_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(move_zumy_gencpp)
add_dependencies(move_zumy_gencpp move_zumy_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS move_zumy_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(move_zumy
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/move_zumy
)

### Generating Module File
_generate_module_lisp(move_zumy
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/move_zumy
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(move_zumy_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(move_zumy_generate_messages move_zumy_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv" NAME_WE)
add_dependencies(move_zumy_generate_messages_lisp _move_zumy_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(move_zumy_genlisp)
add_dependencies(move_zumy_genlisp move_zumy_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS move_zumy_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(move_zumy
  "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/indigo/share/geometry_msgs/cmake/../msg/Pose2D.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/move_zumy
)

### Generating Module File
_generate_module_py(move_zumy
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/move_zumy
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(move_zumy_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(move_zumy_generate_messages move_zumy_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/cc/ee106a/fa15/class/ee106a-cn/ros_workspaces/project/src/move_zumy/srv/Mov2LocSrv.srv" NAME_WE)
add_dependencies(move_zumy_generate_messages_py _move_zumy_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(move_zumy_genpy)
add_dependencies(move_zumy_genpy move_zumy_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS move_zumy_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/move_zumy)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/move_zumy
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(move_zumy_generate_messages_cpp geometry_msgs_generate_messages_cpp)
add_dependencies(move_zumy_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/move_zumy)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/move_zumy
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(move_zumy_generate_messages_lisp geometry_msgs_generate_messages_lisp)
add_dependencies(move_zumy_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/move_zumy)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/move_zumy\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/move_zumy
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(move_zumy_generate_messages_py geometry_msgs_generate_messages_py)
add_dependencies(move_zumy_generate_messages_py std_msgs_generate_messages_py)
