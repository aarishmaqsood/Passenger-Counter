import sqlite3
from ruamel.yaml import YAML
from datetime import datetime
from utils.roi_selection import ROISelector

yaml = YAML()
yaml.preserve_quotes = True 

def load_config(filename='camera_config.yaml'):
    """ Load the YAML configuration file while preserving comments. """
    with open(filename, 'r') as file:
        return yaml.load(file)

def save_config(config, filename='camera_config.yaml'):
    """ Save the YAML configuration file after updating ROIs, preserving comments and format. """
    with open(filename, 'w') as file:
        yaml.dump(config, file)

def update_roi_for_cameras():
    """ Update only the ROI values for each camera in the configuration, preserving other content. """
    config = load_config()  # Load existing configuration
    if not config or 'cameras' not in config:
        print("No camera configuration found.")
        return

    for camera in config['cameras']:
        cam_id = camera.get('camera_id')
        print(f"Updating ROI for camera with ID: {cam_id}...")

        if isinstance(cam_id, str) and '_' in cam_id:
            camera_index = int(cam_id.split('_')[-1]) - 1
        else:
            camera_index = int(cam_id)  # Handle integer or simple numeric strings

        roi_selector = ROISelector(camera_id=camera_index)
        roi = roi_selector.select_roi()

        if roi:
            camera['roi']['x1'] = roi[0]
            camera['roi']['y1'] = roi[1]
            camera['roi']['x2'] = roi[2]
            camera['roi']['y2'] = roi[3]
        else:
            print(f"ROI not defined for camera {cam_id}.")

    save_config(config)

class CountDatabaseManager:
    def __init__(self, db_name='people_counting.db'):
        self.db_name = db_name
        self.conn = None
        self.setup_database()

    def setup_database(self):
        """ Set up the database connection and create the table if it doesn't exist. """
        # Allow connection to be shared across threads
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Counts (
                timestamp TEXT,
                camera_id TEXT,
                count INTEGER
            )
        ''')
        self.conn.commit()

    def insert_count(self, camera_id, count):
        """ Insert a new count into the database. """
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO Counts (timestamp, camera_id, count) VALUES (?, ?, ?)',
                       (datetime.now().isoformat(), camera_id, count))
        self.conn.commit()

    def close(self):
        """ Close the database connection. """
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

