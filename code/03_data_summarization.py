import datetime
import os

import numpy as np
import pandas as pd

# get most recent version
path_primary = "data/03_primary"
path_feature = "data/04_feature"
latest_version = max(os.listdir(path_primary))
# id of the current version: execution_version = ""
execution_version = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# read input_table
consolidated_df = pd.read_csv(
    "%s/cleaned_search_table.csv" % (path_primary), encoding="UTF-16"
)

# create dict of criterias
criterias_dct = {
    "EC0": "EC0 - Duplicated entry",
    "EC1": "EC1 - Agile w/o DS",
    "EC2": "EC2 - DS w/o Agile",
    "EC3": "EC3 - No abstract",
    "EC4": "EC4 - Only abstract",
    "EC5": "EC5 - Not in english",
    "EC6": "EC6 - Not a primary study",
    "EC7": "EC7 - Unavailable or incomplete",
    "NIC1": "Not IC1 - Agile + DS",
    "NIC2": "Not IC2 - J, C, M",
    "NIC3": "Not IC3 - No search term",
    "NIC4": "Not IC4 - <2018",
}


# create exclusion criteria and date cols
conditions = [
    consolidated_df["duplicated_exclusion_flag"] == 1,
    consolidated_df["metadata_exclusion_flag"] == 1,
    consolidated_df["fulltext_exclusion_flag"] == 1,
]
criteria_choices = [
    "EC0",
    consolidated_df["metadata_exclusion_criteria"],
    consolidated_df["fulltext_exclusion_criteria"],
]
dates_choices = [
    consolidated_df["duplicated_validation_date"],
    consolidated_df["metadata_validation_date"],
    consolidated_df["fulltext_validation_date"],
]

consolidated_df["exclusion_criteria"] = np.select(
    conditions, criteria_choices, default=np.nan
)
consolidated_df["exclusion_date"] = np.select(conditions, dates_choices, default=np.nan)

# TODO: create logic for dummification of exclusion criterias used?
# TODO: create cols for RQs
