# Transferable notebook work

This project provides a way to manage transfering notebook works across data scientists in a way that is reproducible and easy to work with.

It includes:

1. A Dockerfile to build the jupyter lab image with dependencies

2. A Json file storing workspace configuration

3. A control script

The dockerfile enables building an image which includes all the dependencies for the project as they are reflected in dev_requirements.txt. This image is subsequently used to launch and run a jupyterlab server that mounts a directory specified in the configuration file from the host inside the container and exposes in the jupyterlab server.

The script can be used to commit the container with the name specified in the json configuration file (transfer-control.json). Then start the container , or stop, or even purge the container to start anew. Finally the container can be commited and pushed with a copy of the workspace in repository specified in the confgiuration file. The configuration file is a json. 

# Dev-notes

This was created with the help of GPT4 with the initial prompt:

```

Build a python script that reads a configuration file name "transfer-control.py" or otherwise specified via command line argument. The script has a build argument that builds an image named as specified in the configuration file. The script has a start argument that starts the a container with name as specified in the configuration file for the image specified in the configuration file. During start of the container a volume is mounted for a directory as specified in the configuration file. The script has a commit argument that permits to commit the container as an image and push to a configuration specified docker repository. There is also the argument for the script to save the running container with the same parameters as in the commit but also having copied before the contents of the mounted volume in the container in the '/archive' directory. Please generate the python script for the provided below json configuration file:

{
    "container": {
        "name": "transfer-default-notebook"

    },

    "image" : {
        "name" : "transfer-defaul-image"
    },

    "volume": {
        "mount-point" : "/tf",
        "host-directory" : "."
    },

    "commit": {
        "name": "bare-notebook-latest",
        "repo": "nvcr.io"
    },

}

```
