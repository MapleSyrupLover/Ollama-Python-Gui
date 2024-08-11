import sys
from PyQt5.QtCore import QThread, pyqtSignal  # type: ignore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea, QComboBox  # type: ignore
from PyQt5.QtGui import QFont, QColor  # type: ignore
import ollama


# MAKE SURE OLLAMA.EXE IS ALREADY RUNNING
# THIS IS A VERY BASIC GUI AND I WILL BE UPDATING IT, IT MAY LOOK BAD NOW BUT IT I SWEAR IT WILL GET BETTER
# MADE BY MAPLESYRUPLOVER


class ResponseThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, message, model):
        super().__init__()
        self.message = message
        self.model = model

    def run(self):
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'user', 'content': self.message}
            ]
        )
        self.response_signal.emit(response['message']['content'])

class Application(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.threads = []  # List to store ResponseThread objects

    def initUI(self):
        self.setWindowTitle("I REALLY LOVE MAPLE SYRUP!")
        self.setGeometry(200, 200, 750, 575)

        layout = QVBoxLayout()

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setContentsMargins(10, 10, 10, 10)  # Add margins
        self.chat_layout.setSpacing(5)  # Decrease spacing between messages
        self.chat_widget.setLayout(self.chat_layout)
        self.chat_area.setWidget(self.chat_widget)
        layout.addWidget(self.chat_area)

        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setMinimumHeight(30)  # Set minimum height
        self.input_field.setMaximumHeight(30)  # Set maximum height
        input_layout.addWidget(self.input_field)

        self.model_combobox = QComboBox()
        self.model_combobox.addItem("llama2-uncensored")
        self.model_combobox.addItem("llama2")
        self.model_combobox.addItem("llama3")
        self.model_combobox.addItem("llama3.1")
        self.model_combobox.addItem("dolphin-mixtral")
        self.model_combobox.addItem("TO ADD MORE LLMS EDIT SOURCE CODE")  # To add more LLM's of your own just add another combo box
        input_layout.addWidget(self.model_combobox)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setMinimumWidth(100)  # Set minimum width
        self.send_button.setFixedHeight(35)  # Set fixed height
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
            QScrollArea {
                border: none;
            }
            QLabel {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 5px;
            }
        """)

    def send_message(self):
        message = self.input_field.toPlainText()
        model = self.model_combobox.currentText()
        self.add_message("You", message)
        self.input_field.clear()

        thread = ResponseThread(message, model)
        self.threads.append(thread)  # Store the ResponseThread object
        thread.response_signal.connect(self.add_response)
        thread.start()

    def add_response(self, response):
        self.add_message("Ollama", response)

    def add_message(self, sender, message):
        message_widget = QWidget()
        message_layout = QHBoxLayout()
        message_label = QLabel(f"{sender}: {message}")
        message_label.setFont(QFont("Arial", 14))
        message_label.setWordWrap(True)
        message_label.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 5px;")
        if sender == "You":
            message_label.setStyleSheet("background-color: #4CAF50; color: #ffffff; border-radius: 10px; padding: 5px;")
            message_layout.addStretch()
            message_layout.addWidget(message_label)
        else:
            message_label.setStyleSheet("background-color: #cccccc; border-radius: 10px; padding: 5px;")
            message_layout.addWidget(message_label)
            message_layout.addStretch()
        message_widget.setLayout(message_layout)
        self.chat_layout.addWidget(message_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())
