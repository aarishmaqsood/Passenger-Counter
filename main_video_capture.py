import cv2
import datetime
import argparse
from utils.video_capture_functions import create_directory_structure, initialize_writer, capture_and_write

def main(fps, frame_width, frame_height, base_path):
    try:
        # Attempt to initialize video capture for cameras
        caps = [cv2.VideoCapture(i) for i in range(4)]  # Adjust the range of availaible cameras
        # Filter out cameras that could not be opened
        caps = [cap for cap in caps if cap.isOpened()]

        if not caps:
            print("Error: No cameras could be opened.")
            return

        frame_size = (frame_width, frame_height)
        print("Press 'q' to exit...")

        while True:
            start_time = datetime.datetime.now()
            directories = [create_directory_structure(base_path, i+1) for i in range(len(caps))]
            writers = [initialize_writer(directories[i], start_time, frame_size, fps) for i in range(len(caps))]
            
            end_time = start_time + datetime.timedelta(minutes=1)
            while datetime.datetime.now() < end_time:
                for i, cap in enumerate(caps):
                    frame = capture_and_write(cap, writers[i], frame_size)
                    if frame is not None:
                        cv2.imshow(f'Camera {i+1}', frame)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        raise KeyboardInterrupt
            
            for writer in writers:
                writer.release()
            for i in range(len(caps)):
                cv2.destroyWindow(f'Camera {i+1}')

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        for cap in caps:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture video from two cameras.")
    parser.add_argument("--fps", type=float, default=20.0, help="Frames per second")
    parser.add_argument("--frame_width", type=int, default=1280, help="Frame width")
    parser.add_argument("--frame_height", type=int, default=720, help="Frame height")
    parser.add_argument("--base_path", type=str, default="./videos", help="Base path for saving videos")
    
    args = parser.parse_args()
    
    main(args.fps, args.frame_width, args.frame_height, args.base_path)
