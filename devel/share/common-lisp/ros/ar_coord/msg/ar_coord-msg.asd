
(cl:in-package :asdf)

(defsystem "ar_coord-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "ZumyCoord" :depends-on ("_package_ZumyCoord"))
    (:file "_package_ZumyCoord" :depends-on ("_package"))
  ))