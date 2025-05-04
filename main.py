import os
import sys
import logging
from pathlib import Path

from markitdown import MarkItDown
from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add console handler to ensure logs are visible in console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Get logger for this module
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)

# Avoid duplicate logs
logger.propagate = False

# Get the application directory
APP_DIR = Path(__file__).parent.absolute()

# Application version
APP_VERSION = "0.1.1"


class DropArea(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Drag and drop PDF, Word (docx), or PowerPoint (pptx) files here")
        self.setMinimumSize(400, 200)
        self.setStyleSheet(
            "QLabel {background-color: #f0f0f0; border: 2px dashed #aaa; border-radius: 8px; font-size: 16px;}"
        )
        self.setAcceptDrops(True)

        # Create MarkItDown instance
        self.mid = MarkItDown(enable_plugins=False)

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            valid_extensions = [".pdf", ".docx", ".pptx"]
            for url in urls:
                file_path = url.toLocalFile()
                if any(file_path.lower().endswith(ext) for ext in valid_extensions):
                    logger.info(f"Valid file detected: {file_path}")
                    event.acceptProposedAction()
                    return
        logger.warning("Dragged content contains no valid files")
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            files_to_convert = []
            for url in urls:
                file_path = url.toLocalFile()
                if file_path.lower().endswith((".pdf", ".docx", ".pptx")):
                    files_to_convert.append(file_path)
            
            logger.info(f"Files to convert: {len(files_to_convert)}")
            
            if files_to_convert:
                successful = []
                failed = []
                for file_path in files_to_convert:
                    try:
                        logger.info(f"Processing file: {file_path}")
                        output_path = self._convert_file(file_path)
                        successful.append((file_path, output_path))
                    except Exception as e:
                        logger.error(f"Conversion failed for {file_path}: {str(e)}", exc_info=True)
                        failed.append((file_path, str(e)))
                
                logger.info(f"Conversion summary: {len(successful)} successful, {len(failed)} failed")
                event.acceptProposedAction()

    def _convert_file(self, file_path):
        input_path = Path(file_path)
        output_path = input_path.with_suffix(".md")
        
        file_size = input_path.stat().st_size / (1024 * 1024)  # Size in MB
        logger.info(f"Starting conversion: {input_path} ({file_size:.2f} MB)")
        
        try:
            result = self.mid.convert(input_path)
            with open(output_path, "w") as f:
                f.write(result.text_content)
            
            if output_path.exists():
                output_size = output_path.stat().st_size / 1024  # Size in KB
                logger.info(f"Conversion complete: {input_path} → {output_path} ({output_size:.2f} KB)")
            else:
                logger.warning(f"Output file not found after conversion: {output_path}")
        except Exception as e:
            logger.error(f"Error during conversion of {input_path}: {str(e)}")
            raise
            
        return str(output_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"MarkItDown GUI v{APP_VERSION}")
        self.setFixedSize(500, 300)
        
        # Try to set icon if available
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            logger.info(f"Icon path: {icon_path}")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add drop area
        self.drop_area = DropArea()
        layout.addWidget(self.drop_area)
        
        # Set central widget
        self.setCentralWidget(central_widget)


def main():
    logger.info("Starting MarkItDown GUI application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    logger.info("Application window displayed")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
