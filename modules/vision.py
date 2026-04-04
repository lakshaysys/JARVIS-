import cv2
import pytesseract # Make sure to install: pip install pytesseract
import os

# If you are on Windows, you must point to where Tesseract is installed:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class JaveirsVision:
    def __init__(self):
        self.camera_index = 0
        self.save_path = "scans/captured_plate.jpg"
        
        # Create folder if it doesn't exist
        if not os.path.exists("scans"):
            os.makedirs("scans")

    def scan_and_read(self):
        """Captures an image and extracts text (Number Plate Recognition)."""
        cap = cv2.VideoCapture(self.camera_index)
        
        if not cap.isOpened():
            return "Error: System could not access the optical sensors."

        # Give the camera a second to adjust to light
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        ret, frame = cap.read()
        cap.release()

        if ret:
            # 1. Save the raw image
            cv2.imwrite(self.save_path, frame)
            
            # 2. Process for OCR (Convert to Grayscale for better reading)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 3. Use Tesseract to read the text
            text = pytesseract.image_to_string(gray, config='--psm 7') # PSM 7 is for single lines
            
            clean_text = text.strip()
            
            if clean_text:
                return f"Scan successful. Detected text: {clean_text}"
            else:
                return "Scan complete, but no clear text was identified on the plate."
        
        return "System failed to capture frame."

# --- Quick Test ---
if __name__ == "__main__":
    vision = JaveirsVision()
    print(vision.scan_and_read())