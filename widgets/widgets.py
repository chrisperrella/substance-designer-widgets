import os
from pathlib import Path
from PySide2 import QtSvg, QtGui, QtCore, QtWidgets


class dialog_template(QtWidgets.QDialog):
	def __init__(self, title, ui_mgr=None, parent=None):
		super(dialog_template, self).__init__()
		
		self.ui_mgr = ui_mgr
		self.setWindowTitle(title)
		self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)) 

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
		
		self.logo_layout = QtWidgets.QHBoxLayout()

		self.logo = icon_svg("sbs", 128)
		self.logo_label = QtWidgets.QLabel()
		self.logo_label.setPixmap(self.logo.pixmap(QtCore.QSize(128, 128)))

		self.tool_name = QtWidgets.QLabel("Tools")
		self.tool_name.setAlignment(QtCore.Qt.AlignCenter)
		self.tool_name.setStyleSheet("font-size: 24px;")
		
		self.logo_layout.addWidget(self.logo_label)
		self.logo_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		self.logo_layout.addWidget(self.tool_name)
		self.logo_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
		
		self.vertical_layout = QtWidgets.QVBoxLayout()

		self.cancel_accept_layout = QtWidgets.QHBoxLayout()
		self.cancel = QtWidgets.QPushButton(self)
		self.cancel.setText("Cancel")
		self.cancel_accept_layout.addWidget(self.cancel)
		self.accept = QtWidgets.QPushButton(self)
		self.accept.setText("Accept")
		self.cancel_accept_layout.addWidget(self.accept)
		self.cancel.clicked.connect(self.close_clicked)

		self.progress = progress_bar()
		
		self.layout.addLayout(self.logo_layout)		
		self.layout.addWidget(styled_separator())
		self.layout.addLayout(self.vertical_layout)
		self.layout.addWidget(styled_separator())		
		self.layout.addLayout(self.cancel_accept_layout)
		self.layout.addWidget(self.progress)
		
		self.setLayout(self.layout)

	def close_clicked(self):
		self.close()


class file_browser(QtWidgets.QWidget):
	def __init__(self, browse_title="Browse...", start_dir="", ext_filter=""):
		super(file_browser, self).__init__()

		self.browse_title = browse_title
		self.start_dir = start_dir
		self.ext_filter = ext_filter

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setAlignment(QtCore.Qt.AlignRight)

		self.widget = QtWidgets.QWidget(self)
		self.browse_button = QtWidgets.QPushButton(self.widget)
		self.browse_button.setStyleSheet('QPushButton { max-width: 12; max-height: 12; min-width: 12; min-height: 12; alignment: center; }')

		self.svg_icon = icon_svg("folder", 12)
		self.browse_button.setIcon(self.svg_icon.pixmap(QtCore.QSize(12, 12)))

		self.vertical_layout.addWidget(self.browse_button)

		self.setLayout(self.vertical_layout)


class reset_button(QtWidgets.QWidget):
	def __init__(self):
		super(reset_button, self).__init__()

		self.vertical_layout = QtWidgets.QVBoxLayout(self)
		self.vertical_layout.setAlignment(QtCore.Qt.AlignRight)
		self.vertical_layout.setContentsMargins(8, 8, 8, 8)
		self.vertical_layout.setSpacing(4)

		self.widget = QtWidgets.QWidget(self)
		self.widget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum))

		self.reset_button = QtWidgets.QPushButton(self.widget)
		self.reset_button.setMaximumSize(QtCore.QSize(8, 8))
		self.reset_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum))
		self.reset_button.setStyleSheet(stylesheet("qpushbutton"))

		self.vertical_layout.addWidget(self.reset_button, alignment=QtCore.Qt.AlignCenter)

		self.setLayout(self.vertical_layout)


class styled_separator(QtWidgets.QFrame):
	def __init__(self, parent=None):
		super(styled_separator, self).__init__(parent)
		self.horizontal_layout = QtWidgets.QHBoxLayout(self)
		
		self.setFrameShape(QtWidgets.QFrame.HLine)
		self.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum))
		
		self.setLayout(self.horizontal_layout)
		

