from dash import Dash, Input, Output, State, html

import plumage_dash_components as pdc

app = Dash(__name__)

app.layout = html.Div(
    [
    pdc.Dropdown(id="dropdown0"), #, options=[{"label": "test1", "value": "test2"}])
    pdc.Dropdown(id="dropdown1", options=[{"label": "test1", "value": "test1"}, {"label": "test2", "value": "test2"}]),
    pdc.Dropdown(id="dropdown2", options=[{"label": "test1", "value": "test1"}, {"label": "test2", "value": "test2"}], isDisabled=True), 
    pdc.Dropdown(id="dropdown3", label= "Some Label", options=[{"label": "test1", "value": "test1"}, {"label": "test2", "value": "test2"}], isMulti=False, isClearable=False, hideSelectedOptions=False, closeMenuOnSelect=True),
    ]
)


@app.callback(
    Output("dropdown0", "options"),
    Input("dropdown0", "value"),
    Input("dropdown1", "value"),
    Input("dropdown2", "value"),
    Input("dropdown3", "value"),
)
def update_colors(value0, value1, value2, value3):
    print("DropDown 0")
    print(value0)
    print("DropDown 1")
    print(value1)
    print("DropDown 2")
    print(value2)
    print("DropDown 3")
    print(value3)
    return ["test1", "test2"]

if __name__ == "__main__":
    app.run_server(debug=True)
