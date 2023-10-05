"""read excel and output csv"""
#!env python

import os
import pandas as pd

filenames = [
    "waterQuality/HARSH/MP/MPFluoride10-11 SK Mar 21 2016.xlsx",
    "waterQuality/HARSH/MP/MPFluoride11-12 SK Mar 21 2016.xls",
    "waterQuality/HARSH/MP/MPFluoride Data Fluoride network SK June 14 2016.xlsx",
    "waterQuality/HARSH/MP/MPFluoride10 to 15 SK Mar 21 2016.xlsx",
    "waterQuality/HARSH/MP/MPFluoride12-13 SK Mar 21 2016.xls",
    "waterQuality/HARSH/MP/MPfluoride14-15 SK Mar 21 2016.xlsx",
    "waterQuality/HARSH/MP/MPfluoride13-14 SK Mar 21 2016.xlsx",
    "waterQuality/HARSH/IndiaFluoride12-13 SK Mar 17 2016 new.xlsx",
    "waterQuality/HARSH/Jamui/Jamui fluoride SK Mar 28 2016.xlsx",
    "waterQuality/HARSH/indiafluoride too high values SK Mar 16 2016.xlsx",
    "waterQuality/HARSH/all fluoride/IndiaFluoride12-13 SK Mar 17 2016.xls",
    "waterQuality/HARSH/all fluoride/IndiaFluoride10-11 SK Mar 16 2016.xlsx",
    "waterQuality/HARSH/all fluoride/IndiaFluoride11-12 SK Mar 16 2016.xls",
    "waterQuality/HARSH/all fluoride/Indiafluoride14-15 SK Mar 17 2016.xlsx",
    "waterQuality/HARSH/all fluoride/Indiafluoride13-14 SK Mar 17 2016.xlsx",
    "waterQuality/guj wq blocks.xlsx",
    "waterQuality/guj wq.xlsx",
    "waterQuality/fluoride all states SK Nov 20 2015.xlsx",
    "waterQuality/New Data Updated May 2017/2013-14 high values.xlsx",
    "waterQuality/New Data Updated May 2017/India Fluoride 2014-15.xlsx",
    "waterQuality/New Data Updated May 2017/district summary 2013-14 SK May 10 2017.xlsx",
    "waterQuality/New Data Updated May 2017/India Fluoride 2013-14.xlsx",
    "waterQuality/mapping/jhabua201011.xlsx",
]

os.makedirs("csvs/", exist_ok=True)

for filename in filenames:
    df = pd.read_excel(filename)
    head, oldfilename = os.path.split(filename)
    name, extenstion = os.path.splitext(oldfilename)
    name = head.replace("/", "_").replace(" ", "_") + "_" + name.replace(" ", "_")
    newfilename = f"csvs/{name}.csv"
    df.to_csv(newfilename, index=False)
