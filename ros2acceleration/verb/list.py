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

from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2acceleration.verb import VerbExtension, run


class ListVerb(VerbExtension):
    """
    List available acceleration kernels.

    Uses the underlying dfx-mgr infrastructure.

    NOTE: future implementations should use modern versions
    of the dfx-mgr API and expose the acceleration kernels
    available directly to the complete ROS 2 tooling set
    (and/or the computational graph also if required through
    rclpy).

    NOTE 2: once directly pulling from the dfx-mgr API, reconsider
    start, stop and restart subverbs.
    """

    def main(self, *, args):
        cmd = "dfx-mgr-client -listPackage"
        # current implementation of dfx-mgr dumps
        # information in stdout of the daemon.
        #
        # NOTE: consider re-implementing this when
        # changing to the API approach.
        outs, errs = run(cmd, shell=True)
        if outs:
            print(3 * "\t" + outs)