class text_with_line_edits(QtWidgets.QWidget):
	def __init__(self, label, default_text='...'):
		super(text_with_line_edits, self).__init__()
		
		self.horizontal_layout = QtWidgets.QHBoxLayout(self)

		self.line_edit = QtWidgets.QLineEdit()
		self.line_edit.setPlaceholderText(default_text)

		self.label = QtWidgets.QLabel(label)

		self.horizontal_layout.addWidget(self.label)
		self.horizontal_layout.addWidget(self.line_edit)
		self.setLayout(self.horizontal_layout)

	def get(self):
		return self.line_edit.text()


class file_browser_line_edit(text_with_line_edits):
	def __init__(self, browse_title="", start_dir="", ext_filter="", *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.browse_button = file_browser(browse_title=browse_title, start_dir=start_dir, ext_filter=ext_filter)
		self.browse_button.browse_button.clicked.connect(self.browse_clicked)
		self.reset_button = reset_button()
		self.reset_button.reset_button.clicked.connect(self.reset_clicked)

		self.horizontal_layout.addWidget(self.browse_button)
		self.horizontal_layout.addWidget(self.reset_button)

	def reset_clicked(self):
		self.line_edit.setText('')

	def browse_clicked(self):
		file_path = QtWidgets.QFileDialog.getSaveFileName(self, 
														caption=self.browse_button.browse_title, 
														dir=str(self.browse_button.start_dir), 
														filter=self.browse_button.ext_filter)[0]													  			
		if file_path:
			self.line_edit.setText(file_path)

	def get(self):
		return self.line_edit.text()


class checkbox_with_reset(QtWidgets.QWidget):
	def __init__(self, text):
		super(checkbox_with_reset, self).__init__()

		self.horizontal_layout = QtWidgets.QHBoxLayout()
		self.horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
		self.horizontal_layout.setContentsMargins(8, 8, 8, 8)
		self.horizontal_layout.setSpacing(8)

		self.checkbox = QtWidgets.QCheckBox(self)
		self.checkbox.setText(text)

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.checkbox.sizePolicy().hasHeightForWidth())
		self.checkbox.setSizePolicy(sizePolicy)
		self.checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
		self.checkbox.setChecked(True)

		self.reset_button = reset_button()

		self.horizontal_layout.addWidget(self.checkbox)
		self.horizontal_layout.addWidget(styled_separator())
		self.horizontal_layout.addWidget(self.reset_button)
		self.setLayout(self.horizontal_layout)

		self.reset_button.reset_button.clicked.connect(self.reset_checkbox)

	def get(self):
		return self.checkbox.isChecked()

	def reset_checkbox(self):
		self.checkbox.setChecked(True)


class horizontal_combobox_with_icon(QtWidgets.QWidget):
	def __init__(self, svg_path, items=[]):
		super(horizontal_combobox_with_icon, self).__init__()

		self.horizontal_layout = QtWidgets.QHBoxLayout()
		
		self.label_icon = QtWidgets.QLabel()
		self.label_icon.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
		self.svg_icon = icon_svg(svg_path, 24)
		self.label_icon.setPixmap(self.svg_icon.pixmap(QtCore.QSize(24, 24)))
		self.label_icon.setContentsMargins(8, 8, 8, 8)

		self.combobox = QtWidgets.QComboBox()
		self.combobox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
		
		for item in items:
			self.combobox.addItem(str(item))		
		self.reset_button = reset_button()

		self.horizontal_layout.addWidget(self.label_icon)
		self.horizontal_layout.addWidget(self.combobox)
		self.horizontal_layout.addWidget(self.reset_button)
		self.horizontal_layout.setAlignment(QtCore.Qt.AlignLeft)
		self.setLayout(self.horizontal_layout)

		self.reset_button.reset_button.clicked.connect(self.reset_combobox)

	def add_items(self, items):
		for item in items:
			self.combobox.addItem(str(item))
	
	def get(self):
		return self.combobox.currentText()

	def reset_combobox(self):
		self.combobox.setCurrentIndex(0)


