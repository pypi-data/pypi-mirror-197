from typing import Any, Callable, List
from . import DocGenLogic


class DDSDocGen():
    def __init__(self, logging_verbosity: str = "INFO") -> None:
        """
        :param logging_verbosity: The requested level of logging. Could be either 'CRITICAL','ERROR','WARNING',
                                'INFO' or 'DEBUG'. NOTE: This parameter is optional; Default is 'INFO'.
        """
        self.__document_generator = DocGenLogic.DocumentGenerator(logging_verbosity)

    def generate_document(self,
                          dds_types_files: list,
                          dds_topics_types_mapping: str = "",
                          output_file_name: str = "ICD",
                          title: str = "ICD",
                          version: str = "1.0",
                          order_alphabetically: bool = True,
                          output_folder: str = "",
                          output_formats=None,
                          update_progress_bar_function: Callable[[], Any] = None
                          ) -> (bool, List[str]):
        """
        Start the doc generation process.
        :param dds_types_files: A list of DDS XML type files or folders.
            :param dds_topics_types_mapping: (string) An XML file that contains a DDS topic to type mapping. NOTE: This
                                              parameter is optional; In case the mapping is not provided, a type-based
                                              ICD will be generated.
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

        return self.__document_generator.run_doc_gen(
            dds_types_files=dds_types_files,
            dds_topics_types_mapping=dds_topics_types_mapping,
            output_file_name=output_file_name,
            title=title,
            version=version,
            order_alphabetically=order_alphabetically,
            output_folder=output_folder,
            output_formats=output_formats,
            update_progress_bar_function=update_progress_bar_function
        )
