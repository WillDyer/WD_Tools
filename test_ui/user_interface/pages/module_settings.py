from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance

class CreateModuleTab(QWidget):
    def __init__(self, module, button, page, scroll_area_layout, layout):
        super().__init__()
        self.module = module
        self.button = button
        self.page = page
        self.scroll_area_layout = scroll_area_layout
        self.module_layout = layout

        self.settings_page = QWidget()
        self.settings_page.setObjectName("settings_page")
        self.settings_page.setStyleSheet(""" QWidget#settings_page { background-color: #25292c;} """)
        self.settings_layout = QFormLayout(self.settings_page)
        self.settings_layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)


        self.parent_joint_widget()
        self.ikfk_widget()
        self.orientation_widget()
        self.offset_widget()
        self.remove_module()

        checkbox = self.move_widget_dropdown()
        self.move_widget(checkbox)

        self.settings_page.hide()


    
    def parent_joint_widget(self):
        # parent joint
        parent_label = QLabel("Parent:")
        parent_combobox = QComboBox()
        parent_combobox.setObjectName(f"combobox_parent_{self.module}")
        parent_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.settings_layout.addRow(parent_label, parent_combobox)

    def ikfk_widget(self):
        # IKFK Default
        ikfk_label = QLabel("IKFK Default:")
        ikfk_combobox = QComboBox()
        ikfk_combobox.setObjectName(f"combobox_ikfk_{self.module}")
        ikfk_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.settings_layout.addRow(ikfk_label, ikfk_combobox)

    def orientation_widget(self):
        # Orientation
        orientation_label = QLabel("Orientation:")
        orientation_combobox = QComboBox()
        orientation_combobox.setObjectName(f"combobox_orientation_{self.module}")
        orientation_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        available_orientations = ["xyz","yzx","zxy"]
        orientation_combobox.addItems(available_orientations)
        index = available_orientations.index("xyz")
        orientation_combobox.setCurrentIndex(index)

        self.settings_layout.addRow(orientation_label, orientation_combobox)

    def offset_widget(self):
        # offset
        offset_label = QLabel("Offset:")
        offset_horizontal_layout = QHBoxLayout()
        for xyz in ["X","Y","Z"]:
            spin_box = QSpinBox()
            spin_box.setObjectName(f"spinbox_offset{xyz}_{self.module}")
            spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            offset_horizontal_layout.addWidget(spin_box)

        self.settings_layout.addRow(offset_label, offset_horizontal_layout)
    
    def remove_module(self):
        #remove module
        remove_module = QPushButton("Remove Module")
        remove_module.setObjectName(f"button_remove_{self.module}")

        self.settings_layout.addRow(remove_module)

    def move_widget_dropdown(self):
        # move widget settings
        checkbox = QCheckBox('Expand/Collapse')
        checkbox.setObjectName("checkbox")
        checkbox.setStyleSheet(""" QWidget#checkbox { background-color: #25292c;} """)

        self.settings_layout.addRow(checkbox)
        return checkbox

    def move_widget(self, checkbox):
        def move_widgets(page, button):
            page = page
            button = button

            def move_widget(updown):
                index = self.scroll_area_layout.indexOf(page)
                new_index = index + updown
                if new_index < 0 or new_index >= self.scroll_area_layout.count():
                    return
                self.scroll_area_layout.insertWidget(new_index, page)

            if "top" in button:
                self.scroll_area_layout.insertWidget(0,page)
            elif "up" in button:
                move_widget(-1)
            elif "down" in button:
                move_widget(1)

        def widget_settings(button, collapse_button, move_widget):
            if button.isChecked() and collapse_button.isChecked():
                move_widget.show()
            else:
                move_widget.hide()

        # move widget
        move_widget = QWidget()
        move_widget.setObjectName("move_widget")
        move_widget.setStyleSheet(""" QWidget#move_widget { background-color: #25292c;} """)
        move_widget_layout = QHBoxLayout(move_widget)
        move_list = []
        #for move in ["Move Up","Move Down","To Top"]:
        moveup_button = QPushButton("move_up")
        move_widget_layout.addWidget(moveup_button)
        movedown_button = QPushButton("move_down")
        move_widget_layout.addWidget(movedown_button)
        movetop_button = QPushButton("to_top")
        move_widget_layout.addWidget(movetop_button)

        
        QObject.connect(moveup_button, SIGNAL("clicked()"), lambda: move_widgets(self.page, button="up"))
        QObject.connect(movedown_button, SIGNAL("clicked()"), lambda: move_widgets(self.page, button="down"))
        QObject.connect(movetop_button, SIGNAL("clicked()"), lambda: move_widgets(self.page, button="top"))

        move_widget.hide()
        QObject.connect(checkbox, SIGNAL("clicked()"), lambda: widget_settings(self.button, checkbox, move_widget))


        # add to the settings_layout
        self.settings_layout.addRow(move_widget)

        self.module_layout.addWidget(self.settings_page)
        QObject.connect(self.button, SIGNAL("clicked()"), lambda: self.drop_downs(self.settings_page))

    def drop_downs(self, settings_page):
        width = self.page.size().width()

        if self.button.isChecked():
            settings_page.show()
        else:
            settings_page.hide()