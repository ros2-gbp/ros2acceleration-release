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

import sys
import os

from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2acceleration.verb import VerbExtension, run, red


DAEMON_BINARY_PATH = "/usr/bin/dfx-mgrd"
DAEMON_BINARY = "dfx-mgrd"

def stop_daemon():
    cmd = "ps -e| grep " + DAEMON_BINARY + " | awk '{print $1}'"
    pid, errs = run(cmd, shell=True)

    if not pid:
        red(DAEMON_BINARY + " not started")        
    else:
        # send the kill signal to stop the daemon
        os.kill(int(pid), 9)


class StopVerb(VerbExtension):
    """Stops the ROS 2 acceleration daemon."""

    def main(self, *, args):
        stop_daemon()




