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


def remove_dfx(kernel):
    if kernel:
        cmd = "dfx-mgr-client -remove " + kernel
    else:
        cmd = "dfx-mgr-client -remove"
    print(cmd)
    outs, errs = run(cmd, shell=True)
    if outs:
        print(outs)


class RemoveVerb(VerbExtension):
    """Remove the acceleration kernel."""

    def add_arguments(self, parser, cli_name):
        add_strategy_node_arguments(parser)
        parser.add_argument(
            "kernel", type=str, nargs="?",
            help="Kernel to remove.", default=None
        )

    def main(self, *, args):
        remove_dfx(args.kernel)
