"""
traverses a directory tree, attempting to read all excel files

"""
#! env python
import os
import logging
from subprocess import check_output
import json
from hashlib import md5
import pandas as pd

LOGFILENAME = "logs/readexcelfiles.log"
logging.basicConfig(filename=LOGFILENAME, level=logging.INFO)
logger = logging.getLogger()

output = check_output(["/usr/bin/find", "waterQuality/", "-type", "f"])

lines = output.decode("utf-8").split("\n")


def colspechash(columns):
    """creates a hash out of the column spec"""
    columns = list(columns)
    return md5(json.dumps(columns).encode("utf-8")).hexdigest()


def is_xmlfile(filename: str) -> bool:
    """looks at the first line of the file for the <xml> tag"""
    with open(filename, "r", encoding="utf-8") as infile:
        try:
            header = infile.readline()
            return header.startswith("<?xml") or header.startswith("<xml")
        except UnicodeDecodeError:
            return False


by_schema = {}


for line in lines:
    if line.endswith(".xls") or line.endswith(".xlsx"):
        if not is_xmlfile(line):
            try:
                df = pd.read_excel(line)
            except ValueError:
                logger.error("could not open %s", line)
                continue
            logger.info("reading column schema of %s", line)
            # pylint:disable=invalid-name
            hashkey = colspechash(df.columns)
            if hashkey not in by_schema:
                by_schema[hashkey] = []
            by_schema[hashkey].append(
                {
                    "file": line,
                    "colspec_hash": hashkey,
                    "rows": len(df),
                }
            )

for hashkey, filelist in by_schema.items():
    os.makedirs(f"column_specs/{hashkey}/", exist_ok=True)
    outputfilename = f"column_specs/{hashkey}/filelist.csv"
    with open(outputfilename, "w", encoding="utf-8") as outfilelist:
        logger.info("writing %s", outputfilename)
        for file_entry in filelist:
            outfilelist.write(
                f'{file_entry["file"]},{file_entry["colspec_hash"]},{file_entry["rows"]}\n'
            )
