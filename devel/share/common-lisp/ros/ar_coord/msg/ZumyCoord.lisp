; Auto-generated. Do not edit!


(cl:in-package ar_coord-msg)


;//! \htmlinclude ZumyCoord.msg.html

(cl:defclass <ZumyCoord> (roslisp-msg-protocol:ros-message)
  ((zumyID
    :reader zumyID
    :initarg :zumyID
    :type cl:string
    :initform "")
   (time
    :reader time
    :initarg :time
    :type std_msgs-msg:Time
    :initform (cl:make-instance 'std_msgs-msg:Time))
   (position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Pose2D
    :initform (cl:make-instance 'geometry_msgs-msg:Pose2D)))
)

(cl:defclass ZumyCoord (<ZumyCoord>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ZumyCoord>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ZumyCoord)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ar_coord-msg:<ZumyCoord> is deprecated: use ar_coord-msg:ZumyCoord instead.")))

(cl:ensure-generic-function 'zumyID-val :lambda-list '(m))
(cl:defmethod zumyID-val ((m <ZumyCoord>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ar_coord-msg:zumyID-val is deprecated.  Use ar_coord-msg:zumyID instead.")
  (zumyID m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <ZumyCoord>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ar_coord-msg:time-val is deprecated.  Use ar_coord-msg:time instead.")
  (time m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <ZumyCoord>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ar_coord-msg:position-val is deprecated.  Use ar_coord-msg:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ZumyCoord>) ostream)
  "Serializes a message object of type '<ZumyCoord>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'zumyID))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'zumyID))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'time) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ZumyCoord>) istream)
  "Deserializes a message object of type '<ZumyCoord>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'zumyID) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'zumyID) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'time) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ZumyCoord>)))
  "Returns string type for a message object of type '<ZumyCoord>"
  "ar_coord/ZumyCoord")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ZumyCoord)))
  "Returns string type for a message object of type 'ZumyCoord"
  "ar_coord/ZumyCoord")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ZumyCoord>)))
  "Returns md5sum for a message object of type '<ZumyCoord>"
  "100d2833b93ecf2b5920ca100a6fdaf8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ZumyCoord)))
  "Returns md5sum for a message object of type 'ZumyCoord"
  "100d2833b93ecf2b5920ca100a6fdaf8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ZumyCoord>)))
  "Returns full string definition for message of type '<ZumyCoord>"
  (cl:format cl:nil "string zumyID~%std_msgs/Time time~%geometry_msgs/Pose2D position~%~%~%================================================================================~%MSG: std_msgs/Time~%time data~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ZumyCoord)))
  "Returns full string definition for message of type 'ZumyCoord"
  (cl:format cl:nil "string zumyID~%std_msgs/Time time~%geometry_msgs/Pose2D position~%~%~%================================================================================~%MSG: std_msgs/Time~%time data~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ZumyCoord>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'zumyID))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'time))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ZumyCoord>))
  "Converts a ROS message object to a list"
  (cl:list 'ZumyCoord
    (cl:cons ':zumyID (zumyID msg))
    (cl:cons ':time (time msg))
    (cl:cons ':position (position msg))
))
