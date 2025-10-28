import sys
import os
# Using PyQt5 as requested
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt

# --- 1. IMPORTS ADDED ---
from qfluentwidgets import (FluentWindow, PushButton, Theme, setTheme, 
                            BodyLabel, InfoBar, InfoBarPosition, StrongBodyLabel,
                            SimpleCardWidget, PrimaryPushButton, FluentIcon)
# Import the function from your scanner.py file
try:
    from scanner import verify_file_type
except ImportError:
    print("Could not import from scanner.py. Make sure it's in the same directory.")
    # Create a dummy function so the app can still run
    def verify_file_type(file_path):
        return {"error": "Could not find scanner.py"}

# --- NEW: Import from report.py ---
try:
    from report import generate_pdf_report
except ImportError:
    print("Could not import from report.py. Make sure it's in the same directory.")
    print("Install reportlab: pip install reportlab")
    def generate_pdf_report(save_path, file_path, scan_results, status_text):
        print("PDF generation function not found.")
        return False


class MyWindow(FluentWindow):
    
    # Simple map to check extension vs MIME.
    # This is very basic and can be expanded.
    MIME_MAP = {
        ".txt": "text/plain",
        ".py": "text/x-python",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".pdf": "application/pdf",
        ".zip": "application/zip",
        ".exe": "application/x-ms-dos-executable",
        ".mp3": "audio/mpeg",
        ".wav": "audio/x-wav",
    }
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Metadata Scanner")
        self.setGeometry(300, 300, 700, 650) # Made window taller

        # Create a "page" widget
        self.homePage = QWidget()
        self.homePage.setObjectName("homePage")
        
        # Create a layout for the page
        self.pageLayout = QVBoxLayout(self.homePage)
        self.pageLayout.setSpacing(10) # Add some spacing
        self.pageLayout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align widgets to top

        # Create the PushButton
        self.myButton = PrimaryPushButton("Browse and Scan File", self.homePage) # Changed to PrimaryPushButton
        
        # Add the button to the page's layout
        self.pageLayout.addWidget(self.myButton)
        
        # --- 2. ADD LABELS FOR RESULTS ---
        # We'll group results in a card for a cleaner look
        self.resultsCard = SimpleCardWidget(self.homePage)
        self.resultsLayout = QVBoxLayout(self.resultsCard)
        self.resultsLayout.setContentsMargins(15, 10, 15, 10) # Add padding
        self.resultsLayout.setSpacing(8)
        
        self.selectedFileLabel = BodyLabel("No file selected", self.resultsCard)
        self.selectedFileLabel.setWordWrap(True)
        
        # --- NEW: Permanent Status Label ---
        self.statusLabel = StrongBodyLabel("Status: Not yet scanned", self.resultsCard)
        
        # --- NEW: Metadata Labels ---
        self.sizeLabel = BodyLabel("Size: -", self.resultsCard)
        self.hashLabel = BodyLabel("SHA256: -", self.resultsCard)
        self.hashLabel.setWordWrap(True) # Hash is long
        
        self.originalExtLabel = BodyLabel("Original Extension: -", self.resultsCard)
        self.detectedMimeLabel = BodyLabel("Detected MIME: -", self.resultsCard)
        self.descriptionLabel = BodyLabel("Description: -", self.resultsCard)
        self.descriptionLabel.setWordWrap(True)
        
        self.createdLabel = BodyLabel("Created: -", self.resultsCard)
        self.modifiedLabel = BodyLabel("Modified: -", self.resultsCard)

        # --- NEW: Save Report Button ---
        self.saveReportButton = PushButton("Save Report", self.resultsCard)
        self.saveReportButton.setToolTip("Save the current scan results as a PDF")

        # Add all labels to the card's layout
        self.resultsLayout.addWidget(self.selectedFileLabel)
        self.resultsLayout.addWidget(self.statusLabel)
        self.resultsLayout.addSpacing(10) # Add a small break
        self.resultsLayout.addWidget(self.originalExtLabel)
        self.resultsLayout.addWidget(self.detectedMimeLabel)
        self.resultsLayout.addWidget(self.descriptionLabel)
        self.resultsLayout.addSpacing(10)
        self.resultsLayout.addWidget(self.sizeLabel)
        self.resultsLayout.addWidget(self.hashLabel)
        self.resultsLayout.addWidget(self.createdLabel)
        self.resultsLayout.addWidget(self.modifiedLabel)
        self.resultsLayout.addSpacing(15) # Add space before button
        self.resultsLayout.addWidget(self.saveReportButton)

        # Add the card to the main page layout
        self.pageLayout.addWidget(self.resultsCard)
        
        self.pageLayout.addStretch(1) # Keep stretch at the bottom

        # Add your page as an interface (with no icon, as requested)
        self.addSubInterface(self.homePage, FluentIcon.HOME, "Home")

        # Connect the click event
        self.myButton.clicked.connect(self.on_scan_button_clicked)
        # --- NEW: Connect Save Button ---
        self.saveReportButton.clicked.connect(self.on_save_report_clicked)
        
        # --- NEW: Class variables to store results ---
        self.current_scan_result = None
        self.current_file_path = None
        self.current_status_text = ""
        
        # Call reset function to set initial "empty" state
        self.reset_labels()

    def reset_labels(self):
        """Resets all labels to their default state."""
        self.selectedFileLabel.setText("No file selected")
        
        # Set status to neutral
        self.statusLabel.setText("Status: Not yet scanned")
        self.statusLabel.setStyleSheet("color: #E6A23C;") # Set to yellow
        
        self.originalExtLabel.setText("Original Extension: -")
        self.detectedMimeLabel.setText("Detected MIME: -")
        self.descriptionLabel.setText("Description: -")
        self.sizeLabel.setText("Size: -")
        self.hashLabel.setText("SHA256: -")
        self.createdLabel.setText("Created: -")
        self.modifiedLabel.setText("Modified: -")
        
        # --- NEW: Hide button and clear results ---
        self.saveReportButton.hide()
        self.current_scan_result = None
        self.current_file_path = None
        self.current_status_text = ""

    def on_scan_button_clicked(self):
        print("Button clicked, opening file dialog...")
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File to Scan",
            "",
            "All Files (*.*)" # Changed to all files for scanning
        )
        
        if file_path:
            print(f"File selected: {file_path}")
            # Reset labels to show we are processing
            self.reset_labels()
            self.selectedFileLabel.setText(f"Scanning: {file_path}")
            QApplication.processEvents() # Force UI update
            
            # --- 3. CALL YOUR UPDATED FUNCTION ---
            print("Calling verify_file_type...")
            result = verify_file_type(file_path)
            print(f"Scan result received: {result}")
            
            # Update file label
            self.selectedFileLabel.setText(f"File: {file_path}")

            # Check for errors from the function
            if "error" in result:
                print(f"Error from scanner: {result['error']}")
                self.statusLabel.setText(f"Status: Scan Error!")
                self.statusLabel.setStyleSheet("color: #F7BA2B;") # Warning yellow
                self.descriptionLabel.setText(result['error'])
                # Use InfoBar for critical errors
                InfoBar.error(
                    "Scan Error",
                    result['error'],
                    parent=self.homePage,
                    duration=4000,
                    position=InfoBarPosition.TOP
                )
                return

            # --- 4. UPDATE ALL LABELS ---
            self.originalExtLabel.setText(f"Original Extension: {result['extension']}")
            self.detectedMimeLabel.setText(f"Detected MIME: {result['detected_mime']}")
            self.descriptionLabel.setText(f"Description: {result['description']}")
            self.sizeLabel.setText(f"Size: {result['size']}")
            self.hashLabel.setText(f"SHA256: {result['hash_sha256']}")
            self.createdLabel.setText(f"Created: {result['creation_time']}")
            self.modifiedLabel.setText(f"Modified: {result['modified_time']}")
            
            # --- 5. CHECK FOR SPOOFING (and set permanent label) ---
            self.check_spoof_status(result)
            
            # --- NEW: Store results and show button ---
            self.current_scan_result = result
            self.current_file_path = file_path
            self.current_status_text = self.statusLabel.text() # Get the final status
            self.saveReportButton.show()

    def check_spoof_status(self, result):
        ext = result['extension']
        mime = result['detected_mime']
        
        # Define colors for status
        green_color = "#67C23A"
        red_color = "#F56C6C"
        yellow_color = "#E6A23C"
        
        if not ext and mime == "application/octet-stream":
            self.statusLabel.setText("Status: UNKNOWN")
            self.statusLabel.setStyleSheet(f"color: {yellow_color};")
            self.descriptionLabel.setText("File has no extension and is an unknown binary type.")
            return

        if ext not in self.MIME_MAP:
            self.statusLabel.setText("Status: UNKNOWN")
            self.statusLabel.setStyleSheet(f"color: {yellow_color};")
            self.descriptionLabel.setText(f"Unknown extension '{ext}'. Cannot verify against MIME type.")
            return

        # The actual check
        expected_mime = self.MIME_MAP[ext]
        
        # Check if the main type (e.g., 'image') or the full type matches
        is_match = (mime == expected_mime)
        is_type_match = mime.startswith(expected_mime.split('/')[0] + "/")
        
        if is_match or is_type_match:
            self.statusLabel.setText("Status: LEGITIMATE")
            self.statusLabel.setStyleSheet(f"color: {green_color};")
        else:
            self.statusLabel.setText("Status: POTENTIAL SPOOF!")
            self.statusLabel.setStyleSheet(f"color: {red_color};")
            # Overwrite description to make spoofing clear
            self.descriptionLabel.setText(
                f"Warning: File extension is '{ext}' (expects '{expected_mime}') "
                f"but content is actually '{mime}'!"
            )

    # --- NEW: Method to save the report ---
    def on_save_report_clicked(self):
        print("Save report button clicked...")
        if not self.current_scan_result or not self.current_file_path:
            print("No scan data to save.")
            InfoBar.warning(
                "No Data",
                "Please scan a file before saving a report.",
                parent=self.homePage,
                duration=3000,
                position=InfoBarPosition.TOP
            )
            return

        # Get the original filename to suggest it for the PDF
        original_filename = os.path.basename(self.current_file_path)
        suggested_name = os.path.splitext(original_filename)[0] + "_scan_report.pdf"

        # Ask user where to save the file
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report As PDF",
            suggested_name,
            "PDF Files (*.pdf)"
        )

        if not save_path:
            print("User cancelled save dialog.")
            return

        # Ensure the path ends with .pdf
        if not save_path.lower().endswith(".pdf"):
            save_path += ".pdf"
            
        print(f"Attempting to save report to: {save_path}")

        # Call the function from report.py
        success = generate_pdf_report(
            save_path,
            self.current_file_path,
            self.current_scan_result,
            self.current_status_text
        )

        # Show confirmation
        if success:
            InfoBar.success(
                "Report Saved",
                f"Report successfully saved to {save_path}",
                parent=self.homePage,
                duration=4000,
                position=InfoBarPosition.TOP
            )
        else:
            InfoBar.error(
                "Save Failed",
                "An error occurred while saving the PDF report.",
                parent=self.homePage,
                duration=4000,
                position=InfoBarPosition.TOP
            )


# Standard application startup
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    setTheme(Theme.DARK)
    
    window = MyWindow()
    window.show()
    
    # Use app.exec_() for PyQt5
    sys.exit(app.exec_())