class horizontal_combobox_with_label_and_reset(QtWidgets.QWidget):
	def __init__(self, text, items=[]):
		super(horizontal_combobox_with_label_and_reset, self).__init__()

		self.horizontal_layout = QtWidgets.QHBoxLayout()
		
		self.label = QtWidgets.QLabel(text)
		self.label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))

		self.combobox = QtWidgets.QComboBox()
		self.combobox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))
		for item in items:
			self.combobox.addItem(str(item))
		self.reset_button = reset_button()

		self.horizontal_layout.addWidget(self.label)
		self.horizontal_layout.addWidget(self.combobox)
		self.horizontal_layout.addWidget(styled_separator())
		self.horizontal_layout.addWidget(self.reset_button)
		self.setLayout(self.horizontal_layout)

		self.reset_button.reset_button.clicked.connect(self.reset_combobox)
	
	def add_items(self, items):
		for item in items:
			self.combobox.addItem(str(item))

	def reset_combobox(self):
		self.combobox.setCurrentIndex(0)

	def get(self):
		return self.combobox.currentText()


class slider_spinbox(QtWidgets.QWidget):
	def __init__(self, min=-5, max=5, default=0):
		super(slider_spinbox, self).__init__()

		self.default = default

		self.horizontal_layout = QtWidgets.QHBoxLayout()

		self.top_slider = QtWidgets.QSlider()
		self.top_slider.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum))
		self.top_slider.setMinimum(min * 100)
		self.top_slider.setMaximum(max * 100)
		self.top_slider.setValue(default * 100)
		self.top_slider.setOrientation(QtCore.Qt.Horizontal)

		self.bottom_spinbox = QtWidgets.QDoubleSpinBox()
		self.bottom_spinbox.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))
		self.bottom_spinbox.setRange(min, max)
		self.bottom_spinbox.setSingleStep(0.005)
		self.bottom_spinbox.setValue(default)
		self.bottom_spinbox.setAlignment(QtCore.Qt.AlignCenter)
		self.bottom_spinbox.setDecimals(3)
		self.bottom_spinbox.setFixedWidth(70)

		self.reset_button = reset_button()
		self.reset_button.reset_button.clicked.connect(self.reset_slider)

		self.horizontal_layout.addWidget(self.top_slider)
		self.horizontal_layout.addWidget(self.bottom_spinbox)
		self.horizontal_layout.addWidget(self.reset_button)
		
		self.top_slider.valueChanged.connect(self.on_slider_update)
		self.bottom_spinbox.valueChanged.connect(self.on_spinbox_update)

		self.setLayout(self.horizontal_layout)

	def on_slider_update(self):
		value = self.top_slider.value() / 100
		self.bottom_spinbox.setValue(value)

	def on_spinbox_update(self):
		value = self.bottom_spinbox.value() * 100
		self.top_slider.setValue(value)

	def reset_slider(self):
		print(self.default)
		self.bottom_spinbox.setValue(self.default)


class horizontal_xy_sliders_and_reset(QtWidgets.QWidget):
	def __init__(self, title, x_min=-5, x_max=5, y_min=-5, y_max=5, default_x=0, default_y=0):
		super(horizontal_xy_sliders_and_reset, self).__init__()

		self.horizontal_layout = QtWidgets.QHBoxLayout()
		self.horizontal_layout.setContentsMargins(8, 0, 0, 0)
		self.vertical_layout = QtWidgets.QVBoxLayout()
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)		

		self.title = QtWidgets.QLabel(title)

		self.x_slider = slider_spinbox(x_min, x_max, default_x)
		self.y_slider = slider_spinbox(y_min, y_max, default_y)
		
		self.horizontal_layout.addWidget(self.title)
		self.vertical_layout.addWidget(self.x_slider)
		self.vertical_layout.addWidget(self.y_slider)
		self.horizontal_layout.addLayout(self.vertical_layout)

		self.setLayout(self.horizontal_layout)

	def get(self):
		return self.x_slider.top_slider.value(), self.y_slider.top_slider.value()


