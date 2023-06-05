import datetime

import pandas as pd
from plotly import graph_objects as go

# get most recent version
path_mi = "data/05_model_input"
path_output = "plots"

# id of the current version: execution_version = ""
execution_version = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# read input_table
complete_df = pd.read_csv(
    "%s/complete_filled_search_table.csv" % (path_mi), encoding="UTF-16"
)


# Create plot layout
layout = go.Layout(
    width=1600,
    height=500,
    template="plotly_white",
    font=dict(
        color="black",
        size=22,  # can change the size of font here
        family="Times New Roman",
    ),
)

# Create display dict
rename_dict = {
    "Not IC1 - Agile + DS": "~IC1: Fuga do tema",
    "Not IC2 - J, C, M": (
        "~IC2, ~IC4, <br>EC5: Ano, <br>local ou <br>idioma <br>invalido"
    ),
    "Not IC4 - <2018": "~IC2, ~IC4, <br>EC5: Ano, <br>local ou <br>idioma <br>invalido",
    "EC1 - Agile w/o DS": "EC1: MA <br>sem CD",
    "EC2 - DS w/o Agile": "EC2: CD sem MA",
    "EC4 - Only abstract": "EC4/EC7: <br>Indisponível <br>ou incompleto",
    "EC6 - Not a primary study": "EC6: Estudo <br>Secundario",
    "EC5 - Not in english": (
        "~IC2, ~IC4, <br>EC5: Ano, <br>local ou <br>idioma <br>invalido"
    ),
    "EC7 - Unavailable or incomplete": "EC4/EC7: <br>Indisponível <br>ou incompleto",
}

filt_df = complete_df.copy()

for key in rename_dict:

    filt_df["fulltext_exclusion_criteria"] = filt_df[
        "fulltext_exclusion_criteria"
    ].replace(key, rename_dict[key])

filt_series = filt_df[filt_df["fulltext_exclusion_flag"] == 1][
    "fulltext_exclusion_criteria"
].value_counts()

fig = go.Figure(layout=layout)

fig = go.Figure(
    go.Treemap(
        labels=[
            "%s <br>%s pubs."
            % (list(filt_series.index)[i], list(filt_series.values)[i])
            for i in range(0, len(filt_series))
        ],
        values=list(filt_series.values),
        parents=["" for x in list(filt_series.index)],
        pathbar_textfont_size=15,
    )
)

fig.update_layout(
    uniformtext=dict(minsize=15, mode="show"), margin=dict(t=25, l=25, r=25, b=25)
)

fig.write_image("%s/treemap_plot.png" % path_output)
