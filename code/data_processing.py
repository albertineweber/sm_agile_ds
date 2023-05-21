import datetime
import os

import numpy as np
import pandas as pd

# get most recent version
path_raw = "data/01_raw"
path_intermediate = "data/02_intermediate"
latest_version = max(os.listdir(path_raw))
# id of the current version: execution_version = "20230521-044735"
execution_version = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# read files per source
acm_df = pd.read_csv("%s/%s/acm.csv" % (path_raw, latest_version))
ieeex_df = pd.read_csv("%s/%s/ieeex.csv" % (path_raw, latest_version))
scopus_df = pd.read_csv("%s/%s/scopus.csv" % (path_raw, latest_version))
wos_df = pd.read_excel("%s/%s/wos.xls" % (path_raw, latest_version))

dbs_dct = {"acm": acm_df, "ieeex": ieeex_df, "scopus": scopus_df, "wos": wos_df}

# create default keys
tb_keys = [
    "entry",
    "database",
    "title",
    "abstract",
    "author_keywords",
    "authors",
    "authors_affiliations",
    "publication_year",
    "source_title",
    "publisher",
    "url",
    "doi",
    "query_date",
    "processing_date",
]

# create dict for aligning names between different dbs
replace_dct = {
    "acm": {
        "keywords": "author_keywords",
    },
    "ieeex": {
        "author_affiliations": "authors_affiliations",
        "document_title": "title",
        "publication_title": "source_title",
        "pdf_link": "url",
    },
    "scopus": {
        "year": "publication_year",
        "affiliations": "authors_affiliations",
        "link": "url",
    },
    "wos": {
        "article_title": "title",
        "affiliations": "authors_affiliations",
    },
}

for db in dbs_dct:
    df = dbs_dct[db]

    # adjust name formatting
    cols = [col.lower().replace(" ", "_") for col in df.columns]

    # replace col names with standardized names
    for orig_col, new_col in replace_dct[db].items():
        cols = [col.replace(orig_col, new_col) for col in cols]
    df.columns = cols

    # create missing columns
    df["database"] = db
    df["query_date"] = latest_version
    df["processing_date"] = execution_version

    missing_cols = [col for col in tb_keys if col not in dbs_dct[db].columns]
    for col in missing_cols:
        df[col] = np.nan

    dbs_dct[db] = df

# extra adjustments
dbs_dct["acm"]["source_title"] = np.where(
    dbs_dct["acm"]["journal"].isna(),
    dbs_dct["acm"]["proceedings_title"],
    dbs_dct["acm"]["journal"],
)

# filter dbs
for db in dbs_dct:
    dbs_dct[db] = dbs_dct[db][tb_keys]

# concatanate dbs
consolidated_df = pd.concat([df for df in dbs_dct.values()]).reset_index(drop=True)
consolidated_df["entry"] = consolidated_df.index + 1

# save versioned dbs
if not os.path.exists("%s/%s" % (path_intermediate, execution_version)):
    os.makedirs("%s/%s" % (path_intermediate, execution_version))

for db in dbs_dct:
    dbs_dct[db].to_csv(
        "%s/%s/%s.csv" % (path_intermediate, execution_version, db), index=False
    )

consolidated_df.to_csv(
    "%s/%s/search_table.csv" % (path_intermediate, execution_version), index=False
)

# save current version
consolidated_df.to_csv("%s/search_table.csv" % (path_intermediate), index=False)
consolidated_df.to_excel("%s/search_table.xlsx" % (path_intermediate), index=False)
