import os
import cv2
import datetime

def ensure_base_path_exists(base_path):
    """Ensures the base path for saving videos exists."""
    os.makedirs(base_path, exist_ok=True)

def create_directory_structure(base_path, camera_id):
    """Creates a directory structure for saving videos."""
    ensure_base_path_exists(base_path)  # Ensure the base path exists
    
    today = datetime.datetime.now()
    date_folder = today.strftime("%Y-%m-%d")
    camera_folder = f"camera_{camera_id}"
    full_path = os.path.join(base_path, camera_folder, date_folder)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def initialize_writer(base_path, start_time, frame_size, fps):
    """Initializes a video writer object."""
    file_time = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{file_time}.mp4"
    full_file_path = os.path.join(base_path, file_name)
    
    # Use 'mp4v' as the codec for MP4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(full_file_path, fourcc, fps, frame_size)
    return out

def capture_and_write(cap, writer, frame_size):
    """Captures a frame from the camera and writes it to the video file."""
    ret, frame = cap.read()
    if ret:
        resized_frame = cv2.resize(frame, frame_size)
        writer.write(resized_frame)
        return resized_frame
    return None