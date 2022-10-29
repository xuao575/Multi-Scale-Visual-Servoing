import numpy as np
import pyrealsense2 as rs
import cv2

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)


for x in range(25):
    frameset = pipeline.wait_for_frames()

print('realsense loaded')

# -----------------------------------------------


# def get_camera_k():
#     intr = profile.get_intrinsics()
#     return intr


def get_color_depth():
    # get frame with align
    frameset = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    frameset = align.process(frameset)

    # get color
    color_frame = frameset.get_color_frame()
    color = np.asanyarray(color_frame.get_data())

    # get depth
    aligned_depth_frame = frameset.get_depth_frame()
    # colorizer = rs.colorizer()
    # colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())
    depth = np.asanyarray(aligned_depth_frame.get_data())

    return color, depth


def stop_pipeline():
    pipeline.stop()



