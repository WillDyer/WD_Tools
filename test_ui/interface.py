import maya.cmds as cmds
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance
import importlib
import os.path

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_interface.pages import module_settings, sidebar, page_utils

importlib.reload(module_settings)
importlib.reload(sidebar)
importlib.reload(page_utils)

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(Interface,self).__init__(*args, **kwargs)
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)
        self.initUI()
        self.setFixedWidth(600)
        self.setFixedHeight(700)
        self.setWindowTitle("Maya_Modular_Rigging")

    def initUI(self):
        # layout
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Main layout
        self.main_layout_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_layout_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setStretch(1,100)
        self.vertical_layout.addWidget(self.main_layout_widget)

        # Rig Progress
        rig_progress_instance = page_utils.RigProgression(self.vertical_layout)

        # sidebar for modules
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMaximumWidth(100)
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.sidebar_layout.setSpacing(2)
        add_available_modules_instance = sidebar.AddAvailableModules(self, self.sidebar_layout)
        rig_name_instance = sidebar.RigNameWidget(self.sidebar_layout)
        colour_widget_instance = sidebar.RigColourWidget(self.sidebar_layout)
        self.main_layout.addWidget(self.sidebar_widget)

        # main settings area
        self.module_widget = QWidget()
        self.module_widget.setMaximumWidth(500)
        self.module_layout = QVBoxLayout(self.module_widget)
        self.module_layout.setSizeConstraint(QVBoxLayout.SetMaximumSize)
        self.init_mainsettings()
        self.main_layout.addWidget(self.module_widget)

        # set stylesheet
        stylesheet_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"user_interface","style","style.css")
        with open(stylesheet_path, "r") as file:
            stylesheet = file.read()
        self.setStyleSheet(stylesheet)

        # set ui icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"interface","images","UI_Logo.png")
        self.setWindowIcon(QIcon(icon_path))

    def init_mainsettings(self):
        settings_label = QLabel("SETTINGS:")
        settings_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 20px;
            }
        """)
        self.module_layout.addWidget(settings_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        container_widget = QWidget()
        
        # Ensure the container widget expands horizontally
        container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.scroll_area_layout = QVBoxLayout(container_widget)
        self.scroll_area_layout.setSpacing(5)
        
        # Remove margins and align to top left
        self.scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_area.setWidget(container_widget)
        self.scroll_area.setWidgetResizable(True)
        self.module_layout.addWidget(self.scroll_area)
        
    def module_buttons(self, module):
        print(f'Button clicked: {module}')
        page = QWidget()
        page.setObjectName("parenWidget")
        page.setStyleSheet(""" QWidget#parenWidget { background-color: #25292c; } """)
        layout = QVBoxLayout(page)
        button = QPushButton(module)
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(button)

        settings_page_instance = module_settings.CreateModuleTab(module, button, page, self.scroll_area_layout, layout)

        self.scroll_area_layout.insertWidget(0,page)


def main():
    ui = Interface()
    ui.show()
    return ui
