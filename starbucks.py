##-------import packages--------------------------------------------------------
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input,Output



##--------import data-----------------------------------------------------------
# drinks data
df_drinks = pd.read_csv("starbucks_drinkMenu_expanded.csv")
df_drinks = df_drinks[df_drinks["Category"]!="Frappuccino® Light Blended Coffee"]
df_drinks["Beverage"] = df_drinks.apply(lambda row: row["Beverage"]+" Frappucino" if "Frappuccino" in row["Category"] else row["Beverage"], axis=1)
df_drinks = df_drinks.drop(["Category","Trans Fat (g)","Saturated Fat (g)","Sodium (mg)","Dietary Fibre (g)","Vitamin A (% DV)","Vitamin C (% DV)","Calcium (% DV)","Iron (% DV)"], axis=1)
df_drinks["Milk"] = df_drinks["Milk"].fillna("No Milk")


# map data
df_map = pd.read_csv("directory.csv")
df_map = df_map.drop(df_map.loc[df_map["Brand"]=="Teavana"].index)
df_map["Phone Number"] = df_map["Phone Number"].fillna("n/a")
df_map["Postcode"] = df_map["Postcode"].fillna(".")
df_map["Address"]= np.where(df_map["Postcode"]==".",(df_map["Street Address"]+", "+df_map["City"]),(df_map["Street Address"]+", "+df_map["City"]+", "+df_map["Postcode"]))
df_map = df_map.drop(["Brand","Store Number","Street Address","City","State/Province","Country","Postcode","Timezone"], axis=1)
df_map = df_map.reindex(columns=["Store Name","Address","Phone Number","Ownership Type","Latitude","Longitude"])



##--------create functions------------------------------------------------------
def draw_bar(dataframe):
    text_labels = [str(val) for val in dataframe["Amount"]]
    max_range = int(max(dataframe["Amount"]))+10
    colors = ["#EAD2AC","#C47335","#A63D40","#6C8EAD"]
    figure = go.Figure(data=[go.Bar(x=dataframe["Nutrition"], y=dataframe["Amount"])])
    figure.update_layout(yaxis_range=[0,max_range], xaxis_title="", plot_bgcolor="#F2F2F2", paper_bgcolor="#F2F2F2", font_family="Verdana", font_color="#000000", showlegend=False, hovermode=False)
    figure.update_traces(marker=dict(color=colors,line=dict(color="#000000",width=2)), text=text_labels, textposition="outside")
    figure.update_layout(font_family="Verdana",font_color="#000000")
    return figure



##-------create static data-----------------------------------------------------
# beverage options
set_beverage_options = [{"label":i,"value":i} for i in df_drinks["Beverage"].unique()]


# map figure
figure_map = px.scatter_geo(data_frame=df_map,lat="Latitude",lon="Longitude",color="Ownership Type",color_discrete_map={"Licensed":"#293644","Joint Venture":"#C08552","Company Owned":"#774936","Franchise":"#629AA1"},hover_name="Store Name",hover_data={"Address":True,"Phone Number":True,"Ownership Type":False,"Longitude":False,"Latitude":False},template="ggplot2")
figure_map.update_layout(margin={"t":0,"r":0,"b":0,"l":0})
figure_map.update_layout({"plot_bgcolor":"rgba(0,0,0,0)","paper_bgcolor":"rgba(0,0,0,0)"})
figure_map.update_layout(legend={"title":"","orientation":"h","xanchor":"center","x":0.5,"yanchor":"bottom","y":1,"bgcolor":"rgba(0,0,0,0)"})



##-------------layout-----------------------------------------------------------
app = dash.Dash()

