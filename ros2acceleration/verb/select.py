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

from ros2pkg.api import package_name_completer
from ros2cli.node.strategy import add_arguments as add_strategy_node_arguments
from ros2cli.node.strategy import NodeStrategy
from ros2acceleration.verb import VerbExtension, run
from ros2acceleration.verb.remove import remove_dfx


class SelectVerb(VerbExtension):
    """Select an acceleration kernel."""

    def add_arguments(self, parser, cli_name):
        add_strategy_node_arguments(parser)
        parser.add_argument("kernel", type=str, nargs=1, help="Kernel to select.")

    def main(self, *, args):
        remove_dfx(None)  # remove previous kernels, if loaded
        cmd = "dfx-mgr-client -load " + args.kernel[0]
        outs, errs = run(cmd, shell=True)
        if outs:
            print(outs)
