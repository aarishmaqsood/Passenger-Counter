# Passenger-Counter

## Overview
The Passenger Counter project is designed to capture and save video from two cameras simultaneously. It organizes saved videos in a directory structure based on the camera number and the date. This project is particularly useful for monitoring and counting purposes in transportation systems, entry points, or any area where passenger or people counting is required.

## Prerequisites
Before running this project, ensure you have the following installed:
- Python 3.10 or higher
- OpenCV library
- Any additional libraries listed in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```
   git clone https://yourrepositorylink.com/path/to/Passenger-Counter.git
   ```

2. **Navigate to the project directory:**
   ```
   cd Passenger-Counter
   ```

3. **Set up a virtual environment (optional but recommended):**
   ```
   python3 -m venv env_name
   ```

4. **Activate the virtual environment:**
   - On macOS and Linux:
     ```
     source env_name/bin/activate
     ```
   - On Windows:
     ```
     .\env_name\Scripts\activate
     ```

5. **Install the required libraries:**
   ```
   pip install -r requirements.txt
   ```

## Usage
To start capturing video from the cameras, run the main script with optional parameters for customization:

```
python main_video_capture.py --fps 30 --frame_width 1920 --frame_height 1080 --base_path "/path/to/save/videos"
```

### Command-line Arguments
- `--fps`: Specify the frames per second for the video capture. Default is 20.0.
- `--frame_width`: Specify the width of the video frame. Default is 1280.
- `--frame_height`: Specify the height of the video frame. Default is 720.
- `--base_path`: Specify the base path where videos will be saved. Default is "./videos".

Press 'q' to exit the video capture process.