# for abstract class
import os
from abc import ABC, abstractmethod

"""
Abstract Base class for defining mutual I/F to be implemented for Doc generation
in various platforms for various formats
"""


class DocGenInterface(ABC):
    def __init__(self, title: str, version: str, time: str):
        self.title = title
        self.version = version
        self.time = time

    """
     This function creates a single chapter in the ICD. When a topic-to-types XML was was given by the user,
     a chapter is created for each topic. When  the user did not provide such XML file, a chapter is created for
     each non-nested type.
     :param topic: A string that contains the topic name. NOTE: When the user doesn't provide the topic-to-type XML.
                   This parameter will contain an empty string ('').
     :param dds_type: A string that contains the type name.
     """

    @abstractmethod
    def add_doc_title_page(self):
        pass

    @abstractmethod
    def add_toc_page(self):
        pass

    @abstractmethod
    def add_chapter(self, title, sub_title=""):
        pass

    # NonAbstract
    def start_table_generation(self):
        tableGenProcess = True

    # NonAbstract
    def table_end(self):
        tableGenProcess = False

    @abstractmethod
    def add_table_header(self, listOfTitles, bLongHeader, color):
        pass

    @abstractmethod
    def add_table_row(self, theTable, cells_text, align='c'):  # align=centered
        pass

    @abstractmethod
    def add_new_page(self):
        pass

    @abstractmethod
    def add_section(self):
        pass

    @abstractmethod
    def add_description(self, descr):
        pass

    @abstractmethod
    def add_new_line(self):
        pass

    @abstractmethod
    def finalize_doc(self):
        # Intended post-processing prior to calling generate_doc
        pass

    @abstractmethod
    def generate_doc(self, output_file_name: str, temp_folder: str):
        pass
