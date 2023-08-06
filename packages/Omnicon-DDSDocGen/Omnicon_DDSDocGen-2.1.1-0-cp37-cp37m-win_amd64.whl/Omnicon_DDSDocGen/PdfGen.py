import os
import sys
import logging
from . import Logger
import docx2pdf
# due to https://stackoverflow.com/questions/74787311/error-with-docx2pdf-after-compiling-using-pyinstaller
logger = Logger.add_logger()
sys.stderr = Logger.LoggerWriter(logger.error)
from .DocxGen import DocxGen
import pythoncom

class PdfGen(DocxGen):
    def __init__(self, title: str, version: str, time: str):
        super().__init__(title, version, time)
        self.logger = Logger.add_logger(__name__)

    def generate_doc(self, output_file_name: str, temp_folder: str)->str:
        self.logger.debug(self.generate_doc.__name__)
        # Create the docx using DocxGen
        super().generate_doc(output_file_name, temp_folder)

        temp_docx_file_name = f'{output_file_name}.docx'
        temp_docx_path = os.path.join(temp_folder, temp_docx_file_name)
        temp_pdf_file_name = f'{output_file_name}.pdf'
        temp_pdf_path = os.path.join(temp_folder, temp_pdf_file_name)

        # Convert to PDF and save into the requested folder
        try:
            self.logger.debug(f"saving {temp_pdf_file_name} into {temp_folder}")
            # keep_active is to prevent the 'docx2pdf.convert' from closing the docx that might be open:
            pythoncom.CoInitialize()
            docx2pdf.convert(temp_docx_path, temp_pdf_path, keep_active=True)

            self.logger.info(f"File saved successfully into '{temp_pdf_path}'")

        except Exception as err:

            self.logger.error(f"Could not save '{temp_pdf_path}'.", exc_info=True)