app.layout = html.Div(
    style={"width":"55%",
           "margin":"auto",
           "background-color":"#006241",
           "padding":"2rem",
           "font-family":"Verdana"},
    children=[
        #header
        html.Div(className="dashboard-header",
                 style={"text-align":"center",
                        "margin-bottom":"100px",
                        "padding-top":"120px"},
                 children=[html.H1("Drink a Smarter Starbucks",
                                   style={"color":"#FFFFFF",
                                          "font-weight":"bold",
                                          "font-size":"80px",
                                          "letter-spacing":"5px",
                                          "margin-bottom":"20px"}),
                           html.P("Discover what’s in your cup, one sip (and dataset) at a time.",
                                  style={"font-size":"24px",
                                         "font-weight":"lighter",
                                         "color":"#DFF9BA"})]),

        #section 1: customization
        html.Div(
            style={"background-color":"#FFFFFF",
                   "border-radius":"12px",
                   "padding":"2rem",
                   "margin-bottom":"100px",
                   "box-shadow":"0 2px 10px rgba(0,0,0,0.1)"},
            children=[html.H2("1️⃣ Customize Your Drink",
                              style={"color":"#000000",
                                     "margin-bottom":"10px"}),
                      html.P("Pick your go-to Starbucks beverage and make it yours.",
                             style={"color":"#000000",
                                    "margin-bottom":"20px"}),
                      dcc.Dropdown(id="beverage_dropdown",
                                   options=set_beverage_options,
                                   placeholder="Select a beverage",
                                   style={"width":"85%",
                                          "margin-bottom":"10px"}),
                      html.Div(children=[html.Div(id="size_text",
                                                  style={"font-style": "italic"}),
                                         dcc.RadioItems(id="size_dropdown",
                                                        style={"margin-bottom":"10px"})]),
                      html.Div(children=[html.Div(id="milk_text",
                                                  style={"font-style": "italic"}),
                                         dcc.RadioItems(id="milk_dropdown",
                                                        style={"margin-bottom":"20px"},)]),
                      html.Div(id="drink_order",
                               style={"text-align":"center",
                                      "font-weight":"bold",
                                      "color":"#1E3932",
                                      "font-size":"20px"})]),

        #section 2: results
        html.Div(
            style={"background-color":"#FFFFFF",
                   "border-radius":"12px",
                   "padding":"2rem",
                   "margin-bottom":"100px",
                   "box-shadow":"0 2px 10px rgba(0,0,0,0.1)"},
            children=[html.H2("2️⃣ Check Out the Nutritional Content",
                              style={"color":"#000000",
                                     "margin-bottom":"10px"}),
                      html.P("See what’s really brewing inside — calories, caffeine and more.",
                             style={"color":"#000000",
                                    "margin-bottom":"20px"}),
                      html.Div(style={"display":"flex",
                                      "justify-content":"center",
                                      "align-items":"center",
                                      "gap":"40px",
                                      "margin-bottom":"20px",
                                      "font-weight":"bold"},
                               children=[html.Div(id="calories_output"),
                                         html.Div(id="caffeine_output")]),
                      dcc.Graph(id="nutrition_output")]),

        #section 3: map
        html.Div(
            style={"background-color":"#FFFFFF",
                   "border-radius":"12px",
                   "padding":"2rem",
                   "box-shadow":"0 2px 10px rgba(0,0,0,0.1)"},
            children=[html.H2("3️⃣ Find Your Nearest Location",
                              style={"color":"#000000",
                                     "margin-bottom":"10px"}),
                      html.P("Craving it now? Locate your closest Starbucks and sip smarter in person.",
                             style={"color":"#000000",
                                    "margin-bottom":"20px"}),
                      dcc.Graph(id="map", figure=figure_map)])])



##------------call backs--------------------------------------------------------
# update size options
@app.callback(
    [Output("size_text","children"),
     Output("size_dropdown","options")],
    [Input("beverage_dropdown","value")])

def set_size_options(selected_beverage):
    if (selected_beverage is None):
        text = ""

    else:
        text = "Select a size:"

    dropdown = [{"label":i, "value":i} for i in df_drinks[df_drinks["Beverage"]==selected_beverage]["Size"].unique()]

    return text, dropdown


# update milk options
@app.callback(
    [Output("milk_text","children"),
     Output("milk_dropdown","options")],
    [Input("size_dropdown","value"),
     Input("beverage_dropdown","value")])

def set_milk_options(selected_size,selected_beverage):
    if (selected_size is None)|(selected_beverage is None):
        text = ""

    else:
        text = "Select a milk:"

    dropdown = [{"label":i, "value":i} for i in df_drinks[(df_drinks["Size"]==selected_size) & (df_drinks["Beverage"]==selected_beverage)]["Milk"].unique()]

    return text, dropdown


# update selected drink
@app.callback(
    Output(component_id="drink_order",component_property="children"),
    [Input(component_id="size_dropdown",component_property="value"),
     Input(component_id="beverage_dropdown",component_property="value"),
     Input(component_id="milk_dropdown",component_property="value")])

def update_drink_output(selected_size,selected_beverage,selected_milk):
    if (selected_size is None)|(selected_beverage is None)|(selected_milk is None):
        drink ="You have not made or completed your drink order."

    else:
        drink ="Your drink order is a {size} {beverage} with {milk}.".format(size=selected_size, beverage=selected_beverage, milk=selected_milk)

    return drink


# update nutrition
@app.callback(
    [Output(component_id="calories_output",component_property="children"),
     Output(component_id="caffeine_output",component_property="children"),
     Output(component_id="nutrition_output",component_property="figure")],
    [Input(component_id="beverage_dropdown",component_property="value"),
     Input(component_id="size_dropdown",component_property="value"),
     Input(component_id="milk_dropdown",component_property="value")])

def update_nutritional_figures(selected_beverage,selected_size,selected_milk):
    if (selected_beverage is None)|(selected_size is None)|(selected_milk is None):
        df_empty = pd.DataFrame([["Total Fat (g)",0],["Total Carbohydrates (g)",0],["Sugars (g)",0],["Protein (g)",0]], columns=["Nutrition","Amount"])

        calories = "0 calories"
        caffeine = "0 mg of caffeine"

        nutrition = draw_bar(df_empty)

    else:
        df_selection = df_drinks[(df_drinks["Beverage"]==selected_beverage) & (df_drinks["Size"]==selected_size) & (df_drinks["Milk"]==selected_milk)]

        calories = "{} calories".format(df_selection["Calories"].iloc[0])
        caffeine = "{} mg of caffeine".format(df_selection["Caffeine (mg)"].iloc[0])

        df_selection = df_selection[["Total Fat (g)","Total Carbohydrates (g)","Sugars (g)","Protein (g)"]]
        df_selection = df_selection.melt(var_name="Nutrition", value_name="Amount")
        nutrition = draw_bar(df_selection)

    return calories, caffeine, nutrition



##-----------run----------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
