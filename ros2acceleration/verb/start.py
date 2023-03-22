#    ____  ____
#   /   /\/   /
#  /___/  \  /   Copyright (c) 2021, Xilinx®.
#  \   \   \/    Author: Víctor Mayoral Vilches <victorma@xilinx.com>
#   \   \
#   /   /
#  /___/   /\
#  \   \  /  \
#   \___\/\___\
#
# Licensed under the Apache License, Version 2.0
#

import os

from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2acceleration.verb import VerbExtension, run, yellow
from ros2acceleration.api import get_package_names, get_prefix_path

DAEMON_BINARY_PATH = "/usr/bin/dfx-mgrd"


def regenerate_firmware():
    """
    This function regenerates in /lib/firmware/xilinx the
    firmware for ROS 2-packages.

    For each packge, if applicable, it generated a folder with
    its name that contains the kernel in xilinx binary format,
    the raw bitstream of the kernel and the device tree blob
    overlay.

    NOTE: this exists due to limitations in the current dfx-mgr
    implementation. Re-place with a different approach once
    dfx-mgr gets updatd.
    """
    for pkg_name in sorted(get_package_names()):
        if is_cpp_package(pkg_name):
            if contains_valid_kernel(pkg_name):
                destination_dir = "/lib/firmware/xilinx/" + pkg_name + "/"

                files_to_copy = []
                files_to_copy.append(get_path_ending(pkg_name, ".xclbin"))
                files_to_copy.append(get_path_ending(pkg_name, ".bit.bin"))
                files_to_copy.append(get_path_ending(pkg_name, ".dtbo"))
                files_to_copy.append(get_path_ending(pkg_name, ".json"))

                if not os.path.exists(destination_dir):
                    run("mkdir " + destination_dir, shell=True, timeout=1)

                for f in files_to_copy:
                    cmd = "cp " + f + " " + destination_dir
                    outs, errs = run(cmd, shell=True)


def get_path_ending(pkg_name, ending):
    """
    Gets the path of the file within a given ROS 2 package with @ending

    :param pkg_name (string)
    :param ending (string)
    :return bool
    """
    prefix = get_prefix_path(pkg_name)
    cpp_path = prefix + "/lib/" + pkg_name
    cmd = "ls " + cpp_path
    outs, errs = run(cmd, shell=True)
    pkg_artifacts = outs.split("\n")

    for artifact in pkg_artifacts:
        if artifact.endswith(ending):
            return cpp_path + "/" + artifact


def contains_valid_kernel(pkg_name):
    """
    Checks if pkg_name contains a valid acceleration kernel.

    Validity is checked against the dfx-mgr supported
    implementation. Currently, it requires a package to have:
    - a valid bitstream (.bit.bin)
    - a valid device tree blob overlay (.dtbo)
    - a valid xilinx binary kernel file (.xclbin)
    - a valid shell JSON file (.json)

    :param pkg_name (string)
    :return bool
    """
    has_xclbin = False
    has_bitbin = False
    has_dtbo = False
    has_json = False

    prefix = get_prefix_path(pkg_name)
    cpp_path = prefix + "/lib/" + pkg_name
    cmd = "ls " + cpp_path
    outs, errs = run(cmd, shell=True)
    if not outs:
        return False
    pkg_artifacts = outs.split("\n")

    for artifact in pkg_artifacts:
        if artifact.endswith(".xclbin"):
            has_xclbin = True
        if artifact.endswith(".bit.bin"):
            has_bitbin = True
        if artifact.endswith(".dtbo"):
            has_dtbo = True
        if artifact.endswith(".json"):
            has_json = True

    return has_xclbin and has_bitbin and has_dtbo and has_json


def is_cpp_package(pkg_name):
    """
    Checks if the pkg_name passed is a C++ ROS 2 package
    or not.

    NOTE: Only ROS 2 packages depending on rclcpp support hardware
    acceleration for now. Future extensions might allow
    to leverage also rclpy and/or other client libraries.

    :param pkg_name (string)
    :return bool
    """
    prefix = get_prefix_path(pkg_name)
    cpp_path = prefix + "/lib/" + pkg_name
    return os.path.exists(cpp_path)


def start_daemon():
    # cmd = DAEMON_BINARY_PATH + " 2> /dev/null > /dev/null &"  # less verbose
    cmd = DAEMON_BINARY_PATH + " 2> /dev/null  &"
    pid = os.fork()
    if pid == 0:  # new process
        os.system(cmd)
        exit()


class StartVerb(VerbExtension):
    """
    Start the ROS 2 acceleration daemon.

    Allows to monitor and interact with acceleration kernels.
    """

    def main(self, *, args):
        regenerate_firmware()
        start_daemon()
