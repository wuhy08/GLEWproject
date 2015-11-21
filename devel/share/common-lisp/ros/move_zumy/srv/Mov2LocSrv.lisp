; Auto-generated. Do not edit!


(cl:in-package move_zumy-srv)


;//! \htmlinclude Mov2LocSrv-request.msg.html

(cl:defclass <Mov2LocSrv-request> (roslisp-msg-protocol:ros-message)
  ((zumyID
    :reader zumyID
    :initarg :zumyID
    :type cl:string
    :initform "")
   (goal
    :reader goal
    :initarg :goal
    :type geometry_msgs-msg:Pose2D
    :initform (cl:make-instance 'geometry_msgs-msg:Pose2D)))
)

(cl:defclass Mov2LocSrv-request (<Mov2LocSrv-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Mov2LocSrv-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Mov2LocSrv-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name move_zumy-srv:<Mov2LocSrv-request> is deprecated: use move_zumy-srv:Mov2LocSrv-request instead.")))

(cl:ensure-generic-function 'zumyID-val :lambda-list '(m))
(cl:defmethod zumyID-val ((m <Mov2LocSrv-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_zumy-srv:zumyID-val is deprecated.  Use move_zumy-srv:zumyID instead.")
  (zumyID m))

(cl:ensure-generic-function 'goal-val :lambda-list '(m))
(cl:defmethod goal-val ((m <Mov2LocSrv-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_zumy-srv:goal-val is deprecated.  Use move_zumy-srv:goal instead.")
  (goal m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Mov2LocSrv-request>) ostream)
  "Serializes a message object of type '<Mov2LocSrv-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'zumyID))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'zumyID))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'goal) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Mov2LocSrv-request>) istream)
  "Deserializes a message object of type '<Mov2LocSrv-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'zumyID) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'zumyID) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'goal) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Mov2LocSrv-request>)))
  "Returns string type for a service object of type '<Mov2LocSrv-request>"
  "move_zumy/Mov2LocSrvRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Mov2LocSrv-request)))
  "Returns string type for a service object of type 'Mov2LocSrv-request"
  "move_zumy/Mov2LocSrvRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Mov2LocSrv-request>)))
  "Returns md5sum for a message object of type '<Mov2LocSrv-request>"
  "486d05b8548358882df27b5102476843")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Mov2LocSrv-request)))
  "Returns md5sum for a message object of type 'Mov2LocSrv-request"
  "486d05b8548358882df27b5102476843")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Mov2LocSrv-request>)))
  "Returns full string definition for message of type '<Mov2LocSrv-request>"
  (cl:format cl:nil "string zumyID~%geometry_msgs/Pose2D goal~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Mov2LocSrv-request)))
  "Returns full string definition for message of type 'Mov2LocSrv-request"
  (cl:format cl:nil "string zumyID~%geometry_msgs/Pose2D goal~%~%================================================================================~%MSG: geometry_msgs/Pose2D~%# This expresses a position and orientation on a 2D manifold.~%~%float64 x~%float64 y~%float64 theta~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Mov2LocSrv-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'zumyID))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'goal))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Mov2LocSrv-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Mov2LocSrv-request
    (cl:cons ':zumyID (zumyID msg))
    (cl:cons ':goal (goal msg))
))
;//! \htmlinclude Mov2LocSrv-response.msg.html

(cl:defclass <Mov2LocSrv-response> (roslisp-msg-protocol:ros-message)
  ((isPosReached
    :reader isPosReached
    :initarg :isPosReached
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Mov2LocSrv-response (<Mov2LocSrv-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Mov2LocSrv-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Mov2LocSrv-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name move_zumy-srv:<Mov2LocSrv-response> is deprecated: use move_zumy-srv:Mov2LocSrv-response instead.")))

(cl:ensure-generic-function 'isPosReached-val :lambda-list '(m))
(cl:defmethod isPosReached-val ((m <Mov2LocSrv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_zumy-srv:isPosReached-val is deprecated.  Use move_zumy-srv:isPosReached instead.")
  (isPosReached m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Mov2LocSrv-response>) ostream)
  "Serializes a message object of type '<Mov2LocSrv-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'isPosReached) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Mov2LocSrv-response>) istream)
  "Deserializes a message object of type '<Mov2LocSrv-response>"
    (cl:setf (cl:slot-value msg 'isPosReached) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Mov2LocSrv-response>)))
  "Returns string type for a service object of type '<Mov2LocSrv-response>"
  "move_zumy/Mov2LocSrvResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Mov2LocSrv-response)))
  "Returns string type for a service object of type 'Mov2LocSrv-response"
  "move_zumy/Mov2LocSrvResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Mov2LocSrv-response>)))
  "Returns md5sum for a message object of type '<Mov2LocSrv-response>"
  "486d05b8548358882df27b5102476843")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Mov2LocSrv-response)))
  "Returns md5sum for a message object of type 'Mov2LocSrv-response"
  "486d05b8548358882df27b5102476843")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Mov2LocSrv-response>)))
  "Returns full string definition for message of type '<Mov2LocSrv-response>"
  (cl:format cl:nil "bool isPosReached~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Mov2LocSrv-response)))
  "Returns full string definition for message of type 'Mov2LocSrv-response"
  (cl:format cl:nil "bool isPosReached~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Mov2LocSrv-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Mov2LocSrv-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Mov2LocSrv-response
    (cl:cons ':isPosReached (isPosReached msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Mov2LocSrv)))
  'Mov2LocSrv-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Mov2LocSrv)))
  'Mov2LocSrv-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Mov2LocSrv)))
  "Returns string type for a service object of type '<Mov2LocSrv>"
  "move_zumy/Mov2LocSrv")