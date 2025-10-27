import sys
# Using PyQt5 as requested
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
# --- 1. IMPORT 'setTheme' ---
from qfluentwidgets import FluentWindow, PushButton, Theme, setTheme, FluentIcon
# FluentIcon is no longer needed since we are passing None
# from qfluentwidgets import FluentIcon 

class MyWindow(FluentWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Browser Button (Dark Mode)")
        self.setGeometry(300, 300, 500, 400)

        # Create a "page" widget
        self.homePage = QWidget()
        self.homePage.setObjectName("homePage") # Don't forget this!
        
        # Create a layout for the page
        self.pageLayout = QVBoxLayout(self.homePage)

        # Create the PushButton
        self.myButton = PushButton("Browse for File", self.homePage) # Changed text
        
        # Add the button to the page's layout
        self.pageLayout.addWidget(self.myButton)
        self.pageLayout.addStretch(1) 

        # Add your page as an interface (with no icon, as requested)
        self.addSubInterface(self.homePage, FluentIcon.HOME, "Home")

        # Connect the click event
        self.myButton.clicked.connect(self.on_button_clicked)

    # --- THIS METHOD IS UNCHANGED ---
    def on_button_clicked(self):
        print("Button clicked, opening file dialog...")
        
        # Open the native file explorer dialog
        # It returns a tuple: (selected_file_path, selected_filter)
        # We use '_' to discard the selected_filter part
        file_path, _ = QFileDialog.getOpenFileName(
            self,                                 # Parent widget
            "Select a File",                      # Dialog window title
            "",                                   # Starting directory (empty = last used)
            "All Files (*.*);;Text Files (*.txt);;Python Files (*.py)" # File filters
        )
        
        # This 'if' checks if the user selected a file (and didn't click 'Cancel')
        if file_path:
            print(f"You selected this file: {file_path}")
            # You can now do something with the file_path,
            # like opening it or displaying it in a label

# Standard application startup
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- 2. SET THE THEME TO DARK ---
    setTheme(Theme.DARK)
    # --------------------------------

    window = MyWindow()
    window.resize(800, 600)
    window.show()
    
    # --- 3. USE app.exec_() for PyQt5 ---
    sys.exit(app.exec_())
