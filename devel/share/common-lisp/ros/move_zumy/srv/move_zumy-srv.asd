
(cl:in-package :asdf)

(defsystem "move_zumy-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
)
  :components ((:file "_package")
    (:file "Mov2LocSrv" :depends-on ("_package_Mov2LocSrv"))
    (:file "_package_Mov2LocSrv" :depends-on ("_package"))
  ))