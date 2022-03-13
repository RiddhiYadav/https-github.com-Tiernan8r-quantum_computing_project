# Copyright 2022 Tiernan8r
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from PySide6 import QtWidgets
from PySide6 import QtCore
import time
from qcp.ui.components import AbstractComponent
from qcp.ui.constants import THREAD_PAUSE, LCD_CLASSICAL, LCD_GROVER


class SimulatorComponent(AbstractComponent):

    def __init__(self, main_window: QtWidgets.QMainWindow, button_component,
                 graph_component, *args, **kwargs):
        self.button_component = button_component
        self.graph_component = graph_component
        super().__init__(main_window, *args, **kwargs)

        self.graph_component.hide()

    def setup_signals(self):
        self._find_widgets()
        self.qcp_thread = SimulateQuantumComputerThread()

        self.qcp_thread.finished.connect(self.update_lcd_displays)
        # Hide the cancel button if the calculation finishes
        self.qcp_thread.finished.connect(
            self.button_component.cancel_button.hide)

        self.qcp_thread.finished.connect(self.simulation_finished)

    def _find_widgets(self):
        lcds = self.main_window.ui_component.findChildren(QtWidgets.QLCDNumber)
        for lcd in lcds:
            if lcd.objectName() == LCD_CLASSICAL:
                self.lcd_classical = lcd
            elif lcd.objectName() == LCD_GROVER:
                self.lcd_grover = lcd

    def run_simulation(self):
        # Code to initialise the qcp simulation on the qthread
        if not self.qcp_thread.isRunning():
            self.qcp_thread.exiting = False
            self.qcp_thread.start()
            while not self.qcp_thread.isRunning():
                time.sleep(THREAD_PAUSE)

    def simulation_finished(self):
        self.graph_component.show()

    def update_lcd_displays(self):
        classical_value = self.lcd_classical.value()
        self.lcd_classical.display(classical_value + 1)

        quantum_value = self.lcd_grover.value()
        self.lcd_grover.display(quantum_value + 1)


class SimulateQuantumComputerThread(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def run(self):
        self.quit()