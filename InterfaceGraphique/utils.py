from PyQt5.QtWidgets import (
	QMessageBox
)

import traceback


def popup_error(text, err=None):
	diag = QMessageBox()
	diag.setText(text)

	if err is not None: traceback.print_exception(err)

	diag.exec()