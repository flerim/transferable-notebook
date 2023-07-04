#!/usr/bin/env python

import argparse
import json
import os
import subprocess


def read_config_file(filename):
    with open(filename, "r") as f:
        config = json.load(f)
    return config


def build_image(config):
    image_name = config["image"]["name"]
    subprocess.run(
        ["docker", "build", "-f", "Dockerfile.work", "-t", image_name, "."])


def start_container(config):
    container_name = config["container"]["name"]
    image_name = config["image"]["name"]
    volume_mount_point = config["volume"]["mount-point"]
    host_directory = config["volume"]["host-directory"],
    portmaps = [
        f"{portnumber}:{portnumber}" for portnumber in config["ports"]["default"]]

    # Check if the container already exists
    container_exists = False
    result = subprocess.run(["docker", "ps", "-a", "--filter",
                             f"name={container_name}", "--format", "{{.Names}}"], capture_output=True, text=True)
    if container_name in result.stdout.strip().split('\n'):
        container_exists = True

    if container_exists:
        # Start the existing container
        subprocess.run(["docker", "start", "-a", container_name])
    else:
        # Create and start a new container
        run_list = ["docker", "run", "--name", container_name,
                    "-v", f"{host_directory[0]}:{volume_mount_point}"]

        for portmap in portmaps:
            run_list += ["-p", portmap]

        if "gpu" in config.keys():
            for ulimit in config["gpu"]["ulimit"]:
                run_list += ["--ulimit", ulimit]

            if "gpus" in config["gpu"].keys():
                run_list += ["--gpus", config["gpu"]["gpus"]]

        run_list += [image_name]

        print(run_list)
        subprocess.run(run_list)


def commit_container(config):
    container_name = config["container"]["name"]
    commit_name = config["commit"]["name"]
    repo = config["commit"]["repo"]
    subprocess.run(
        ["docker", "commit", container_name, f"{repo}/{commit_name}"])


def save_container(config):
    container_name = config["container"]["name"]
    commit_name = config["commit"]["name"]
    repo = config["commit"]["repo"]
    host_directory = config["volume"]["host-directory"]
    subprocess.run(
        ["docker", "cp", f"{host_directory}",
         f"{container_name}:/tf/archive/"])
    subprocess.run(
        ["docker", "commit", container_name, f"{repo}/{commit_name}"])


def push_container(config):
    commit_name = config["commit"]["name"]
    repo = config["container"]["repo"]
    subprocess.run(["docker", "push", f"{repo}/{commit_name}"])


def stop_container(config):
    container_name = config["container"]["name"]
    subprocess.run(["docker", "stop", container_name])


def delete_container(config):
    container_name = config["container"]["name"]

    stop_result = stop_container(config)
    if stop_result == 0:
        print(f"Stopped container {container_name}")
    else:
        print(f"Container {container_name} not running")

    subprocess.run(["docker", "rm", container_name])
    print(f"Deleted container {container_name}")


def main():
    parser = argparse.ArgumentParser(description="Transfer control script")
    parser.add_argument("config", nargs="?", default="config-transfer-control.json",
                        help="Configuration file (default: transfer-control.json)")
    parser.add_argument("--build", action="store_true", help="Build the image")
    parser.add_argument("--start", action="store_true",
                        help="Start the container")
    parser.add_argument("--commit", action="store_true",
                        help="Commit the container")
    parser.add_argument("--push", action="push_true",
                        help="Push the tagged image")
    parser.add_argument("--save", action="store_true",
                        help="Save the container")
    parser.add_argument("--stop", action="store_true",
                        help="Stop the container")
    parser.add_argument("--delete", action="store_true",
                        help="Delete the container")
    args = parser.parse_args()

    config = read_config_file(args.config)

    if args.build:
        build_image(config)
    elif args.start:
        start_container(config)
    elif args.commit:
        commit_container(config)
    elif args.save:
        save_container(config)
    elif args.push:
        push_container(config)
    elif args.stop:
        stop_container(config)
    elif args.delete:
        delete_container(config)


if __name__ == "__main__":
    main()
