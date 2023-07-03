#
#    @@@@@@@@@@@@@@@@@@@@
#    @@@@@@@@@&@@@&&@@@@@
#    @@@@@ @@  @@    @@@@
#    @@@@@ @@  @@    @@@@
#    @@@@@ @@  @@    @@@@ Copyright (c) 2023, Acceleration Robotics®
#    @@@@@ @@  @@    @@@@ Author: Víctor Mayoral Vilches <victor@accelerationrobotics.com>
#    @@@@@ @@  @@    @@@@ Author: Martiño Crespo <martinho@accelerationrobotics.com>
#    @@@@@ @@  @@    @@@@ Author: Alejandra Martínez Fariña <alex@accelerationrobotics.com>
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
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition

import sys
import argparse
import json

def main(argv):
    
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--hardware_device_type', type=str, help='Hardware Device Type (e.g. cpu or fpga)', default ='cpu')
    parser.add_argument('--trace_path', type=str, help='Path to trace files (e.g. /tmp/analysis/trace)', default = '/tmp/analysis/trace')
    parser.add_argument('--metrics', type=str, help='List of metrics to be analyzed (e.g. latency and/or throughput)', default = ['latency'])
    parser.add_argument('--integrated', type=str, help='Integrated or separated version of the Resize and Rectify nodes (only for fpga now)', default='false') 
    args = parser.parse_args(argv)

    # Get the values of the arguments
    hardware_device_type = args.hardware_device_type
    trace_path = args.trace_path
    metrics_string = args.metrics
    metrics_elements = [element.strip() for element in metrics_string.strip("[]").split(",")]
    metrics = json.loads(json.dumps(metrics_elements))
    integrated = args.integrated

    # Instantiate the class
    ba = BenchmarkAnalyzer('a1_perception_2nodes', hardware_device_type)

    if hardware_device_type == 'cpu':
        # add parameters for analyzing the traces
        ## using message header id
        target_chain = [
            "robotperf_benchmarks:robotperf_image_input_cb_init",  # 0
            "robotperf_benchmarks:robotperf_image_input_cb_fini",  # 1
            "robotperf_benchmarks:robotperf_image_output_cb_init",  # 10
            "robotperf_benchmarks:robotperf_image_output_cb_fini",  # 11
        ]

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

    elif hardware_device_type == "fpga":
        if integrated == 'false':
            target_chain = [
                "ros2:callback_start",  # 0
                "robotperf_benchmarks:robotperf_image_input_cb_init",  # 1
                "robotperf_benchmarks:robotperf_image_input_cb_fini",  # 2
                "ros2:callback_end",  # 3
                "ros2:callback_start",  # 4
                "ros2_image_pipeline:image_proc_rectify_cb_init",  # 5
                "ros2_image_pipeline:image_proc_rectify_init",  # 6
                "ros2:vitis_profiler:kernel_enqueue",  # 7
                "ros2:vitis_profiler:kernel_enqueue",  # 8
                "ros2_image_pipeline:image_proc_rectify_fini",  # 9
                # "ros2:rclcpp_publish",
                # "ros2:rcl_publish",
                # "ros2:rmw_publish",
                "ros2_image_pipeline:image_proc_rectify_cb_fini",  # 10
                "ros2:callback_end",  # 11
                "ros2:callback_start",  # 12
                "ros2_image_pipeline:image_proc_resize_cb_init",  # 13
                "ros2_image_pipeline:image_proc_resize_init",  # 14
                "ros2:vitis_profiler:kernel_enqueue",  # 15
                "ros2:vitis_profiler:kernel_enqueue",  # 16
                "ros2_image_pipeline:image_proc_resize_fini",  # 17
                # "ros2:rclcpp_publish",
                # "ros2:rcl_publish",
                # "ros2:rmw_publish",
                "ros2_image_pipeline:image_proc_resize_cb_fini",  # 18
                "ros2:callback_end",  # 19
                "ros2:callback_start",  # 20
                "robotperf_benchmarks:robotperf_image_output_cb_init",  # 21
                "robotperf_benchmarks:robotperf_image_output_cb_fini",  # 22
                "ros2:callback_end",  # 23
            ]

            # add parameters for analyzing the traces
            ba.add_target(
                {
                    "name": "ros2:callback_start",
                    "name_disambiguous": "ros2:callback_start",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "lightgray",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "robotperf_benchmarks:robotperf_image_input_cb_init",
                    "name_disambiguous":
                        "robotperf_benchmarks:robotperf_image_input_cb_init",
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
            ba.add_target(
                {
                    "name": "ros2:callback_end",
                    "name_disambiguous": "ros2:callback_end",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "gray",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:callback_start",
                    "name_disambiguous": "ros2:callback_start (2)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "lightsalmon",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_cb_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_cb_init",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "salmon",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_init",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "darksalmon",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )

            ba.add_target(
                {
                    "name": "ros2:vitis_profiler:kernel_enqueue",
                    "name_disambiguous": "ros2:kernel_enqueue:rectify_init",
                    "colors_fg": "green",
                    "colors_fg_bokeh": "indianred",
                    "layer": "kernel",
                    "label_layer": 1,
                    "marker": "plus",
                }
            )

            ba.add_target(
                {
                    "name": "ros2:vitis_profiler:kernel_enqueue",
                    "name_disambiguous": "ros2:kernel_enqueue:rectify_fini",
                    "colors_fg": "green",
                    "colors_fg_bokeh": "crimson",
                    "layer": "kernel",
                    "label_layer": 1,
                    "marker": "plus",
                }
            )

            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_fini",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "lightcoral",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_cb_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_cb_fini",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "darkred",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:callback_end",
                    "name_disambiguous": "ros2:callback_end (2)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "red",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:callback_start",
                    "name_disambiguous": "ros2:callback_start (3)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "lavender",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_resize_cb_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_resize_cb_init",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "thistle",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_resize_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_resize_init",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "plum",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:vitis_profiler:kernel_enqueue",
                    "name_disambiguous": "ros2:kernel_enqueue:resize_init",
                    "colors_fg": "green",
                    "colors_fg_bokeh": "fuchsia",
                    "layer": "kernel",
                    "label_layer": 1,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:vitis_profiler:kernel_enqueue",
                    "name_disambiguous": "ros2:kernel_enqueue:resize_finit",
                    "colors_fg": "green",
                    "colors_fg_bokeh": "darkmagenta",
                    "layer": "kernel",
                    "label_layer": 1,
                    "marker": "plus"
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_resize_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_resize_fini",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "fuchsia",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_resize_cb_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_resize_cb_fini",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "indigo",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:callback_end",
                    "name_disambiguous": "ros2:callback_end (3)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "mediumslateblue",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
            ba.add_target(
                {
                    "name": "ros2:callback_start",
                    "name_disambiguous": "ros2:callback_start (4)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "chartreuse",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )
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
            ba.add_target(
                {
                    "name": "ros2:callback_end",
                    "name_disambiguous": "ros2:callback_end (4)",
                    "colors_fg": "blue",
                    "colors_fg_bokeh": "cornflowerblue",
                    "layer": "rclcpp",
                    "label_layer": 3,
                    "marker": "diamond",
                }
            )

        else: #integrated
            # add parameters for analyzing the traces
            ## using message header id
            target_chain = [
                "robotperf_benchmarks:robotperf_image_input_cb_init",  # 0
                "robotperf_benchmarks:robotperf_image_input_cb_fini",  # 1
                "ros2_image_pipeline:image_proc_rectify_cb_init",  # 2
                "ros2_image_pipeline:image_proc_rectify_init",  # 3
                "ros2_image_pipeline:image_proc_rectify_fini",  # 4
                "ros2_image_pipeline:image_proc_rectify_cb_fini",  # 5
                "robotperf_benchmarks:robotperf_image_output_cb_init",  # 6
                "robotperf_benchmarks:robotperf_image_output_cb_fini",  # 7
            ]

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
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_cb_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_cb_init",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "salmon",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_init",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_init",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "darksalmon",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_fini",
                    "colors_fg": "red",
                    "colors_fg_bokeh": "lightcoral",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
            ba.add_target(
                {
                    "name": "ros2_image_pipeline:image_proc_rectify_cb_fini",
                    "name_disambiguous": "ros2_image_pipeline:image_proc_rectify_cb_fini",
                    "colors_fg": "yellow",
                    "colors_fg_bokeh": "darkred",
                    "layer": "userland",
                    "label_layer": 4,
                    "marker": "plus",
                }
            )
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

    else:
        print('The hardware device type ' + hardware_device_type + ' is not yet implemented\n')
        
    num_metrics = 0 # initialize the metric count
    add_power = False # initialize the boolean
    for metric in metrics:
        if metric == 'power':
            add_power = True
            ba.add_power(
            {
                "name": "robotcore_power:robotcore_power_output_cb_fini",
                "name_disambiguous": "robotcore_power:robotcore_power_output_cb_fini",
                "colors_fg": "blue",
                "colors_fg_bokeh": "silver",
                "layer": "userland",
                "label_layer": 4,
                "marker": "plus",
            }
            )
        else:
            num_metrics += 1 # it will be larger than 0 if other metrics besides power are desired
    
    for metric in metrics:
        if metric == 'latency':
            ba.analyze_latency(trace_path, add_power)
        elif metric == 'throughput':
            ba.analyze_throughput(trace_path, add_power)
        elif metric == 'power': 
            if num_metrics == 0: # launch independently iff no other metric is requested
                total_consumption = ba.analyze_power(trace_path)
                print("The average consumption is {} W".format(total_consumption))
        else:
            print('The metric ' + metric + ' is not yet implemented\n')
    

def generate_launch_description():
    # Declare the launch arguments
    hardware_device_type_arg = DeclareLaunchArgument(
        'hardware_device_type',
        default_value='cpu',
        description='Hardware Device Type (e.g. cpu or fpga)'
    )

    trace_path_arg = DeclareLaunchArgument(
        'trace_path',
        default_value='/tmp/analysis/trace',
        description='Path to trace files (e.g. /tmp/analysis/trace)'
    )

    metrics_arg = DeclareLaunchArgument(
        'metrics',
        default_value=['latency'],
        description='List of metrics to be analyzed (e.g. latency and/or throughput)'
    )
    
    integrated_arg = DeclareLaunchArgument(
        'integrated',
        default_value="false",
        description='Integrated or separated version of the Resize and Rectify nodes (only for fpga now)'
    )

    # Create the launch description
    ld = LaunchDescription()
    
    # Define the ExecuteProcess action to run the Python script
    analyzer = ExecuteProcess(
        cmd=[
            'python3', "src/benchmarks/benchmarks/perception/a1_perception_2nodes/launch/analyze_a1_perception_2nodes.launch.py",
            '--hardware_device_type', LaunchConfiguration('hardware_device_type'),
            '--trace_path', LaunchConfiguration('trace_path'),
            '--metrics', LaunchConfiguration('metrics'),
            '--integrated', LaunchConfiguration('integrated')],
        output='screen'
    )

    # Add the declared launch arguments to the launch description
    ld.add_action(hardware_device_type_arg)
    ld.add_action(trace_path_arg)
    ld.add_action(metrics_arg)
    ld.add_action(integrated_arg)
    
    # Add the ExecuteProcess action to the launch description
    ld.add_action(analyzer)

    return ld

if __name__ == '__main__':
    main(sys.argv[1:])
    