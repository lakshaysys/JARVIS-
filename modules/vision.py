import os
import cv2
import pytesseract

class JaveirsVision:
    def __init__(self):
        """Initializes optical sensors and scans directory."""
        self.output_dir = "scans"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print("[System] Optical sensors calibrated.")

    def scan_and_read(self):
        """Captures a frame from the camera and processes it for text (OCR)."""
        # 0 is usually the default built-in webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return "Optical sensor failure: Unable to open camera feed."

        # Allow camera to adjust to lighting
        for _ in range(5):
            ret, frame = cap.read()

        if ret:
            # Save the raw capture
            img_path = os.path.join(self.output_dir, "last_scan.jpg")
            cv2.imwrite(img_path, frame)
            
            # Convert to grayscale to help the OCR engine read better
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Extract text from the image
            try:
                extracted_text = pytesseract.image_to_string(gray_frame).strip()
            except Exception as e:
                extracted_text = f"OCR engine error: {str(e)}"

            cap.release()
            
            if extracted_text:
                return f"Scan complete. Data read: '{extracted_text}'"
            else:
                return "Scan complete. No legible data detected in visual field."
        
        cap.release()
        return "Optical sensor failure: Frame capture timed out."

    def process_frame_for_objects(self, frame):
        """Placeholder for custom matrix operations or edge detection."""
        # This converts the image to show distinct outlines/edges
        edges = cv2.Canny(frame, 100, 200)
        return edges