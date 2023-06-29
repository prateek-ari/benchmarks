# Copyright (C) Acceleration Robotics S.L.U. - All Rights Reserved
#
# Written by Víctor Mayoral-Vilches <victor@accelerationrobotics.com>
# Licensed under the Apache License, Version 2.0

import os
import subprocess
import sys
import yaml

from ros2cli.plugin_system import PLUGIN_SYSTEM_VERSION
from ros2cli.plugin_system import satisfies_version


def run(cmd, shell=False, timeout=1):
    """
    Spawns a new processe launching cmd, connect to their input/output/error pipes, and obtain their return codes.

    :param cmd: command split in the form of a list
    :returns: stdout
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
    try:
        outs, errs = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    # decode, or None
    if outs:
        outs = outs.decode("utf-8").strip()
    else:
        outs = None

    if errs:
        errs = errs.decode("utf-8").strip()
    else:
        errs = None
    return outs, errs
    

def black(text):
    print("\033[30m", text, "\033[0m", sep="")


def red(text):
    print("\033[31m", text, "\033[0m", sep="")


def redinline(text):
    print("\033[31m", text, "\033[0m", end="")


def green(text):
    print("\033[32m", text, "\033[0m", sep="")


def greeninline(text):
    print("\033[32m", text, "\033[0m", end='')


def yellow(text):
    print("\033[33m", text, "\033[0m", sep="")


def yellowinline(text):
    print("\033[33m", text, "\033[0m", end="")


def blue(text):
    print("\033[34m", text, "\033[0m", sep="")


def magenta(text):
    print("\033[35m", text, "\033[0m", sep="")


def cyan(text):
    print("\033[36m", text, "\033[0m", sep="")


def gray(text):
    print("\033[90m", text, "\033[0m", sep="")


def grayinline(text):
    print("\033[90m", text, "\033[0m", end="")


def search_benchmarks(filename="benchmark.yaml", searchpath="src"):
    """
    Returns a list with the paths of each benchmarks' benchmark.yaml
    """
    benchmark_paths = []
    for root, dirs, files in os.walk(searchpath):
        for file in files:
            if file == filename:
                benchmark_paths.append(os.path.join(root, file))    
    return benchmark_paths

def search_benchmarks_repo(searchpath="src"):
    """
    Returns path of the benchmarks repo
    """
    for root, dirs, files in os.walk(searchpath):
        if 'benchmarks' in dirs:
            return os.path.join(root, 'benchmarks')
    return None    



class VerbExtension:
    """
    The extension point for 'acceleration' verb extensions.

    The following properties must be defined:
    * `NAME` (will be set to the entry point name)

    The following methods must be defined:
    * `main`

    The following methods can be defined:
    * `add_arguments`
    """

    NAME = None
    EXTENSION_POINT_VERSION = '0.1'

    def __init__(self):
        super(VerbExtension, self).__init__()
        satisfies_version(PLUGIN_SYSTEM_VERSION, '^0.1')

    def add_arguments(self, parser, cli_name):
        pass

    def main(self, *, args):
        raise NotImplementedError()


class Benchmark:
    def __init__(self, yaml_file):
        with open(yaml_file, "r") as f:
            yaml_data = yaml.safe_load(f)
        if yaml_data is None:
            raise ValueError(f"Could not load data from {yaml_file}. Please check if file is empty or invalid.")

        self.id = yaml_data["id"]
        self.name = yaml_data["name"]
        self.description = yaml_data["description"]
        self.short = yaml_data["short"]
        self.graph = yaml_data["graph"]
        self.reproduction = yaml_data["reproduction"]
        self.results = []   # Ensure this line exists
        self.path = yaml_file.replace("/benchmark.yaml", "")

        for result in yaml_data["results"]:
            result_data = result["result"]
            metric = result_data.get("metric", "default_metric")
            metric_unit = result_data.get("metric_unit", "default_metric_unit")
            result_type = result_data.get("type", "default_type")
            hardware = result_data.get("hardware", "default_hardware")
            category = result_data.get("category", "default_category")
            timestampt = result_data.get("timestampt", "default_timestampt")
            value = result_data.get("value", "default_value")
            note = result_data.get("note", "default_note")
            datasource = result_data.get("datasource", "default_datasource")

            self.results.append({
                "metric": metric,
                "metric_unit": metric_unit,
                "type": result_type,  # "type" is a reserved keyword in Python, so we use "result_type"
                "hardware": hardware,
                "category": category,
                "timestampt": timestampt,
                "value": value,
                "note": note,
                "datasource": datasource
            })


    def __str__(self):
        yaml_data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short": self.short,
            "graph": self.graph,
            "reproduction": self.reproduction,
            "results": [{"result": result} for result in self.results]
        }

        key_order = ["id", "name", "description", "short", "graph", "reproduction", "results"]
        return yaml.dump(yaml_data, sort_keys=key_order)

    def markdown(self):
        """
        Markdown format for the class

        Meant for each benchmark's README.md file
        """
        # Header section
        md = f"# {self.name}\n\n"
        md += f"{self.short}\n\n"
        md += f"### ID\n{self.id}\n\n"
        md += f"### Description\n{self.description}\n\n"
        md += f"![]({self.graph})\n\n"

        # NOTE: metric and unit now living on each measurements
        # md += f"**Metric**: {self.metric['metric']} ({self.metric['unit']})\n\n"
        
        md += f"## Reproduction Steps\n\n```bash\n{self.reproduction}\n```\n\n"
        
        # Results section
        md += "## Results\n\n"
        md += "| Type | Hardware | Metric | Value | Category | Timestamp | Note | Data Source |\n"
        md += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"

        for result in self.results:
            if result['type'].lower() == "grey":
                aux_type = "[:white_circle:](https://github.com/robotperf/benchmarks/blob/main/benchmarks/README.md#type)"
            elif result['type'].lower() == "black":
                aux_type = "[:black_circle:](https://github.com/robotperf/benchmarks/blob/main/benchmarks/README.md#type)"
            else:
                aux_type = result['type']
            datasource = "[{}](https://github.com/robotperf/rosbags/tree/main/{})".format(result['datasource'], result['datasource'])

            md += f"| {aux_type} | {result['hardware']} | {result['metric']} | {result['value']} | {result['category']} | {result['timestampt']} | {result['note']} | {datasource} |\n"
        md += "\n"
        
        return md

    def markdown_general(self):
        """
        Markdown results (only), meant for general README.md file
        """        
        md = ""        
        
        benchmarks_repo_path = search_benchmarks_repo()
        # relative = self.path.replace("./" + benchmarks_repo_path, "")
        relative = self.path.replace("src/benchmarks/", "")
        relative_graph_path = "imgs" + self.graph.split("imgs")[1]

        for result in self.results:
            md += f"| [{self.id}](https://github.com/robotperf/benchmarks/tree/main/{relative}) | ![]({relative_graph_path}) | {self.short} | {result['metric']} ({result['metric_unit']}) | {result['hardware']} | {result['value']} | {result['category']} | {result['timestampt']} | {result['note']} | {result['datasource']} |\n"        
        return md