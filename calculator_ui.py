from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QComboBox,
    QPushButton, QLabel, QGridLayout
)
import sys

# requires pip install PySide6

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")

        # Widgets
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()

        self.operation = QComboBox()
        self.operation.addItems(["Add", "Subtract", "Multiply"])

        self.button = QPushButton("Calculate")
        self.button.clicked.connect(self.calculate)

        self.result_label = QLabel("Result: ")

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.input1, 0, 0)
        layout.addWidget(self.input2, 0, 1)
        layout.addWidget(self.operation, 1, 0, 1, 2)
        layout.addWidget(self.button, 2, 0, 1, 2)
        layout.addWidget(self.result_label, 3, 0, 1, 2)

        self.setLayout(layout)

    def calculate(self):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())
            op = self.operation.currentText()

            if op == "Add":
                result = num1 + num2
            elif op == "Subtract":
                result = num1 - num2
            elif op == "Multiply":
                result = num1 * num2
            else:
                result = "Unknown op"

            self.result_label.setText(f"Result: {result}")

        except ValueError:
            self.result_label.setText("Please enter valid numbers")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
