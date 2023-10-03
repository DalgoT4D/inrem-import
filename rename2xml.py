"""
traverses a directory tree, renaming any files to .xml if their first line
is an <xml opening tag
"""
#! env python

import logging
from subprocess import check_output
import shutil

LOGFILENAME = "logs/rename2xml.log"
logging.basicConfig(filename=LOGFILENAME, level=logging.INFO)
logger = logging.getLogger()

output = check_output(["/usr/bin/find", "waterQuality/", "-type", "f"])

lines = output.decode("utf-8").split("\n")


def is_xmlfile(filename: str) -> bool:
    """looks at the first line of the file for the <xml> tag"""
    with open(filename, "r", encoding="utf-8") as infile:
        try:
            header = infile.readline()
            return header.startswith("<?xml") or header.startswith("<xml")
        except UnicodeDecodeError:
            return False


for line in lines:
    if line.endswith(".xls") and is_xmlfile(line):
        xmlfilename = line.replace(".xls", ".xml")

    elif line.endswith(".xlsx") and is_xmlfile(line):
        xmlfilename = line.replace(".xlsx", ".xml")

    else:
        continue

    shutil.move(line, xmlfilename)
    logger.info("%s,%s", line, xmlfilename)
