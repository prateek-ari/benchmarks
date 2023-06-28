#
#    @@@@@@@@@@@@@@@@@@@@
#    @@@@@@@@@&@@@&&@@@@@
#    @@@@@ @@  @@    @@@@
#    @@@@@ @@  @@    @@@@
#    @@@@@ @@  @@    @@@@ Copyright (c) 2023, Acceleration Robotics®
#    @@@@@ @@  @@    @@@@ Author: Víctor Mayoral Vilches <victor@accelerationrobotics.com>
#    @@@@@ @@  @@    @@@@ Author: Martiño Crespo <martinho@accelerationrobotics.com>
#    @@@@@ @@  @@    @@@@
#    @@@@@@@@@&@@@@@@@@@@
#    @@@@@@@@@@@@@@@@@@@@
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from benchmark_utilities.analysis import BenchmarkAnalyzer
from launch import LaunchDescription


def generate_launch_description():
    return LaunchDescription()


ba = BenchmarkAnalyzer("a5_resize")

# # add parameters for analyzing the traces
# ba.add_target(
#     {
#         "name": "ros2:callback_start",
#         "name_disambiguous": "ros2:callback_start",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "lightgray",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )
ba.add_target(
    {
        "name": "robotperf_benchmarks:robotperf_image_input_cb_init",
        "name_disambiguous": "robotperf_benchmarks:robotperf_image_input_cb_init",
        "colors_fg": "blue",
        "colors_fg_bokeh": "silver",
        "layer": "userland",
        "label_layer": 4,
        "marker": "plus",
    }
)
ba.add_target(
    {
        "name": "robotperf_benchmarks:robotperf_image_input_cb_fini",
        "name_disambiguous": "robotperf_benchmarks:robotperf_image_input_cb_fini",
        "colors_fg": "blue",
        "colors_fg_bokeh": "darkgray",
        "layer": "benchmark",
        "label_layer": 5,
        "marker": "plus",
    }
)
# ba.add_target(
#     {
#         "name": "ros2:callback_end",
#         "name_disambiguous": "ros2:callback_end",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "gray",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )
# ba.add_target(
#     {
#         "name": "ros2:callback_start",
#         "name_disambiguous": "ros2:callback_start (2)",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "lavender",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )
# ba.add_target(
#     {
#         "name": "ros2:callback_end",
#         "name_disambiguous": "ros2:callback_end (2)",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "mediumslateblue",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )
# ba.add_target(
#     {
#         "name": "ros2:callback_start",
#         "name_disambiguous": "ros2:callback_start (3)",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "chartreuse",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )
ba.add_target(
    {
        "name": "robotperf_benchmarks:robotperf_image_output_cb_init",
        "name_disambiguous": "robotperf_benchmarks:robotperf_image_output_cb_init",
        "colors_fg": "blue",
        "colors_fg_bokeh": "chocolate",
        "layer": "benchmark",
        "label_layer": 5,
        "marker": "plus",
    }
)
ba.add_target(
    {
        "name": "robotperf_benchmarks:robotperf_image_output_cb_fini",
        "name_disambiguous": "robotperf_benchmarks:robotperf_image_output_cb_fini",
        "colors_fg": "blue",
        "colors_fg_bokeh": "coral",
        "layer": "userland",
        "label_layer": 4,
        "marker": "plus",
    }
)
# ba.add_target(
#     {
#         "name": "ros2:callback_end",
#         "name_disambiguous": "ros2:callback_end (3)",
#         "colors_fg": "blue",
#         "colors_fg_bokeh": "cornflowerblue",
#         "layer": "rclcpp",
#         "label_layer": 3,
#         "marker": "diamond",
#     }
# )

ba.analyze_latency()