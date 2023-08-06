import enum
import os
import sys
import webbrowser
from typing import Dict

import logging

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QResizeEvent, QFont
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QLabel, QSizeGrip

import DocGenLogic as docGen
import form
import ColorThemes

class MessageType(enum.Enum):
    Error = 0
    Success = 1
    Notification = 2


class MainWindow(QtWidgets.QWidget):
    line_edit_vs_label: Dict[QLineEdit, QLabel]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the log and create self.logger:
        self.logger = Logger.init_logger('Omnicon.DDSDocGen')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s: %(name)s: %(funcName)s: %(message)s')
        # file_handler = logging.FileHandler('DocGen_log.log')
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)



        self.separator = "; "

        # Connect to UI code (automatically generated from designer)
        self.ui = form.Ui_docGen()
        self.ui.setupUi(self)

        # Hide windows title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Map lineEdits to their respective labels (for easy access from button handlers and such)
        self.line_edit_vs_label = {
            self.ui.type_lineEdit: self.ui.type_label,
            self.ui.topics_lineEdit: self.ui.topics_label,
            self.ui.output_file_name_lineEdit: self.ui.output_label,
        }
        # self.dark_light_toggle = AnimatedToggle(
        #     checked_color="#FFB000",
        #     pulse_checked_color="#44FFB000"
        # )

        self.ui.toggle_dark_or_light.stateChanged.connect(self.set_dark_mode)
        self.light_logo = QtGui.QIcon('../../icons/Logo.ico')
        self.dark_logo = QtGui.QIcon('../../icons/DARK.png')

        # Set the dark mode and light mode title bar icons
        self.minimize_icon_for_dark = QtGui.QIcon('../../icons/minimize_dark.png')
        self.maximize_icon_for_dark = QtGui.QIcon('../../icons/maximize_dark.png')
        self.restore_icon_for_dark = QtGui.QIcon('../../icons/restore_dark.png')
        self.close_icon_for_dark = QtGui.QIcon('../../icons/close_dark2.png')
        self.minimize_icon_for_light = QtGui.QIcon('../../icons/minimize.png')
        self.maximize_icon_for_light = QtGui.QIcon('../../icons/maximize.png')
        self.restore_icon_for_light = QtGui.QIcon('../../icons/restore.png')
        self.close_icon_for_light = QtGui.QIcon('../../icons/close.png')

        self.is_window_maximized = False

        self.ui.minimize_window_btn.setIcon(self.minimize_icon_for_dark)
        self.put_the_right_icon_in_maximize_window_button()
        self.ui.btn_close_window.setIcon(self.close_icon_for_dark)

        self.ui.btn_close_window.setStyleSheet('QPushButton:hover {background: red;}')

        # close_win = QStyle.SP_TitleBarCloseButton
        # self.close_win_icon = self.style().standardIcon(close_win)
        #
        # self.ui.btn_close_window.setIcon(self.close_win_icon)

        # self.ui.omnicon_logo.setPixmap(self.light_logo)

        # Set the text colors for the current color theme: current is dark mode
        self.regular_text_color : str = "white"
        self.warning_text_color : str = "red"
        self.success_text_color : str = "rgb(0, 255, 0)"  # green

        self.ui.output_file_name_lineEdit.setText(os.getcwd() + '\ICD.docx')

        # Connect button clicked events to respective function
        self.ui.run_generator_btn.clicked.connect(self.handle_run_generator_click)
        self.ui.type_btn.clicked.connect(self.handle_browse_directory_button)
        self.ui.topics_btn.clicked.connect(self.handle_browse_topic_names_xml_button)
        self.ui.output_directory_btn.clicked.connect(self.handle_browse_output_directory_button)

        self.ui.btn_close_window.clicked.connect(app.quit)
        self.ui.minimize_window_btn.clicked.connect(self.showMinimized)
        self.ui.maximize_window_btn.clicked.connect(self.handle_maximize_btn_push)

        self.ui.omnicon_logo.clicked.connect(self.open_omnicon_website)

        # Allow moving the window around
        self.ui.title_bar_frame.mouseMoveEvent = self.moveWindow

        self.small_labels_list = [
            self.ui.type_label,
            self.ui.topics_label,
            self.ui.output_label,
            self.ui.notification_label,
        ]

        self.line_edit_list = [
            self.ui.type_lineEdit,
            self.ui.topics_lineEdit,
            self.ui.output_file_name_lineEdit,
        ]

        self.folder_icon_btns_list = [
            self.ui.type_btn,
            self.ui.topics_btn,
            self.ui.output_directory_btn,
        ]

        # # SET DROPSHADOW WINDOW
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(20)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 100))
        #
        # # APPLY DROPSHADOW TO FRAME
        # self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)

        self.sizegrip = QSizeGrip(self.ui.resize_frame)
        self.sizegrip.setStyleSheet(
            "QSizeGrip { width: 20px; height: 20px;  }")
        self.sizegrip.setToolTip("Resize Window")

        # Hide progress bar
        self.ui.progressBar.hide()

        self.update_progress_bar_function = self.update_progress_bar

        print(self.light_logo)


    """
    ###############################################   Button handlers   ###############################################
    """

    def handle_run_generator_click(self) -> None:
        """
        This function is called when the button is pushed.
        The event that triggered the calling of this function is 'Run generator' button push.
        """
        self.set_dark_mode()
        # The entry dictionary holds the names of tha labels as s key and the corresponding entry as a value:
        self.logger.debug("User clicked the Run generator button")

        # Check the inputs:
        try:
            self.check_multiple_files_lineEdit(self.ui.type_lineEdit)
            self.check_file_lineEdit(self.ui.topics_lineEdit)
            self.check_output_file_name(self.ui.output_file_name_lineEdit)

        # Handle exceptions:
        except Exception as error:
            # Display error message to the user
            self.write_to_notification_label(MessageType.Error, str(error))
            return

        #  initially use these inputs:
        #  /OmniCon_GenericDDSEngine_Config.xml
        #  ConfigurationFiles/

        # Display "in progress" message
        self.write_to_notification_label(MessageType.Notification, "Document generation in progress...")
        # Re-display the progress bar
        self.ui.progressBar.show()
        try:
            document_generator = docGen.DocumentGenerator()
            document_generator.run_doc_gen(
                self.ui.type_lineEdit.text(),
                self.ui.topics_lineEdit.text(),
                self.ui.output_file_name_lineEdit.text(),
                self.update_progress_bar_function
            )

        except Exception as err:
            if err.args[0] == "some_types_not_ok":
                self.write_to_notification_label(
                    MessageType.Notification, "ICD was created with issues; Check DocGen_log for more information.")
            else:
                self.logger.debug(Exception, err)
                self.write_to_notification_label(MessageType.Error, str(err))
            self.ui.progressBar.hide()

        else:
            # When all went well, display a success message
            self.logger.info("ICD document was generated successfully.")
            self.ui.progressBar.hide()
            self.write_to_notification_label(MessageType.Success, "ICD document was successfully generated!")

    def handle_browse_directory_button(self) -> None:
        """
        This function is called when the browse directory button is pushed
        :return: N/A
        """
        # Read whatever is in the entry into file_directory
        file_directory = self.ui.type_lineEdit.text()
        if file_directory != "":
            # When there is something in the input_pointer, add " , " (a separator):
            file_directory += self.separator

        user_input, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "XML files (*.xml) ;; All Files (*)")
        # See if the user selected a file:
        if user_input == "":
            # When the user did not select anything, do not change the entry:
            return
        else:
            # When the user did select a file, add it into the end of the existing string.
            file_directory += user_input

        # Now that we have what's in the entry we can clear the it:
        self.ui.type_lineEdit.clear()
        # Write the concatenated file names into the entry.
        self.ui.type_lineEdit.setText(file_directory)

    def handle_browse_topic_names_xml_button(self) -> None:
        """
        This function is called when the browse topic names xml button is pushed
        :return: N/A
        """
        topic_names_xml_filename, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "XML files (*.xml) ;; All Files (*)")
        # Check if a file was selected:
        if topic_names_xml_filename != "":
            # When a file was selected, remove the old entry before adding the one chosen by the user.
            self.ui.topics_lineEdit.clear()

        # Add input_pointer to line edit:
        self.ui.topics_lineEdit.setText(topic_names_xml_filename)

    def handle_browse_output_directory_button(self) -> None:
        """
        This function is called when the browse directory button is pushed
        :return: N/A
        """
        # file_directory = filedialog.askdirectory(mustexist=True)
        output_file_name_tuple = QFileDialog.getSaveFileName(self, "Save File", "E:\\", ("MS Word (*.docx)"))
        output_file_name = output_file_name_tuple[0]
        # Handle the case where the user chooses to cancel ( the input will be ""):
        if output_file_name == "":
            return

        if output_file_name != "":
            # delete the existing string from the entry to clear the way for the new entry
            self.ui.output_file_name_lineEdit.clear()
        self.ui.output_file_name_lineEdit.setText(output_file_name)

    """
    ###############################################  Utility functions  ###############################################
    """

    def check_multiple_files_lineEdit(self, input_pointer: QLineEdit) -> bool:
        """
        This function checks the user input. first figures out if the input is in the form of multiple files
        :param input_pointer: The QLineEdit that need to be checked
        :return: boolean. True = ok, False = bad input.
        """
        if input_pointer.text() == "":
            # When it's empty, display an error message:
            input_pointer.selectAll()
            self.highlight_entry(input_pointer)
            raise Exception("Error! Highlighted field is empty!")

        # file name will end up as a list:
        final_input = input_pointer.text().split(self.separator)
        # Go over the list of file names and check them all
        for file_name in final_input:
            if not os.path.exists(file_name):
                self.highlight_entry(input_pointer)
                raise Exception("Error! The file/folder: " + file_name + " does not exist!")
        return True

    def check_file_lineEdit(self, input_pointer: QLineEdit) -> bool:
        """
        This function checks the file input_pointer from the entry provided as a parameter then returns a
        boolean: True for a valid input_pointer or False for an invalid input_pointer.
        :return: boolean.
        """
        # entry is optional so no need to check if entry is empty
        if input_pointer.text() == "":
            return True

        if not os.path.exists(input_pointer.text()):
            self.highlight_entry(input_pointer)
            raise Exception("Error! file: " + input_pointer.text() + " does not exist!")

        return True

    def check_output_file_name(self, entry_name: QLineEdit) -> bool:
        """
        Thi function checks a folder input_pointer from the entry provided as a parameter.
        :param entry_name: an entry name used which is the key in  user_input_dictionary. The value is the user input_pointer.
        :return: boolean
        """
        output_file_name = entry_name.text()
        if output_file_name == "":
            return True
        # # See if the user gave the '.docx' extension to his choice
        # if not output_file_name.endswith('.docx'):
        #     # When the '.docx' extension wasn't at the end of the string: fix it and let the user know about it.
        #     self.write_to_notification_label\
        #         (MessageType.Notification,
        #          "Provided output file name doesn't have the '.docx' extension. Added it automatically")
        #     entry_name.setText(output_file_name + '.docx')
        #     # Make sure the message is displayed by refreshing the window
        #     QtWidgets.QApplication.processEvents()
        #     # Sleep to make sure the user has time to see the message
        #     sleep(3)
        return True


    def highlight_entry(self, input_pointer: QLineEdit) -> None:
        """
        This function highlights the given entry
        :param input_pointer:
        :return: N/A
        """
        self.line_edit_vs_label[input_pointer].setStyleSheet("color: red")
        input_pointer.setFocus()
        # Have the highlight removed when text is changed in that entry
        input_pointer.textChanged.connect(lambda: self.stop_entry_highlight(input_pointer))

    def stop_entry_highlight(self, input_pointer):
        self.line_edit_vs_label[input_pointer].setStyleSheet("color: " + self.regular_text_color)
        input_pointer.disconnect()


    def write_to_notification_label(self, message_type: MessageType, message_text: str) -> None:
        """
        This function writes a text (given as the 'message_text' parameter) to the notification label
        (that is displayed to the user). The text is displayed with color coding: green - success message,
        black - notification message and red -  error message. The function determines the color using the
        'message_type' parameter.
        :param message_type: Helps the function to determine what font color is to be used. The valid Enum values are:
                            "Error", "Success" and "Notification".
        :param message_text: The message to display for the user.
        :return: N/A
        """
        text_color: str = self.regular_text_color
        if message_type == MessageType.Error:
            text_color = self.warning_text_color
        elif message_type == MessageType.Success:
            text_color = self.success_text_color

        self.ui.notification_label.setStyleSheet("QLabel { color : " + text_color + " }")
        self.ui.notification_label.setText(message_text)

    def handle_maximize_btn_push(self):
        """
        This function handles the maximize button push
        :return: None
        """
        if not self.is_window_maximized:
            self.showMaximized()
        else:
            self.showNormal()
        self.is_window_maximized = not self.is_window_maximized
        # Set the right icon:
        self.put_the_right_icon_in_maximize_window_button()

    def put_the_right_icon_in_maximize_window_button(self):
        """
        This function determines and sets the right maximize button icon for any state (dark/light, maximized/normal)
        :return: None
        """
        # See whether we are in dark mode or light mode
        if self.ui.toggle_dark_or_light.isChecked():
            # When in light mode:
            if self.is_window_maximized:
                # When window is maximized
                self.ui.maximize_window_btn.setIcon(self.restore_icon_for_light)

            else:
                # When window is not maximized
                self.ui.maximize_window_btn.setIcon(self.maximize_icon_for_light)
        else:
            # When it's dark mode:
            if self.is_window_maximized:
                # When window is maximized
                self.ui.maximize_window_btn.setIcon(self.restore_icon_for_dark)

            else:
                # When window is not maximized
                self.ui.maximize_window_btn.setIcon(self.maximize_icon_for_dark)


    def update_progress_bar(self, num_of_chapters: int, iteration_number: int) -> None:
        """
        This function updates the progress bar (if supplied by the developer)
        :param num_of_chapters: The total number of chapters to go over
        :param iteration_number: The indication of how many chapters are done with so far
        :return: N/A
        """
        # func(iteration_number / num_of_chapters)

        self.ui.progressBar.setValue((iteration_number / num_of_chapters) * 100)

    def set_light_mode(self):
        #Change the pallette to light mode:
        ColorThemes.set_light_mode(self)

        # Set the notification text colors for light mode theme:
        self.regular_text_color: str = "black"
        self.warning_text_color: str = "red"
        self.success_text_color: str = "green"
        print("light")

    def set_dark_mode(self):
        #Change the pallette to light mode:
        if self.ui.toggle_dark_or_light.isChecked():
            ColorThemes.set_light_mode(self)

            # Set the title bar icons to light mode icons
            self.ui.minimize_window_btn.setIcon(self.minimize_icon_for_light)
            self.put_the_right_icon_in_maximize_window_button()
            self.ui.btn_close_window.setIcon(self.close_icon_for_light)
        else:
            ColorThemes.set_dark_mode(self)
            # Set the title bar icons to dark mode icons
            self.ui.minimize_window_btn.setIcon(self.minimize_icon_for_dark)
            self.put_the_right_icon_in_maximize_window_button()
            self.ui.btn_close_window.setIcon(self.close_icon_for_dark)

        # Set the notification text colors for light mode theme:
        self.regular_text_color: str = "white"
        self.warning_text_color: str = "red"
        self.success_text_color: str = "rgb(0, 255, 0)" #green

    def mousePressEvent(self, event):
        # Get the offset from the cursor position to the top left corner of the app:
        self.offset = event.pos()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Window resize event: In addition to resizing the window itself, resize the fonts of anything important -
        could be a button, labels or lineEdits.
        :param event: the resize event
        :return: None
        """
        super().resizeEvent(event)
        # Resize button font size:
        self.set_font_size(self.ui.run_generator_btn, 40)
        # Resize regular size labels:
        for label_to_resize in self.small_labels_list:
            self.set_font_size(label_to_resize, 40)
        # Resize the headline label
        self.set_font_size(self.ui.Headline_label, 30)
        # Resize the tiny dark/light labels
        self.set_font_size(self.ui.label_dark, 50)
        self.set_font_size(self.ui.label_light, 50)
        # Resize the QLineEdits font:
        for line_edit in self.line_edit_list:
            self.set_font_size(line_edit, 55)

        for folder_icon_btn in self.folder_icon_btns_list:
            self.set_icon_size(folder_icon_btn, 14)


        width = self.geometry().width()
        height = self.geometry().height()
        # Determine the font size
        icon_axis_size = min(height, width) // 15
        # self.ui.omnicon_logo.setPresize(QSize(icon_axis_size, icon_axis_size))
        self.set_icon_size(self.ui.omnicon_logo, 14)

    def set_font_size(self, element_to_resize, resize_factor: int) -> None:
        """
        This function sets a new size to the given element. The calculation: min(height,width) / resize_factor. So,
         the bigger the resize factor, the smaller the font come out.
        :param element_to_resize: label / line edit / button that needs font size change
        :param resize_factor: int: Bigger resize factor results in smaller font size.
        :return: None
        """
        width = self.geometry().width()
        height = self.geometry().height()
        # Determine the font size
        font_size = min(height, width) // resize_factor
        element_to_resize.setFont(QFont('', font_size))

    def set_icon_size(self, element_to_resize, resize_factor: int) -> None:
        """
        This function sets a new icon size to the given element. The calculation: min(height,width) / resize_factor. So,
         the bigger the resize factor, the smaller the font come out.
        :param element_to_resize: label / line edit / button that needs font size change
        :param resize_factor: int: Bigger resize factor results in smaller font size.
        :return: None
        """
        width = self.geometry().width()
        height = self.geometry().height()
        # Determine the font size
        icon_axis_size = min(height, width) // resize_factor
        element_to_resize.setIconSize(QSize(icon_axis_size, icon_axis_size))


    # def mouseMoveEvent(self, event):
    #
    #     # Get the x and y global positions
    #     x = event.globalX()
    #     y = event.globalY()
    #     # Get the x and y of offset positions
    #     x_w = self.offset.x()
    #     y_w = self.offset.y()
    #     # Calculate the new position:
    #     self.move(x - x_w, y - y_w)
    #
    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     # Get current cursor position:
    #     self.clickedPosition = event.globalPos()

    def moveWindow(self, event):

        # Check if the window is at normal size:
        if self.is_window_maximized == False:
            # If it's a left mouse button click
            if event.buttons() == Qt.LeftButton:
                # Get the x and y global positions
                x = event.globalX()
                y = event.globalY()
                # Get the x and y of offset positions
                x_w = self.offset.x()
                y_w = self.offset.y()
                # Calculate the new position:
                self.move(x - x_w, y - y_w)

            event.accept()

    def open_omnicon_website(self):
        webbrowser.open('http://www.omniconSystems.com')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec_()
