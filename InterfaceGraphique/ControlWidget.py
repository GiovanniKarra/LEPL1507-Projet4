from PyQt5.QtWidgets import (
	QVBoxLayout,
	QWidget,
	QPushButton,
	QHBoxLayout,
	QLineEdit,
	QFileDialog,
	QLabel,
	QCheckBox
)
from PyQt5.QtCore import (
	Qt,
	pyqtSignal
)
from PyQt5.QtGui import (
	QIntValidator,
	QDoubleValidator
)


class Controls(QWidget):

	file_selected = pyqtSignal(str)
	solve = pyqtSignal(int, bool, float)  # num_de_satellites: int, 3D: bool
	set_names = pyqtSignal(int)
	toggled_threeD = pyqtSignal(bool)

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		
		file_selection = FileSelectionWidget(title="Select input file")
		file_selection.file_selected.connect(self.file_selected)

		dim_selection = DimSelectionWidget()
		dim_selection.toggled_threeD.connect(self.toggled_threeD)
		dim_selection.setFixedWidth(120)

		sat_num_selection = NumWidget("Number of satellites")
		sat_num_selection.setFixedWidth(235)

		radius_selection = NumWidget("Satellite radius", float)
		radius_selection.setFixedWidth(200)

		solve_button = QPushButton("Run")
		solve_button.pressed.connect(
			lambda:
				self.solve.emit(sat_num_selection.num,
								dim_selection.threeD,
								radius_selection.num)
		)
		solve_button.setFixedWidth(50)

		show_names = CheckboxWidget("Show city names?")
		show_names.setFixedWidth(200)
		show_names.checked.connect(self.set_names)

		layout.addWidget(file_selection)
		layout.addWidget(show_names)
		layout.addWidget(dim_selection)
		layout.addWidget(sat_num_selection)
		layout.addWidget(radius_selection)
		layout.addWidget(solve_button)


class FileSelectionWidget(QWidget):
	file_selected = pyqtSignal(str)

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
		self.file_name.textChanged.connect(self.file_selected)

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


class DimSelectionWidget(QWidget):

	toggled_threeD = pyqtSignal(bool)

	def __init__(self):
		super().__init__()

		self.threeD = False

		self.setLayout(QHBoxLayout())

		self.twoD_button = QPushButton("2D")
		self.twoD_button.setEnabled(False)
		self.twoD_button.pressed.connect(self.toggle_threeD)

		self.threeD_button = QPushButton("3D")
		self.threeD_button.pressed.connect(self.toggle_threeD)

		self.layout().addWidget(self.twoD_button)
		self.layout().addWidget(self.threeD_button)

	def toggle_threeD(self):
		self.threeD = not self.threeD

		self.twoD_button.setEnabled(self.threeD)
		self.threeD_button.setEnabled(not self.threeD)

		self.toggled_threeD.emit(self.threeD)


class NumWidget(QWidget):
	def __init__(self, label, type=int):
		super().__init__()

		self.num = 0

		self.type = type

		self.setLayout(QHBoxLayout())

		text = QLabel()
		text.setText("%s:"%label)

		num_field = QLineEdit()
		if type is int:
			num_field.setValidator(QIntValidator(0, 9999, self))
		else:
			num_field.setValidator(QDoubleValidator(0, 9999, 3, self))
		num_field.setText("0")
		num_field.textEdited.connect(self.set_num)

		self.layout().addWidget(text)
		self.layout().addWidget(num_field)

	def set_num(self, num):
		self.num = self.type(num)


class CheckboxWidget(QWidget):

	checked = pyqtSignal(int)

	def __init__(self, label=""):
		super().__init__()

		self.setLayout(QHBoxLayout())

		text = QLabel()
		text.setText(label)

		box = QCheckBox()
		box.stateChanged.connect(self.checked)

		self.layout().addWidget(text)
		self.layout().addWidget(box)
		