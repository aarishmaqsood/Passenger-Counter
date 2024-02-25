import cv2
import datetime
import argparse
from utils.video_capture_functions import create_directory_structure, initialize_writer, capture_and_write

def main(fps, frame_width, frame_height, base_path):
    try:
        # Initialize video capture for both cameras
        cap1 = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)
        
        frame_size = (frame_width, frame_height)
        
        if not cap1.isOpened() or not cap2.isOpened():
            print("Error: Cameras could not be opened.")
            return
        
        print("Press 'q' to exit...")

        while True:
            start_time = datetime.datetime.now()
            directory1 = create_directory_structure(base_path, 1)
            directory2 = create_directory_structure(base_path, 2)
            writer1 = initialize_writer(directory1, start_time, frame_size, fps)
            writer2 = initialize_writer(directory2, start_time, frame_size, fps)
            
            end_time = start_time + datetime.timedelta(minutes=1)
            while datetime.datetime.now() < end_time:
                frame1 = capture_and_write(cap1, writer1, frame_size)
                frame2 = capture_and_write(cap2, writer2, frame_size)
                
                if frame1 is not None:
                    cv2.imshow('Camera 1', frame1)
                if frame2 is not None:
                    cv2.imshow('Camera 2', frame2)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise KeyboardInterrupt
            writer1.release()
            writer2.release()
            cv2.destroyWindow('Camera 1')
            cv2.destroyWindow('Camera 2')

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        if cap1:
            cap1.release()
        if cap2:
            cap2.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture video from two cameras.")
    parser.add_argument("--fps", type=float, default=20.0, help="Frames per second")
    parser.add_argument("--frame_width", type=int, default=1280, help="Frame width")
    parser.add_argument("--frame_height", type=int, default=720, help="Frame height")
    parser.add_argument("--base_path", type=str, default="./videos", help="Base path for saving videos")
    
    args = parser.parse_args()
    
    main(args.fps, args.frame_width, args.frame_height, args.base_path)
