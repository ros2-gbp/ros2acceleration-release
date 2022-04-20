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

from ctypes import *
from socket import *

from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2acceleration.verb import VerbExtension
from ros2acceleration.verb.start import start_daemon
from ros2acceleration.verb.stop import stop_daemon


class RestartVerb(VerbExtension):
    """Restart the ROS 2 acceleration daemon."""

    def main(self, *, args):
        stop_daemon()
        start_daemon()
