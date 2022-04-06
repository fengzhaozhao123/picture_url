import pyrealsense2 as rs
import numpy as np
import cv2

save_path = "d:/Desktop/data/car138/"

if __name__ == "__main__":
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    rs_align_color = rs.align(rs.stream.color)
    i = 1
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            for a in range(0, 40):
                pipeline.wait_for_frames()
            frames = pipeline.wait_for_frames()
            # Align all frames to color viewport
            Data = rs_align_color.process(frames)
            depth_frame = Data.get_depth_frame()
            color_frame = Data.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            dist_to_center = depth_frame.get_distance(int(width / 2), int(height / 2))
            print(dist_to_center)
            # Convert images to numpy arrays
            depth_data = np.asanyarray(depth_frame.get_data(), dtype="float16")
            depth_image = np.asanyarray(depth_frame.get_data())

            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            key = cv2.waitKey(1)
            # 写RGB
            rgb_path = save_path + str(i) + ".jpg"
            cv2.imwrite(rgb_path, color_image)
            # 深度信息由采集到的float16直接保存为npy格式
            depth_path = save_path + "{}".format(i)
            np.save(depth_path, depth_data)
            i += 1
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        # Stop streaming
        pipeline.stop()