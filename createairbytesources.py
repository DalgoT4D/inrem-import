"""create airbyte sources for the csvs in s3"""
#!env python

import sys
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--aws-access-key-id", required=True)
parser.add_argument("--aws-secret-access-key", required=True)
parser.add_argument("--workspace-id", required=True)
parser.add_argument("--airbyte-api-token", required=True)
parser.add_argument("--delete-sources", action="store_true")
args = parser.parse_args()

AIRBYTE_API_TOKEN = args.airbyte_api_token


s3keys = {
    "s3://dalgo-data/inrem/csvs/waterQuality_fluoride_all_states_SK_Nov_20_2015.csv": "allstates",
    "s3://dalgo-data/inrem/csvs/waterQuality_guj_wq_blocks.csv": "guj_wq_blocks",
    "s3://dalgo-data/inrem/csvs/waterQuality_guj_wq.csv": "guj_wq",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_all_fluoride_IndiaFluoride10-11_SK_Mar_16_2016.csv": "IndiaFluoride10_11",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_all_fluoride_IndiaFluoride11-12_SK_Mar_16_2016.csv": "IndiaFluoride11_12",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_all_fluoride_IndiaFluoride12-13_SK_Mar_17_2016.csv": "IndiaFluoride12_13",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_all_fluoride_Indiafluoride13-14_SK_Mar_17_2016.csv": "Indiafluoride13_14",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_all_fluoride_Indiafluoride14-15_SK_Mar_17_2016.csv": "Indiafluoride14_15",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_IndiaFluoride12-13_SK_Mar_17_2016_new.csv": "IndiaFluoride12_13_new",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_indiafluoride_too_high_values_SK_Mar_16_2016.csv": "indiafluoride_too_high",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_Jamui_Jamui_fluoride_SK_Mar_28_2016.csv": "Jamui_fluoride",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPFluoride10-11_SK_Mar_21_2016.csv": "MPFluoride10_11",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPFluoride10_to_15_SK_Mar_21_2016.csv": "MPFluorid_10_15",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPFluoride11-12_SK_Mar_21_2016.csv": "MPFluoride11_12",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPFluoride12-13_SK_Mar_21_2016.csv": "MPFluoride12_13",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPfluoride13-14_SK_Mar_21_2016.csv": "MPfluoride13_14",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPfluoride14-15_SK_Mar_21_2016.csv": "MPfluoride14_15",
    "s3://dalgo-data/inrem/csvs/waterQuality_HARSH_MP_MPFluoride_Data_Fluoride_network_SK_June_14_2016.csv": "Fluoride_network",
    "s3://dalgo-data/inrem/csvs/waterQuality_mapping_jhabua201011.csv": "jhabua201011",
    "s3://dalgo-data/inrem/csvs/waterQuality_New_Data_Updated_May_2017_2013-14_high_values.csv": "2013_14_high_values",
    "s3://dalgo-data/inrem/csvs/waterQuality_New_Data_Updated_May_2017_district_summary_2013-14_SK_May_10_2017.csv": "district_summary_2013_14",
    "s3://dalgo-data/inrem/csvs/waterQuality_New_Data_Updated_May_2017_India_Fluoride_2013-14.csv": "2017_India_Fluoride_2013_14",
    "s3://dalgo-data/inrem/csvs/waterQuality_New_Data_Updated_May_2017_India_Fluoride_2014-15.csv": "2017_India_Fluoride_2014_15",
}


def get_airbyte_sources(workspace_id: str):
    """get list of sources for this workspace"""
    req = requests.post(
        "http://localhost:8000/api/v1/sources/list",
        headers={"Authorization": f"Basic {AIRBYTE_API_TOKEN}"},
        json={"workspaceId": workspace_id},
    )
    sources = req.json()
    return sources["sources"]


all_workspace_sources = get_airbyte_sources(args.workspace_id)
print(all_workspace_sources)

if args.delete_sources:
    for workspace_source in all_workspace_sources:
        if workspace_source["name"] in s3keys.values():
            r = requests.post(
                "http://localhost:8000/api/v1/sources/delete",
                headers={"Authorization": f"Basic {AIRBYTE_API_TOKEN}"},
                json={"sourceId": workspace_source["sourceId"]},
            )
    sys.exit(0)


all_source_names = [x["name"] for x in all_workspace_sources]

for s3key, sourcename in s3keys.items():
    if sourcename in all_source_names:
        continue
    payload = {
        "name": sourcename,
        "workspaceId": args.workspace_id,
        "sourceDefinitionId": "778daa7c-feaf-4db6-96f3-70fd645acc77",
        "connectionConfiguration": {
            "url": s3key,
            "format": "csv",
            "reader_options": "{}",
            "dataset_name": sourcename,
            "provider": {
                "storage": "S3",
                "aws_access_key_id": args.aws_access_key_id,
                "aws_secret_access_key": args.aws_secret_access_key,
            },
        },
    }
    r = requests.post(
        "http://localhost:8000/api/v1/sources/create",
        headers={"Authorization": f"Basic {AIRBYTE_API_TOKEN}"},
        json=payload,
    )
    print(r.json())
    r.raise_for_status()
