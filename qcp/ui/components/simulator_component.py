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
from qcp.ui.components import AbstractComponent, \
    ButtonComponent, GraphComponent
from qcp.ui.constants import LCD_CLASSICAL, LCD_GROVER
from qcp.matrices import Matrix
import qcp.algorithms as ga
import math


class SimulatorComponent(AbstractComponent):
    """
    UI Component that handles the background task of running the Quantum
    Computer Simulator code on a separate QThread.
    """

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 button_component: ButtonComponent,
                 graph_component: GraphComponent, *args, **kwargs):
        """
        Initialise the SimulatorComponent object, referencing the main window
        element, and the two UI components required for it to function.

        :param QtWidgets.QMainWindow main_window: The main window element of
            the UI.
        :param ButtonComponent button_component: The search input box of the
            UI
        :param GraphComponent graph_component: The target input box of the UI
        :param *args: variable length extra arguments to pass down
            to QtCore.QObject
        :param **kwargs: dictionary parameters to pass to QtCore.QObject
        """
        self.button_component = button_component
        self.graph_component = graph_component
        super().__init__(main_window, *args, **kwargs)

    def setup_signals(self):
        """
        Initialise the QThread to run the simulation on and have it ready
        to run when the input parameters are provided.

        Setup signals to display the graph when the calculation completes,
        and to hide the cancel button and progress bar.
        """
        super().setup_signals()

        self.qcp_thread = SimulateQuantumComputerThread()
        self.qcp_thread.simulation_result_signal.connect(
            self._simulation_results)

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

    def run_simulation(self, nqbits, target):
        """
        Pass the input parameters to the QThread, and start up the
        simulation
        """
        # Code to initialise the qcp simulation on the qthread
        # Pass the number of qbits and target bit over to the thread
        self.nqbits = nqbits
        self.qcp_thread.simulation_input_signal.emit(nqbits, target)

    @QtCore.Slot(Matrix)
    def _simulation_results(self, qregister):
        """
        Signal catcher to read in the simulation results from the
        QThread that it is calculated in.
        """
        self.graph_component.display(qregister)

        self.button_component.pb_thread.exiting = True

    def simulation_finished(self):
        """
        Function to handle behaviour when the QThread completes successfully

        Shows the quantum state on the matplotlib graph
        """
        self.graph_component.show()

    def update_lcd_displays(self):
        """
        Show the comparison between the number of iterations a classical
        computer would have needed to run the search, versus the number
        of iterations our quantum simulation took.
        """
        if not self.nqbits:
            return

        # TODO: Don't know if this reasoning makes sense...
        number_entries = math.log2(self.nqbits)
        classical_average = math.ceil(number_entries / 2)
        quantum_average = math.ceil(math.sqrt(number_entries))

        self.lcd_classical.display(classical_average)
        self.lcd_grover.display(quantum_average)


class SimulateQuantumComputerThread(QtCore.QThread):
    """
    QThread object to handle the running of the Quantum Computer
    Simulation, input/output is passed back to the main thread by pipes.
    """
    simulation_result_signal = QtCore.Signal(Matrix)
    simulation_input_signal = QtCore.Signal(int, int)

    def __init__(self, parent=None):
        """
        Setup the SimulateQuantumComputerThread QThread.
        """
        super().__init__(parent)
        self.simulation_input_signal.connect(self.input)
        self.exiting = False

    @QtCore.Slot(int, int)
    def input(self, qbits, target):
        if not self.isRunning():
            self.nqbits = qbits
            self.target = target
            self.exiting = False
            self.start()
        else:
            print("simulation already running!")

    def run(self):
        """
        Run the simulation
        """
        # TODO: Actual calculated results would be passed back here...
        grovers = ga.Grovers(self.nqbits, self.target)
        qregister = None
        try:
            qregister = grovers.run()
        except AssertionError as ae:
            print(ae)
        self.simulation_result_signal.emit(qregister)
        self.quit()
