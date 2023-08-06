import shutil
import tempfile
import time
import types
from asyncio import sleep
from datetime import datetime
from typing import Dict, Any, List, Union, Tuple, Callable

from . import Utils
from Omnicon_GenericDDSEngine_Py import Omnicon_GenericDDSEngine_Py as Omnicon
import os

import xml.etree.ElementTree as ET

from .ErrorListHandler import ErrorListHandler, LogLevel

from . import Logger
from . import SingleChapterGenerator
# from LatexDocGen import LatexDocGen
from .DocxGen import DocxGen
from .DocGenInterface import DocGenInterface
from .PdfGen import PdfGen


def get_hash_of_template(verbose=0):
    import hashlib, os
    import traceback
    SHAhash = hashlib.md5()

    template_file = DocxGen.get_doc_template_path()
    if not os.path.exists(template_file):
        return -1

    try:
        if verbose == 1:
            print('Hashing file')
        # filepath = os.path.join(os.getcwd(), file_name)
        with open(template_file, 'rb') as f1:
            while 1:
                # Read file in as little chunks
                buf = f1.read()
                # remove carriage returns due to different file saving methods
                buf = buf.replace(b'\r', b'')
                if not buf:
                    break
                SHAhash.update(buf)

    except:
        # Print the stack traceback
        raise (traceback.print_exc())
    return SHAhash.hexdigest()


