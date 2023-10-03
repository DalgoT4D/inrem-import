"""reads inrems excel files and outputs csv where possible"""
#!env python

import json
from hashlib import md5
from subprocess import check_output
import logging
import tempfile
import shutil
import pandas as pd

LOGFILENAME = "logs/xl2csv.log"

logging.basicConfig(filename=LOGFILENAME, level=logging.INFO)
logger = logging.getLogger()

output = check_output(["/usr/bin/find", "waterQuality/", "-type", "f"])

lines = output.decode("utf-8").split("\n")


def colspechash(columns):
    """creates a hash out of the column spec"""
    columns = list(columns)
    return md5(json.dumps(columns).encode("utf-8")).hexdigest()


def xml2xlsx(xmlfilename: str, outputfilename: str) -> None:
    """takes an xlsx-compatible xml file and creates an xlsx"""
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree("sample", tmpdir, dirs_exist_ok=True)
        shutil.copyfile(xmlfilename, f"{tmpdir}/xl/worksheets/sheet1.xml")
        shutil.make_archive(outputfilename, "zip", tmpdir)
        logger.warning("made archive %s => %s", xmlfilename, outputfilename)


seen = set()

with open(LOGFILENAME, "r", encoding="utf-8") as logfile:
    for logline in logfile.readlines():
        rundata = logline.split(":")[2]
        if rundata[0] == "INFO":
            hashkey, line = rundata.split(",")
            seen.add(line)

for line in lines:
    if line in seen:
        continue

    if line.endswith(".xml"):
        xlsxfilename = line.replace(".xml", ".xlsx")
        xml2xlsx(line, xlsxfilename)

    elif line.endswith(".xls") or line.endswith(".xlsx"):
        try:
            df = pd.read_excel(line)
        except ValueError:
            logger.error("could not open %s", line)
            continue

        # pylint:disable=invalid-name
        hashkey = colspechash(df.columns)
        logger.info("%s,%s", hashkey, line)
        seen.add(line)
