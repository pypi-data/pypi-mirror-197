import os
from pathlib import Path
from skeletal_animation.utils.loader import load_fbx, serialize

SERIALIZED_ANIMATION_PATH = Path("path/to/serialized/animations")
FBX_ANIMATION_PATH = Path("path/to/fbx/animations")

# Load the fbx file
fbx_file = "death.fbx"
# Replace default path with the path of the fbx file
walk_animator = load_fbx(
    # "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/fbx/walk.fbx"
    os.path.join(FBX_ANIMATION_PATH, fbx_file)
)

serialized_file = "".join(fbx_file.split(".")[:-1])
# Replace default path with the path where you want to save the serialized animation
serialize(
    walk_animator,
    # "demo_hello_world",
    serialized_file,
    SERIALIZED_ANIMATION_PATH,
    # "C:/Users/christop.muller1/Desktop/",
    # "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/serialized/",
)
