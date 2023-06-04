import datetime
import os

import numpy as np
import pandas as pd

# get most recent version
path_feature = "data/04_feature"
path_mi = "data/05_model_input"
latest_version = max(os.listdir(path_feature))
# id of the current version: execution_version = ""
execution_version = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# read input_table
consolidated_df = pd.read_excel("%s/filled_search_table.xlsx" % (path_feature))

# save copy of versioned dbs and current version
if not os.path.exists("%s/versioned/%s" % (path_feature, execution_version)):
    os.makedirs("%s/versioned/%s" % (path_feature, execution_version))

consolidated_df.to_csv(
    "%s/versioned/%s/filled_search_table.csv" % (path_feature, execution_version),
    index=False,
    encoding="utf-16",
)

consolidated_df.to_csv(
    "%s/filled_search_table.csv" % (path_feature), index=False, encoding="utf-16"
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
    "EC0 - Duplicated entry",
    consolidated_df["metadata_exclusion_criteria"],
    consolidated_df["fulltext_exclusion_criteria"],
]
dates_choices = [
    consolidated_df["duplicated_validation_date"],
    consolidated_df["metadata_validation_date"],
    consolidated_df["fulltext_validation_date"],
]

consolidated_df["exclusion_criteria"] = np.select(
    conditions, criteria_choices, default="Not excluded"
)
consolidated_df["exclusion_date"] = np.select(conditions, dates_choices, default="N/A")

# Save complete dataframe
complete_df = consolidated_df.copy()

# Create filtered copy with only selected studies
selected_df = consolidated_df[consolidated_df["exclusion_criteria"] == "Not excluded"]

cols_for_rqs = [
    "RQ1_PubSourceType",
    "RQ1_PubSourceName",
    "RQ1_PubYear",
    "RQ2_ResearchType",
    "RQ3_ResearchMethod",
    "RQ4_OrganizationType",
    "RQ5_SubtopicsAM",
    "RQ6_SubtopicsDS",
    "RQ7_ProblemsReported",
    "RQ8_ObjectiveAM",
    "RQ9_ContributionsResults",
]

for col in cols_for_rqs:
    selected_df[col] = np.nan

# save copy of versioned dbs and current version
if not os.path.exists("%s/versioned/%s" % (path_mi, execution_version)):
    os.makedirs("%s/versioned/%s" % (path_mi, execution_version))

complete_df.to_csv(
    "%s/versioned/%s/complete_filled_search_table.csv" % (path_mi, execution_version),
    index=False,
    encoding="utf-16",
)

complete_df.to_csv(
    "%s/complete_filled_search_table.csv" % (path_mi), index=False, encoding="utf-16"
)

selected_df.to_csv(
    "%s/versioned/%s/selected_filled_search_table.csv" % (path_mi, execution_version),
    index=False,
    encoding="utf-16",
)

selected_df.to_csv(
    "%s/selected_filled_search_table.csv" % (path_mi), index=False, encoding="utf-16"
)
