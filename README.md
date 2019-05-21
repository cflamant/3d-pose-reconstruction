# 3D Human Pose Reconstruction from a 2D Monocular Image with Joint Ordering Uncertainty

Given a picture of a human and the approximate location of joints and their relative z-ordering (closeness to the camera), this script reconstructs an approximation of their 3D pose.

Please refer to the file [3D_Pose_Reconstruction.pdf](3D_Pose_Reconstruction.pdf) for an in-depth explanation of the code, as well as examples of it in action.

## Example
![breakdance ex](fig/mybreakdance.png)
![breakdance recons1](fig/mybreakdancerecons.png)
![breakdance recons1](fig/mybreakdancerecons2.png)

## Setup and Running the Code
Required packages:
* Pillow
* numpy
* scipy
* vpython

To run the script, in a terminal simply navigate to the `code/` directory and execute

```
$ python run.py
```
