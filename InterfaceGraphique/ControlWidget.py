from PyQt5.QtWidgets import (
	QVBoxLayout,
	QWidget,
	QPushButton,
	QHBoxLayout,
	QLineEdit,
	QFileDialog,
	QLabel
)


class Controls(QWidget):
	def __init__(self):
		super().__init__()
		
		layout = QVBoxLayout()
		self.setLayout(layout)

		file_selection_title = QLabel()
		file_selection_title.setText("<h4>Select input file</h4>")

		file_selection = FileSelectionWidget()

		layout.addWidget(file_selection_title)
		layout.addWidget(file_selection)


class FileSelectionWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.setLayout(QHBoxLayout())

		file_selection_button = QPushButton("select file")
		file_selection_button.clicked.connect(self.open_file_selection_dialog)
		
		self.file_name = QLineEdit()
		self.file_name.setEnabled(False)
		self.file_name.setText("<input file>")

		self.layout().addWidget(self.file_name)
		self.layout().addWidget(file_selection_button)
		

	def open_file_selection_dialog(self):
		diag = QFileDialog()
		diag.fileSelected.connect(lambda x: self.file_name.setText(x))

		diag.exec()