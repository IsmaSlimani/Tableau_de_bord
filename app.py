# data_handler function fetches data from the API and stores it in a CSV file.
# Transforming all API data can take around 2 hours.
# No need to uncomment, as the data is already handled in the CSV, and the app can run fine for testing.

# from data_handler.main import data_handler
# data_handler()

# ===============================================


from pages import levels, players
import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Spy Dashboard"

sidebar = html.Div(
    [
        html.Div(

            [html.H2("Spy Dashboard", className="sidebar-title"),
             html.Div(
                [
                    dcc.Link("Levels", href="/levels", className="menu-link"),
                    dcc.Link("Players", href="/players",
                             className="menu-link"),
                ],
                className="sidebar-links"
            )],
            className="sidebar",
        ),
        html.Hr(),
    ],
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        sidebar,
        html.Div(id="page-content", className="content"),
    ],
    className="container",
)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/players":
        return players.layout
    else:
        return levels.layout


if __name__ == "__main__":
    app.run_server(debug=True)
