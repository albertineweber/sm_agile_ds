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
    width=1200,
    height=600,
    template="plotly_white",
    font=dict(
        color="black",
        size=28,  # can change the size of font here
        family="Times New Roman",
    ),
)

fig = go.Figure(layout=layout)

# Add database info
for db in complete_df["database"].unique():

    filt_df = complete_df[complete_df["database"] == db]

    step1 = len(filt_df)
    step2 = step1 - len(filt_df[filt_df["exclusion_step"] == "Duplicates filter"])
    step3 = step2 - len(filt_df[filt_df["exclusion_step"] == "Metadata filter"])
    step4 = step3 - len(filt_df[filt_df["exclusion_step"] == "Full-text filter"])

    fig.add_trace(
        go.Funnel(
            name=db,
            y=[
                "Após Etapa 1 - Coleta de artigos",
                "Após Etapa 2 - Remover duplicados",
                "Após Etapa 3 - Filtro de metadados",
                "Após Etapa 4 - Filtro de leitura",
            ],
            x=[step1, 0, 0, 0],
            textinfo="value",
            textfont=dict(
                color="black",
                size=22,  # can change the size of font here
                family="Times New Roman",
            ),
            constraintext="outside",
            marker=dict(line=dict(color="white")),
        ),
    )

# Add totals info
filt_df = complete_df.copy()

step1 = len(filt_df)
step2 = step1 - len(filt_df[filt_df["exclusion_step"] == "Duplicates filter"])
step3 = step2 - len(filt_df[filt_df["exclusion_step"] == "Metadata filter"])
step4 = step3 - len(filt_df[filt_df["exclusion_step"] == "Full-text filter"])

fig.add_trace(
    go.Funnel(
        y=[
            "Após Etapa 1 - Coleta de artigos",
            "Após Etapa 2 - Remover duplicados",
            "Após Etapa 3 - Filtro de metadados",
            "Após Etapa 4 - Filtro de leitura",
        ],
        x=[0, step2, step3, step4],
        textinfo="value",
        textfont=dict(
            color="black",
            size=28,  # can change the size of font here
            family="Times New Roman",
        ),
        constraintext="outside",
        marker=dict(line=dict(color="white")),
        showlegend=False,
    ),
)

fig.add_annotation(
    text=str(step1),
    showarrow=False,
    xref="paper",
    yref="paper",
    x=1.02,
    y=0.91,
    font=dict(
        color="black",
        size=24,  # can change the size of font here
        family="Times New Roman",
    ),
)

fig.write_image("%s/funnel_plot.png" % path_output)
