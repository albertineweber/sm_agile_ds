import datetime
import os

import numpy as np
import pandas as pd

# get most recent version
path_intermediate = "data/02_intermediate"
path_primary = "data/03_primary"
latest_version = max(os.listdir(path_intermediate))
# id of the current version: execution_version = ""
execution_version = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# read input_table
consolidated_df = pd.read_csv("%s/search_table.csv" % (path_intermediate))

# sanitize title name
consolidated_df["sanitized_title"] = consolidated_df["title"].str.lower().str.split(" ")

# build doi and title duplicated flags
consolidated_df["duplicated_title"] = consolidated_df["sanitized_title"].duplicated()
consolidated_df["duplicated_doi"] = (consolidated_df["doi"].duplicated()) & (
    ~consolidated_df["doi"].isna()
)

# generate exclusion flag
consolidated_df["duplicated_exclusion_flag"] = (
    consolidated_df["duplicated_title"] | consolidated_df["duplicated_doi"]
)
consolidated_df["duplicated_validation_date"] = execution_version

consolidated_df = consolidated_df.drop(["duplicated_title", "duplicated_doi"], axis=1)

# create empty validation cols
consolidated_df["metadata_exclusion_flag"] = np.nan
consolidated_df["metadata_exclusion_criteria"] = np.nan
consolidated_df["metadata_validation_date"] = np.nan
consolidated_df["fulltext_exclusion_flag"] = np.nan
consolidated_df["fulltext_exclusion_criteria"] = np.nan
consolidated_df["fulltext_validation_date"] = np.nan

# save versioned dbs
if not os.path.exists("%s/versioned/%s" % (path_primary, execution_version)):
    os.makedirs("%s/versioned/%s" % (path_primary, execution_version))

consolidated_df.to_csv(
    "%s/versioned/%s/cleaned_search_table.csv" % (path_primary, execution_version),
    index=False,
)

# save current version
consolidated_df.to_csv("%s/cleaned_search_table.csv" % (path_primary), index=False)
