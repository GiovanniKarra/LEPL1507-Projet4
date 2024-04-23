from PyQt5.QtWidgets import (
	QVBoxLayout,
	QWidget,
	QPushButton,
	QHBoxLayout,
	QLineEdit,
	QFileDialog,
	QLabel
)
from PyQt5.QtCore import (
	Qt
)


class Controls(QWidget):
	def __init__(self):
		super().__init__()
		
		layout = QVBoxLayout()
		self.setLayout(layout)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		file_selection = FileSelectionWidget("Select input file")

		layout.addWidget(file_selection)


class FileSelectionWidget(QWidget):
	def __init__(self, title=""):
		super().__init__()

		self.setLayout(QVBoxLayout())

		selection_widget = QWidget()
		selection_widget.setLayout(QHBoxLayout())

		file_selection_button = QPushButton("select file")
		file_selection_button.clicked.connect(self.open_file_selection_dialog)
		
		self.file_name = QLineEdit()
		self.file_name.setEnabled(False)
		self.file_name.setText("<input file>")

		selection_widget.layout().addWidget(self.file_name)
		selection_widget.layout().addWidget(file_selection_button)

		if title != "":
			file_selection_title = QLabel()
			file_selection_title.setText("<h4>%s</h4>"%title)

			self.layout().addWidget(file_selection_title)

		self.layout().addWidget(selection_widget)
		

	def open_file_selection_dialog(self):
		diag = QFileDialog()
		diag.fileSelected.connect(lambda x: self.file_name.setText(x))

		diag.exec()