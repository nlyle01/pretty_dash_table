import pandas as pd
import dash
from dash import callback, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


BOOTSTRAP_ICONS = "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css"


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, BOOTSTRAP_ICONS])  # bootstrap, litera


data = {
    "Sales Region": ["North", "South", "East", "West"],
    "Sales Lead": ["John Smith", "Jane Doe", "Sam Sammy", "Mr. Sir"],
    "Coverage": [55, 30, 70, 20],
    "Sales": [15000, 25000, 10000, 35000],
    "delta": [500, -150, 0, -1000],
    "delta_type": ["positive", "negative", "none", "negative"]
}


df = pd.DataFrame(data)


def apply_variance_icon(delta_type, delta):
    if delta_type == "negative":
        return dbc.Badge(delta, pill = False, color="#FAE9E8", text_color="danger", className = "badge-variance")
    elif delta_type == "positive":
        return dbc.Badge(delta, pill = False, color = "#F1FCEF", text_color = "success", className = "badge-variance")
    else:
        return dbc.Badge("0", pill = False, color = "#F7F8FB", text_color = "secondary", className = "badge-variance")


df["Sales"] = df["Sales"].astype(int).apply('{:,}'.format)

df["delta"] = df["delta"].astype(int).apply('{:,}'.format)

df["Coverage YTD"] = df.apply(lambda x: dbc.Progress(value = x["Coverage"]), axis = 1)

df["Lead"] = df.apply(
    lambda x: dbc.Badge([html.I(className="bi bi-person-fill"), " "+x["Sales Lead"]], color = "#F2F2F2", text_color = "black", className="badge-person"),
    axis = 1
)

df["Over/Under"] = df.apply(lambda x: apply_variance_icon(x["delta_type"], x["delta"]), axis=1)

df_final = df[["Sales Region", "Lead", "Coverage YTD", "Sales", "Over/Under"]]


test_df_table = dbc.Table.from_dataframe(df_final, bordered=True)


app.layout = html.Div(
    [
        dbc.Container(
            children = [
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H2(html.B("Plotly Dash ✨"), className = "card-title"),
                                            # html.Small(["Fake Data "]),
                                            dbc.Badge("Fake Data", color = "dark"),
                                            html.Br(),
                                            html.Br(),
                                            test_df_table,
                                        ]
                                    )
                                ],
                                className = "shadow p-3"
                            ),
                            width = 9
                        )
                    ],
                    className = "mb-3"
                ),
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