class collapsable_layout(QtWidgets.QFrame):
	def __init__(self, parent=None, title=None):
		QtWidgets.QFrame.__init__(self, parent=parent)

		self.is_collapsed = True
		self.title_frame = None
		self.content, self.content_layout = (None, None)

		self.vertical_layout = QtWidgets.QVBoxLayout()
		self.vertical_layout.addWidget(self.init_title_frame(title, self.is_collapsed))
		self.vertical_layout.addWidget(self.init_content(self.is_collapsed))

		self.init_collapsable()

		self.setLayout(self.vertical_layout)

	def init_title_frame(self, title, collapsed):
		self.title_frame = self.collapsable_title(title=title, collapsed=collapsed)
		return self.title_frame
	
	def init_content(self, collapsed):
		self.content = QtWidgets.QWidget()
		self.content_layout = QtWidgets.QVBoxLayout()

		self.content.setLayout(self.content_layout)
		self.content.setVisible(not collapsed)

		return self.content

	def addWidget(self, widget):
		self.content_layout.addWidget(widget)

	def init_collapsable(self):
		QtCore.QObject.connect(self.title_frame, QtCore.SIGNAL("clicked()"), self.toggle_collapsed)

	def toggle_collapsed(self):
		self.content.setVisible(self.is_collapsed)
		self.is_collapsed = not self.is_collapsed
		self.title_frame._icon.set_icon(int(self.is_collapsed))


	class collapsable_title(QtWidgets.QFrame):
		def __init__(self, parent=None, title="", collapsed=False):
			QtWidgets.QFrame.__init__(self, parent=parent)

			self.setMinimumHeight(24)
			self.move(QtCore.QPoint(24, 0))
			
			self.horizontal_layout = QtWidgets.QHBoxLayout()
			self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
			self.horizontal_layout.setSpacing(0)
			
			self.title = None
			self._icon = None

			self.horizontal_layout.addWidget(self.init_icon(collapsed))
			self.horizontal_layout.addWidget(self.init_title(title))

			self.setLayout(self.horizontal_layout)
					
		def init_title(self, title=None):
			self.title = QtWidgets.QLabel(title)
			self.title.setMinimumHeight(24)
			self.title.move(QtCore.QPoint(24, 0))			
			return self.title

		def init_icon(self, collapsed):
			self._icon = collapsable_layout.Icon(collapsed=collapsed)
			return self._icon
			
		def mousePressEvent(self, event):
			self.emit(QtCore.SIGNAL("clicked()"))
			return super(collapsable_layout.collapsable_title, self).mousePressEvent(event)

	class Icon(QtWidgets.QFrame):
		def __init__(self, parent=None, collapsed=False):
			QtWidgets.QFrame.__init__(self, parent=parent)

			self.setMaximumSize(24, 24)

			# horizontal == 0
			self._icon_horizontal = (QtCore.QPointF(7.0, 8.0), QtCore.QPointF(17.0, 8.0), QtCore.QPointF(12.0, 13.0))
			# vertical == 1
			self._icon_vertical = (QtCore.QPointF(8.0, 7.0), QtCore.QPointF(13.0, 12.0), QtCore.QPointF(8.0, 17.0))
			# icon
			self._icon = None
			self.set_icon(int(collapsed))
			
		def set_icon(self, icon_dir):
			if icon_dir:
				self._icon = self._icon_vertical
			else:
				self._icon = self._icon_horizontal

		def paintEvent(self, event):
			painter = QtGui.QPainter()
			painter.begin(self)
			painter.setBrush(QtGui.QColor(192, 192, 192))
			painter.setPen(QtGui.QColor(64, 64, 64))
			painter.drawPolygon(self._icon)
			painter.end()


