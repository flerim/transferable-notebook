# Transferable notebook work

This project provides a way to manage datascience notebook hell so that data scientists can work across is a way that is easily reproducible.

It includes:

1. A Dockerfile to build the jupyter lab image with dependencies

2. A Json file storing workspace configuration

3. A control script `transferctl`

The entire operation consists of a few steps that can be performed via the control script. The user needs to only have defined the working directory where work is planned to be performed, e.g. notebooks, code, and data is going to reside. Modifying the example configuration file, building the image and launching the container. Then performing work from within the container using the notebook and finally saving the container to also include the workspace via the control script. Finally, the image can be pushed to a repository and published as needed. 

## Definition of workspace

One needs to define in the control configuration file ( customizable via the first positional argument of the control script ) the following parameters:

- The container name `{"container": {"name": "<value of container name>"}}` which is going to be used to name the container. One should take care to avoid overwriting currently running containers. 
- The image name `{"image" : {"name" : "<value of image name>"}}`
- The host-directory `{"volume":{"host-directory":"<location on host to mount>"}}` , this is where all the code, models, and data can be found

## Using the script

1. `transferctl --build` to build the image if it does not exist. It is advised to have a different for each workspace
2. `transferctl --start` to launch the container , then it can be accessed by clicking on the provided link

The options to stop and delete a container are provided also. 

Finally the user may decide to commit the container if there have been changes or to save and publish the container with `--save` and `--push` arguments.


## Dev-notes

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
