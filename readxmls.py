"""extracts the data from the excel 2003 xml files and writes them to csvs"""
#!env python

import logging
from subprocess import check_output
from bs4 import BeautifulSoup

LOGFILENAME = "logs/readxmls.log"
logging.basicConfig(filename=LOGFILENAME, level=logging.INFO)
logger = logging.getLogger()


def is_xmlfile(fname: str) -> bool:
    """looks at the first line of the file for the <xml> tag"""
    with open(fname, "r", encoding="utf-8") as infile:
        try:
            header = infile.readline()
            return header.startswith("<?xml") or header.startswith("<xml")
        except UnicodeDecodeError:
            return False


output = check_output(["/usr/bin/find", "waterQuality/", "-type", "f"])

lines = output.decode("utf-8").split("\n")

num_pageo_file = open("num_pageo.txt", "w", encoding="utf-8")

for filename in lines:
    if (filename.endswith(".xls") or filename.endswith(".xlsx")) and is_xmlfile(
        filename
    ):
        logger.info("reading file: %s", filename)
        with open(filename, "r", encoding="utf-8") as f:
            xml = f.read()

        soup = BeautifulSoup(xml, "lxml")

        worksheets = soup.find_all("worksheet")

        for ws in worksheets:
            ws_name = ws.attrs.get("ss:name")
            logger.info("reading worksheet: %s %s", filename, ws_name)

            # If there's no row data, skip
            if not ws.table.row:
                logger.warning(
                    "No data found in this worksheet: %s %s", filename, ws_name
                )
                continue

            rows = ws.table.find_all("row")

            column_names = [cell.data.string for cell in rows[0].find_all("cell")]

            for idx, row in enumerate(rows[1:]):
                cell_values = []
                for cell in row.find_all("cell"):
                    if cell.data is None:
                        cell_values.append("")
                    else:
                        cell_values.append(cell.data.string)
                data = dict(zip(column_names, cell_values))
                data["file"] = filename
                data["sheet"] = ws_name
                data["row"] = idx + 1
                if column_names == ["num", "pageo"]:
                    num_pageo_file.write(
                        f"{data['file']},{data['sheet']},{data['row']},{data['num']},{data['pageo']}\n"
                    )
                else:
                    # write to stdout
                    print(data)

num_pageo_file.close()