class DocumentGenerator:
    titles_to_indexes: Dict[str, int]
    header_titles: Tuple[str, str, str, str]
    basic_types: List[str]
    type_rename_dictionary: Dict[Union[str, Any], Union[str, Any]]
    engine: Any  # It's a GenericDDSEngine,
    # but for some reason OmniCon_GenericDDSEngine_PythonAPI is not read well by the IDE
    # document: Document
    doc_generator: DocGenInterface
    currTable: Any

    # table: Table
    # row_cells: List[_Row.cells]
    current_union_enum_vector: List[Any]
    level_of_Discriminator: int
    union_label_to_userComment_dictionary: Dict[str, str]
    name_of_previous_element: str
    is_all_types_ok: bool
    levels_skipped: List[int]

    def __init__(self, logging_verbosity) -> None:
        # :param logging_verbosity: The requested level of logging. Could be either 'CRITICAL','ERROR','WARNING',
        #                         'INFO' or 'DEBUG'. NOTE: This parameter is optional; Default is 'INFO'.
        self.single_chapter_generator = None
        factory_configuration = Omnicon.FactoryConfiguration()
        factory_configuration.loggerConfiguration.verbosity = Omnicon.LogSeverityLevel.info
        Omnicon.GenericDDSEngine.SetFactoryConfiguration(factory_configuration)

        self.logger = Logger.init_logger(__name__, logging_verbosity)

        self.check_artifacts_integrity()

        self.header_titles = ("Hierarchy", "Field", "Type", "Description/Metadata")
        # Create an automatic dictionary to link between indexes and column-titles
        self.titles_to_indexes = {}
        index = 0
        for title in self.header_titles:
            self.titles_to_indexes.update({title: index})
            index += 1

        self.basic_types = [
            "ENUMERATION", "BOOLEAN", "UINT_8", "INT_16", "UINT_16", "INT_32", "UINT_32", "INT_64", "UINT_64",
            "FLOAT_32", "FLOAT_64", "FLOAT_128", "CHAR_8", "CHAR_16", "CHAR_32"]

        self.type_rename_dictionary = {
            "ENUMERATION": "enum", "ARRAY": "array", "SEQUENCE": "sequence", "STRING": "string", "WSTRING": "wstring",
            "STRUCTURE": "struct", "UNION": "union", "BOOLEAN": "boolean", "UINT_8": "uint8", "INT_16": "int16",
            "UINT_16": "uint16", "INT_32": "int32", "UINT_32": "uint32", "INT_64": "int64", "UINT_64": "uint64",
            "FLOAT_32": "float32", "FLOAT_64": "float64", "FLOAT_128": "float128", "CHAR_8": "char8",
            "CHAR_16": "char16", "CHAR_32": "char32"}
        self.engine = None

        self.doc_generator = None

    @staticmethod
    def VERSION():
        return "2.0.1"

    def init_and_run_engine(self, input_files_and_dirs_list: list) -> None:
        """
        This creates an engine instance and performs init and run with the desired configurations.
        :param input_files_and_dirs_list: A string that holds the path of the folder that holds the input_pointer files
        """
        # Create an engine instance:
        self.engine = Omnicon.GenericDDSEngine()
        # Create an engine configuration object:
        engine_configuration = Omnicon.EngineConfiguration()

        # Set the parameters:
        # Go over the new list and append it into the configuration file path vector:
        for input_file in input_files_and_dirs_list:
            engine_configuration.ddsConfigurationFilesPath.append(input_file)
        # Perform the introspection:
        engine_configuration.engineOperationMode = \
            Omnicon.EngineOperationMode.TYPE_INTROSPECTION
        # init the engine:
        self.logger.debug("init engine...")
        is_engine_ok = self.engine.Init(engine_configuration)

        # Check if the init went well
        if is_engine_ok is False:
            error_message: str = "Error! Problem with engine configuration."
            self.logger.error(error_message)
            ErrorListHandler.add_entry(LogLevel.ERROR, error_message)
            raise Exception(error_message)

        self.logger.info("Engine was init successfully")
        # Run the engine:
        is_engine_ok = self.engine.Run()
        # Check if the init went well
        if is_engine_ok is False:
            error_message: str = "Failed to run the engine."
            self.logger.error(error_message)
            ErrorListHandler.add_entry(LogLevel.ERROR, error_message)
            raise Exception("Error! Engine run FAILED!")

    @staticmethod
    def order_topics_by_xml(topic_names_to_types_xml: str, alphabet_order_list: list):
        """
        This function returns a list of topic
        :param topic_names_to_types_xml:
        :param alphabet_order_list:
        :return:
        """
        topic_mapping_dict: dict = {}
        tree = ET.parse(topic_names_to_types_xml)
        root = tree.getroot()
        for topic in root.findall('domain_library/domain/topic'):
            topic_name = topic.get('name')
            dds_type = topic.get('register_type_ref')
            if topic_name in alphabet_order_list:
                topic_mapping_dict[topic_name] = dds_type

        return topic_mapping_dict

    def generate_topic_based_icd(self, topic_names_to_types_xml: str,
                                 order_alphabetically: int) -> List[str]:
        """
        This function generates an ICD with topics as chapters.
        :param topic_names_to_types_xml:  The topic names to types xml file name.
        :param update_progress_bar_function: a 'pointer' to the function that updates the progress bar.
        :return: a list of all topics that had errors while processing

        """
        self.logger.debug("Using topics as chapter headers.")
        # Get the topic to type map:
        DDSTopicToTypeXMLMapping = Omnicon.GenericDDSEngine.GetTopicNameToTypeNameMap(topic_names_to_types_xml)

        if bool(DDSTopicToTypeXMLMapping) is False:
            self.logger.error("DDS topics-to-types XML mapping file is invalid: %s ", topic_names_to_types_xml)
            raise Exception("Invalid DDS topics-to-types XML mapping file!")

        if order_alphabetically == False:
            # When the user requested the topic order to be as it is in the xml file:
            DDSTopicToTypeXMLMapping = self.order_topics_by_xml(topic_names_to_types_xml, DDSTopicToTypeXMLMapping)
        # A flag that holds TRUE (when at least one chapter (type) was written. False when no chapter was written):
        is_at_least_one_type_ok: bool = False
        # Run the introspection for each data type:
        iteration_number: int = 1
        num_of_chapters: int = len(DDSTopicToTypeXMLMapping.keys())
        self.calculate_total_work_for_progress_bar(num_of_chapters)

        for topic, DDS_type in DDSTopicToTypeXMLMapping.items():
            self.update_progress_bar(iteration_number)
            iteration_number += 1
            # Generate a new chapter for that topic / type:
            try:
                self.single_chapter_generator.generate_single_chapter(topic, DDS_type)
            except Exception as e:
                self.logger.error(Exception, e)
                # Signal that there is an issue with one of the types.
                error_message: str = 'Failed to parse topic' + topic + ' . Error : ' + str(e)
                self.logger.error(error_message)
                ErrorListHandler.add_entry(LogLevel.ERROR, error_message)
                self.is_all_types_ok = False
            else:
                # When writing a chapter went well
                is_at_least_one_type_ok = True

        self.logger.debug("generate_topic_based_icd has finished going over the topics")

        if is_at_least_one_type_ok is False:
            self.logger.error("No DDS-type was found in the provided files/folders.")
            raise Exception("Could not find any DDS-type in provided files/folders!")


    @staticmethod
    def get_type_name(DDS_type):
        """
        This function is used by the sort() function; The returned value is used as a key for sorting alphabetically
        :param DDS_type: An element from the list received from GetTypesBasicInfo,
        :return:
        """
        return DDS_type.fullName

    def calculate_total_work_for_progress_bar(self, num_of_chapters):
        """
        This function determines the numbers that would be used to calculate the progress (for the progress bar)
        :param num_of_chapters: The total number of chapters from the given XML
        :return:
        """
        self.num_of_chapters = num_of_chapters
        self.work_per_format = num_of_chapters +  int(num_of_chapters / 5)
        self.total_work_to_do = self.total_num_of_formats * self.work_per_format

    def update_progress_bar(self, iteration_number: int):
        """
        This function updates the progress bar by calling the function provided by the user, taking into
        consideration the total num of  formats required by the user, the current iteration within the format currently
         under work, and adding 10% to the total work required for file saving overhead.
        :param iteration_number: The iteration number - where are we in terms of progress
        :return: None
        """
        if self.update_external_progress_bar_function is not None:
            current_iteration = iteration_number + (self.work_per_format * (self.current_format_num -1))
            state_txt = f"{ErrorListHandler.get_current_module().lower()}_parse"
            self.update_external_progress_bar_function(self.total_work_to_do ,current_iteration, state_txt)

    def update_progress_save(self):
        """
        This function updates the progress bar by calling the function provided by the user, letting him know now we
        are saving a file and that might take a while.
        :return: None
        """

        current_progress = (self.current_format_num - 1) * self.work_per_format + self.num_of_chapters
        state_txt = f"{ErrorListHandler.get_current_module().lower()}_save"
        self.update_external_progress_bar_function(self.total_work_to_do,current_progress, state_txt)

    def generate_type_based_ICD(self, order_alphabetically) -> List[str]:
        """
        This function generates an ICD with non-nested types as chapters.
        :param update_progress_bar_function: A function that updates the progress bar.
        """
        self.logger.debug("Topic-to-types XML file was not found. Using DDS type names as chapter headers.")
        # Use the engine's API to get a list of all available types:
        DDS_type_list = self.engine.GetTypesBasicInfo()

        if order_alphabetically:
            # When the user requested the chapters ordered alphabetically
            DDS_type_list.sort(key=self.get_type_name)
        list_of_errors: List[str] = []

        if not DDS_type_list:
            self.logger.error("DDS type files are invalid")
            raise Exception("Error! Invalid DDS type files!")
        # A flag that holds TRUE (when at least one chapter (type) was written. False when no chapter was written):
        is_at_least_one_type_ok: bool = False
        iteration_number: int = 1
        num_of_chapters: int = len(DDS_type_list)
        self.calculate_total_work_for_progress_bar(num_of_chapters)

        for DDS_type in DDS_type_list:
            self.update_progress_bar(iteration_number)
            iteration_number += 1
            if DDS_type.isNested is False:
                # Add a chapter only when the type is not a nested one:
                try:
                    self.single_chapter_generator.generate_single_chapter("", DDS_type.fullName)
                except Exception as err:
                    # Signal that there is an issue with one of the types.
                    list_of_errors.append(err)
                    self.is_all_types_ok = False
                else:
                    # When writing a chapter went well
                    is_at_least_one_type_ok = True
        if is_at_least_one_type_ok is False:
            raise Exception("Could not find any DDS-type in provided files/folders!")

        return list_of_errors

    def check_input_types(self,
                          input_files_and_dirs_list: list,
                          output_file_name: str,
                          title: str,
                          version: str,
                          topic_names_to_types_xml_path: str,
                          output_folder: str,
                          update_progress_bar_function: Callable[[], Any],
                          output_formats: list):
        if type(input_files_and_dirs_list) != list:
            error_message: str = f"Invalid input! Parameter <input_files_and_dirs_list>: '{input_files_and_dirs_list}' is: " \
                                 f"{type(input_files_and_dirs_list)}. Should be of class 'list'."
            raise Exception(error_message)

        if type(output_file_name) != str:
            error_message: str = f"Invalid input! Parameter Parameter <output_file_name>: '{output_file_name}' is: " \
                                 f"{type(output_file_name)}. Should be of class 'string'."
            raise Exception(error_message)

        if type(title) != str:
            error_message: str = f"Invalid input! Parameter <title>: '{title}' is: " \
                                 f"{type(title)}. Should be of class 'string'."
            raise Exception(error_message)

        if type(version) != str:
            error_message: str = f"Invalid input! Parameter <version> '{version}' is: " \
                                 f"{type(version)}. Should be of class 'string'."
            raise Exception(error_message)

        if type(topic_names_to_types_xml_path) != str:
            error_message: str = f"Invalid input! Parameter <topic_names_to_types_xml_path>: " \
                                 f"'{topic_names_to_types_xml_path}' is: " \
                                 f"{type(topic_names_to_types_xml_path)}. Should be of class 'string'."
            raise Exception(error_message)

        if type(output_folder) != str:
            error_message: str = f"Invalid input! Parameter <output_folder> '{output_folder}' is: " \
                                 f"{type(output_folder)}. Should be of class 'string'."
            raise Exception(error_message)

        if type(output_formats) != list:
            error_message: str = f"Invalid input! Parameter <output_formats> '{output_formats}' is: " \
                                 f"{type(output_formats)}. Should be of class 'list'."
            raise Exception(error_message)

        if update_progress_bar_function != None:
            if not isinstance(update_progress_bar_function, types.FunctionType):
                error_message: str = f"Invalid input! Parameter <update_progress_bar_function> " \
                                     f"'{update_progress_bar_function}' is: " \
                                     f"{type(update_progress_bar_function)}. Should be of class 'function'."
                raise Exception(error_message)
    def check_output_format_list(self, output_format_list):
        error_message: str
        example_message: str = "Please add a list of requested formats. For example: ['pdf']. " \
                               "Another example: ['docx', 'pdf']."
        if output_format_list == None:
            error_message = f"Invalid input! Parameter <output_format> is 'None'. {example_message}"
            raise Exception(error_message)
        if len(output_format_list) == 0:
            error_message = f"Invalid input! Parameter <output_format> is an empty list.{example_message}"
            raise Exception(error_message)

    def check_path(self, output_folder: str):
        if not os.path.exists(os.path.join(os.getcwd(), output_folder)):
            error_message = f"Selected output folder '{output_folder}' does not exist. " \
                            f"Please create the folder or choose an existing one."
            raise Exception(error_message)

    @staticmethod
    def check_type_files_not_empty(input_files_and_dirs_list: list):
        # Check if the list is empty
        if input_files_and_dirs_list == None:
            error_message = f"input_files_and_dirs_list is None. Cannot create an ICD without type file(s) or" \
                            f" a folder that contains at least one."
            raise Exception(error_message)

        # Check if the list is empty
        if len(input_files_and_dirs_list) == 0:
            error_message = f"input_files_and_dirs_list is empty. Cannot create an ICD without type file(s) or" \
                            f" a folder that contains at least one"
            raise Exception(error_message)

    def check_input(self,
                    input_files_and_dirs_list: list,
                    output_file_name: str,
                    title: str,
                    version: str,
                    topic_names_to_types_xml_path: str,
                    output_folder: str,
                    update_progress_bar_function: Callable[[], Any],
                    output_formats: list):
        """
        This function checks several aspects of the input. IF there is an issue, an exception is thrown.
        """
        self.check_input_types(input_files_and_dirs_list, output_file_name, title, version,
                               topic_names_to_types_xml_path,
                               output_folder, update_progress_bar_function, output_formats)

        self.check_output_format_list(output_formats)

        # check if output folder even exists
        self.check_path(output_folder)  # SEE NOTE BElOW
        # NOTE: Since there is a list of requested type files, we check (for each type file) if the output file
        # is open at a later stage, when calling that type file's docGen's init method (for example, in the case
        # of a PDF, the test happens in LatexDocGen.__init__)

        self.check_type_files_not_empty(input_files_and_dirs_list)

    def save_file_to_requested_folder(self,
                                      output_file_name: str, output_folder: str, temp_folder: str, output_type: str):
        """
        This function copies the requested file from the temp location to the requested location.
        :param output_file_name: Requested file name
        :param output_folder: Requested output folder
        :param temp_folder: The temp folder where the requested file was created
        :param output_type: The requested file extension ('pdf'/'docx'/etc...)
        """
        output_file_name = f'{output_file_name}.{output_type}'
        temp_output_path = os.path.join(temp_folder, output_file_name)
        if output_folder == "":
            output_folder = os.getcwd()
        full_requested_path = os.path.join(output_folder, output_file_name)
        self.logger.info(f"Generating {output_file_name}")

        # Copy the file into the requested folder:
        try:
            self.logger.debug(f"saving {output_file_name} into {output_folder}")
            shutil.copyfile(temp_output_path, full_requested_path)
            info_text = f"File saved successfully into '{full_requested_path}'"
            self.logger.info(info_text)
            # ErrorListHandler.add_entry(LogLevel.INFO, info_text)

        except Exception as err:
            message = f"Could not save '{full_requested_path}'. " \
                      f"Please check you have writing permissions at requested target folder."
            self.logger.error(message, exc_info=True)
            raise Exception(message)

    def check_artifacts_integrity(self):
        self.logger.debug("check_artifacts_integrity")
        # print(get_hash_of_dirs("images"))
        if not get_hash_of_template() == '03cbb7de956d74ec7da76a7b2dec7040':
            self.logger.fatal("DocGen resource 'Template.Docx' was modified. Cannot start DocGen")
            exit()

    def run_engine_and_generate_ICD(self,
                                    dds_types_files: list,
                                    dds_topics_types_mapping: str,
                                    output_file_name: str,
                                    title: str,
                                    version: str,
                                    order_alphabetically: bool,
                                    output_folder: str,
                                    output_formats:[list],
                                    update_progress_bar_function: Callable[[], Any]) -> List[str]:

        self.update_external_progress_bar_function = update_progress_bar_function
        self.total_num_of_formats = len(output_formats)

        self.is_all_types_ok = True  # An indicator that helps to know whether all types went well

        self.init_and_run_engine(dds_types_files)

        now: datetime = datetime.now()
        date_time_string: str = now.strftime("%d/%m/%Y %H:%M:%S")

        # Two variables to know which status to give the user at the end.
        is_at_least_one_file_created = False
        is_at_least_one_file_error = False

        # Create an ICD of each requested type of output file
        for i, output_format in enumerate(output_formats):
            self.current_format_num = i + 1
            # Update the errors list handler which format is about to be worked on
            ErrorListHandler.update_current_module_name(output_format)

            # Create a temporary directory to save some temporary files
            with tempfile.TemporaryDirectory() as temp_folder:
                try:
                    # Check if the requested file is open
                    if Utils.is_output_file_open(output_file_name, output_folder, output_format):
                        # When the output file is open:
                        is_at_least_one_file_error = True
                        warning_message = f"Cannot save file while {output_file_name}.{output_format} is open. " \
                                          f"Please close the file and try again."
                        self.logger.warning(warning_message)
                        ErrorListHandler.add_entry(LogLevel.ERROR, warning_message)
                        continue

                    # Switch 'output format' to lower case:
                    output_format = output_format.lower()

                    if output_format == 'docx':
                        # Case where the requested type is docx
                        self.doc_generator = DocxGen(title=title,
                                                     version=version,
                                                     time=date_time_string)
                    elif output_format == 'pdf':
                        # Case where the requested type is pdf
                        self.doc_generator = PdfGen(title=title,
                                                    version=version,
                                                    time=date_time_string)

                    # TODO the following comment is for use when we want to use the latex:
                    # elif output_format.lower() == 'tex':
                    #     self.doc_generator = LatexDocGen(title=title, version=version, time=date_time_string)

                    else:
                        # When an invalid type was requested, send warning and continue to the nextformat:
                        warning_message = f"Requested output format '{output_format}' is unsupported at this point."
                        self.logger.warning(warning_message)
                        ErrorListHandler.add_entry(LogLevel.ERROR, warning_message)
                        continue

                    self.single_chapter_generator = SingleChapterGenerator.SingleChapterGenerator(self.engine,
                                                                                                  self.doc_generator)
                    # See whether the ICD is to be based on topics or on types:
                    if dds_topics_types_mapping != "":
                        # When the user provided a topic-to-types xml, a topic-based ICD is to be created:
                        # (generate_topic_based_icd returns a list of all topics that could not be processed)
                        self.generate_topic_based_icd(
                            dds_topics_types_mapping, order_alphabetically)
                    else:
                        # When the user did NOT provide a topic-to-type XML:
                        self.generate_type_based_ICD(order_alphabetically)

                    # update the progress bar and the state (format_save phase)
                    self.update_progress_save()
                    # Finalize and save doc
                    self.doc_generator.finalize_doc()
                    self.doc_generator.generate_doc(output_file_name, temp_folder)
                    self.save_file_to_requested_folder(output_file_name, output_folder, temp_folder, output_format)

                    is_at_least_one_file_created = True

                except Exception as err:
                    ErrorListHandler.add_entry(LogLevel.ERROR, str(err))
                    self.logger.error(str(err), exc_info=True)


        state_txt = f"{ErrorListHandler.get_current_module().lower()}_save"
        self.update_external_progress_bar_function(1,1, state_txt)
        time.sleep(0.5)

        ErrorListHandler.update_current_module_name("general")
        if is_at_least_one_file_created == False:
            warning_message = "There was an issue creating the files. Please refer to the log for more information."
            self.logger.error(warning_message)
            # ErrorListHandler.add_entry(LogLevel.ERROR, warning_message)

            raise Exception(warning_message)

        elif is_at_least_one_file_error:
            msg = "There was an issue with some of the requested files. " \
                  "Please refer to the log for more information."
            self.logger.warning(msg)
            ErrorListHandler.add_entry(LogLevel.WARNING, msg)

            # Clear the temporary directory

    """
    ############################################   MAIN   ############################################
    """

    def run_doc_gen(self,
                          dds_types_files: list,
                          dds_topics_types_mapping: str = "",
                          output_file_name: str = "ICD",
                          title: str = "ICD",
                          version: str = "1.0",
                          order_alphabetically: bool = True,
                          output_folder: str = "",
                          output_formats=None,
                          update_progress_bar_function: Callable[[], Any] = None) -> (bool, List[str]):
        """
        Start the doc generation process.
        :param dds_types_files: (list of strings) A list of file or folders names, in an order specified
                                           by the user according to files dependencies.
        :param dds_topics_types_mapping: (string) An XML file that contains a DDS topic to type mapping. NOTE: This
                                              parameter is optional; Sending an empty string ("") will switch ICD from
                                               topic-based to type-based document, meaning chapters will be types and
                                               not topics,.
        :param output_file_name: (string) The user's file name of choice. NOTE: This parameter is optional.
                                  Default: "ICD".
        :param title: (string) The title/heading  of the document. This string will be added to the first page of the
                               document. NOTE: This parameter is optional; Default is "ICD"
        :param version: The document's version number - This string will be added to the top page of the ICD.
                        NOTE: This parameter is optional; Default is "1.0"
        :param order_alphabetically: Whether to order to generated document topics/types alphabetically or according to
                                    the loaded files order
        :param output_folder: (string) The user's output folder of choice. NOTE: This parameter is optional;
                              Default is current working directory.
        :param output_formats: A list of desired output formats as strings. for example: ["docx", "pdf"]
        :param update_progress_bar_function: A 'pointer' to the function that updates the progress bar.


        :return: tuple of (bool, list). bool: True upon success. list: list of errors that happened along the way
        """
        is_document_generated: bool = False
        try:

            self.check_input(dds_types_files, output_file_name, title, version, dds_topics_types_mapping,
                             output_folder, update_progress_bar_function, output_formats)

            self.logger.info(f"type_file_path_list: {dds_types_files}")
            self.logger.info(f"topic_names_to_types_xml_path: {dds_topics_types_mapping}")
            self.logger.info(f"output_folder: {output_folder}")
            self.logger.info(f"output_file_name: {output_file_name}")

            self.run_engine_and_generate_ICD(dds_types_files,
                                            dds_topics_types_mapping,
                                            output_file_name,
                                            title,
                                            version,
                                            order_alphabetically,
                                            output_folder,
                                            output_formats,
                                            update_progress_bar_function)

            is_document_generated = True

        except Exception as err:
            self.logger.error(err, exc_info=True)
            ErrorListHandler.add_entry(LogLevel.ERROR,err)


        return (is_document_generated, ErrorListHandler.get_error_list())
