ssl-refbox-ros
==============

ROS node that publishes the referee's messages into a topic

Dependencies
============

* [Python 2.7](http://www.python.org/downloads/)
* [rospy](http://wiki.ros.org/ROS/Installation)
* [Google protocol-buffers compiler](http://code.google.com/p/protobuf/downloads/)

Usage
=====

Both the `msg/` and `scripts/` folders should be put inside your ROS package sources in a Catkin workspace:

    CATKIN_WORKSPACE/src/YOUR_PACKAGE/

Compile the `.proto` file to a Python class so it can be imported by the ROS node

    $ protoc -I=. --python_out=. referee.proto

Check the `catkin_python_setup()` line is uncommented, and add the `.msg` files to the `add_message_files` section in your package's `CMake.txt` file:

```
catkin_python_setup()

add_message_files(
   # Your other files
   team_info.msg
   referee.msg
 )
```

And make sure rospy is listed as a build and run dependency in your package's `package.xml` file:

```
<build_depend>rospy</build_depend>
<run_depend>rospy</run_depend>
```

After everything is setup, run `catkin_make` in your workspace's root folder
