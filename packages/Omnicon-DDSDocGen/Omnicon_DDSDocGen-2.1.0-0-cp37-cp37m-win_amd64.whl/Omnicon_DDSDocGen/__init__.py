# from .DocGenLogic import DocumentGenerator
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from Omnicon_DDSDocGen import Logger
from Omnicon_DDSDocGen import Utils
from Omnicon_DDSDocGen import DocGenLogic
from Omnicon_DDSDocGen.DocGenInterface import DocGenInterface
from Omnicon_DDSDocGen import SingleChapterGenerator
from Omnicon_DDSDocGen import PdfGen
from Omnicon_DDSDocGen import DocxGen
from Omnicon_DDSDocGen import DocGenInterface
from Omnicon_DDSDocGen import ErrorListHandler
