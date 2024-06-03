import cv2

class ROISelector:
    """
    A class to select a region of interest (ROI) by drawing a rectangle on an image or the first frame of a video,
    or from a live camera feed, with interactive feedback and instructions.
    """

    def __init__(self, video_path=None, image_path=None, camera_id=None):
        """
        Initializes the ROISetter with a video path, an image path, or a camera ID.
        """
        assert sum([bool(video_path), bool(image_path), bool(camera_id is not None)]) == 1, \
            "Exactly one source must be provided."
        
        self.video_path = video_path
        self.image_path = image_path
        self.camera_id = camera_id
        self.points = []
        self.original_image = None
        self.current_instruction = ""

    def _click_event(self, event, x, y, flags, param):
        """
        Internal method to handle mouse click events, drawing a rectangle dynamically and providing visual feedback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < 2:  # Only allow two points for a rectangle
                self.points.append((x, y))
                self.update_instructions()
                self.redraw_elements()

    def update_instructions(self):
        """
        Updates the instructions based on the current state of point selection.
        """
        if len(self.points) == 1:
            text = "First corner set. Now click to select the opposite corner. Press 'z' to undo."
        elif len(self.points) == 2:
            text = "Rectangle defined. Press 'q' to finalize and save, or 'z' to adjust corners."
        else:
            text = "Click to select the first corner of the ROI. Ensure visibility of all corners for accurate selection."
        
        if text != self.current_instruction:
            self.current_instruction = text
            self._display_instructions(self.current_instruction, self.original_image)

    def redraw_elements(self):
        """
        Redraw points and rectangle on the image based on the current points list.
        """
        self.original_image = self.original_image.copy()
        if len(self.points) > 0:
            for point in self.points:
                cv2.circle(self.original_image, point, 5, (0, 0, 255), -1)  # Red circle at each point
        if len(self.points) == 2:
            cv2.rectangle(self.original_image, self.points[0], self.points[1], (0, 0, 255), 2)  # Rectangle in red

    def _display_instructions(self, text, image):
        """
        Display instructions on the image.
        """
        font_scale = 0.7
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_color = (0, 0, 0)  # Black
        x, y = 10, 30
        cv2.putText(image, text, (x, y), font, font_scale, text_color, 2)

    def select_roi(self):
        """
        Displays the image or video frame and allows the user to select the ROI by drawing a rectangle,
        with instructions and visual feedback.
        """
        window_name = "Image"
        cap = None
        if self.image_path:
            image = cv2.imread(self.image_path)
        elif self.video_path:
            cap = cv2.VideoCapture(self.video_path)
        elif self.camera_id is not None:
            cap = cv2.VideoCapture(self.camera_id)

        if cap:
            if not cap.isOpened():
                print("Failed to open the video or camera.")
                return None
            success, image = cap.read()
            if not success:
                print("Failed to read from the video or camera.")
                return None

        self.original_image = image.copy()
        self.update_instructions()  # Initial instruction set
        cv2.imshow(window_name, self.original_image)
        cv2.setMouseCallback(window_name, self._click_event, self.original_image)

        while True:
            if cap:
                success, image = cap.read()
                if not success:
                    break
                self.original_image = image.copy()
            self.redraw_elements()
            self._display_instructions(self.current_instruction, self.original_image)
            cv2.imshow(window_name, self.original_image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('z') and self.points:  # Undo the last point
                self.points.pop()
                self.update_instructions()
                self.redraw_elements()
            elif key == ord('q'):  # Quit
                break

        cv2.destroyAllWindows()
        if cap:
            cap.release()

        if len(self.points) < 2:
            print("ROI not properly defined.")
            return None
        else:
            x1, y1 = self.points[0]
            x2, y2 = self.points[1]
            return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