class progress_bar(QtWidgets.QWidget):
	def __init__(self, max=100):
		super(progress_bar, self).__init__()

		self.max = max

		self.horizontal_layout = QtWidgets.QHBoxLayout()
		self.horizontal_layout.setContentsMargins(0, 8, 0, 0)

		self.progress_bar = QtWidgets.QProgressBar()
		self.progress_bar.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.progress_bar.setRange(0, self.max)
		self.progress_bar.setFixedHeight(8)
		self.progress_bar.setTextVisible(False)

		self.horizontal_layout.addWidget(self.progress_bar)

		self.setLayout(self.horizontal_layout)

	def update(self, percentage):
		progress_value = int(percentage * self.max)
		self.progress_bar.setValue(progress_value)


class editable_toolbar(QtWidgets.QTabBar):
	def __init__(self, parent):
		QtWidgets.QTabBar.__init__(self, parent)
		self._editor = QtWidgets.QLineEdit(self)
		self._editor.setWindowFlags(QtCore.Qt.Popup)
		self._editor.setFocusProxy(self)
		self._editor.editingFinished.connect(self.handle_editing_finished)
		self._editor.installEventFilter(self)

	def event_filter(self, widget, event):
		if ((event.type() == QtCore.QEvent.MouseButtonPress and not 
							 self._editor.geometry().contains(event.globalPos())) or 
							 (event.type() == QtCore.QEvent.KeyPress and 
							 event.key() == QtCore.Qt.Key_Escape)):
			self._editor.hide()
			return True
		return QtWidgets.QTabBar.eventFilter(self, widget, event)

	def mouseDoubleClickEvent(self, event):
		index = self.tabAt(event.pos())
		if index >= 0:
			self.edit_tab(index)

	def edit_tab(self, index):
		rect = self.tabRect(index)
		self._editor.setFixedSize(rect.size())
		self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
		self._editor.setText(self.tabText(index))
		if not self._editor.isVisible():
			self._editor.show()

	def handle_editing_finished(self):
		index = self.currentIndex()
		if index >= 0:
			self._editor.hide()
			self.setTabText(index, self._editor.text())


def icon_svg(name, size, svg_path=None):
	if svg_path is None:
		svg_path = str(Path(os.path.dirname(__file__), 'ui'))
	icon_path = os.path.abspath(os.path.join(svg_path, name + '.svg'))
	icon_path_hover = os.path.abspath(os.path.join(svg_path, name + '_hover.svg'))
	
	if not Path(icon_path_hover).is_file():
		icon_path_hover = icon_path    

	svgRenderer = QtSvg.QSvgRenderer(icon_path)
	svgRenderer_hover = QtSvg.QSvgRenderer(icon_path_hover)
	if svgRenderer.isValid():
		pixmap = QtGui.QPixmap(QtCore.QSize(size, size))
		pixmap_hover = QtGui.QPixmap(QtCore.QSize(size, size))

		if not pixmap.isNull():
			pixmap.fill(QtCore.Qt.transparent)
			painter = QtGui.QPainter(pixmap)
			svgRenderer.render(painter)
			painter.end()

			pixmap_hover.fill(QtCore.Qt.transparent)
			painter_hover = QtGui.QPainter(pixmap_hover)
			svgRenderer_hover.render(painter_hover)
			painter_hover.end()            

		icon = QtGui.QIcon()
		icon.addPixmap(pixmap)
		icon.addPixmap(pixmap_hover, QtGui.QIcon.Active)
		return icon

	return None


def stylesheet(name, path=None):
	if path is None:
		path = str(Path(os.path.dirname(__file__), 'qss'))
	stylesheet_path = os.path.abspath(os.path.join(path, name + '.qss'))
	qss_file = open(stylesheet_path).read()

	return qss_file


def simple_dialog(text):
	dialog = QtWidgets.QMessageBox()
	dialog.setText(text)
	dialog.setIcon(QtWidgets.QMessageBox.Warning)
	dialog.setStandardButtons(QtWidgets.QMessageBox.Yes)
	dialog.exec_()
