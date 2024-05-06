import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors
import dash
from dash import dcc, html
from dash.dependencies import Input,Output


#------------------------------------------------------------------


# map data
df_map = pd.read_csv("directory.csv")
df_map.drop(df_map.loc[df_map["Brand"]=="Teavana"].index,inplace=True)
df_map["Phone Number"].fillna("n/a",inplace=True)
df_map["Postcode"].fillna(".",inplace=True)
df_map["Address"] = np.where(df_map["Postcode"]==".",(df_map["Street Address"]+", "+df_map["City"]),(df_map["Street Address"]+", "+df_map["City"]+", "+df_map["Postcode"]))
df_map.drop(["Brand","Store Number","Street Address","City","State/Province","Country","Postcode","Timezone"],axis=1,inplace=True)
df_ma = df_map.reindex(columns=["Store Name","Address","Phone Number","Ownership Type","Latitude","Longitude"])

# drinks data
df = pd.read_csv("starbucks_drinkMenu_expanded.csv")
df["Vitamin A (% DV)"] = df["Vitamin A (% DV)"].apply(lambda x:x.split("%")[0])
df["Vitamin C (% DV)"] = df["Vitamin C (% DV)"].apply(lambda x:x.split("%")[0])
df["Calcium (% DV)"] = df["Calcium (% DV)"].apply(lambda x:x.split("%")[0])
df["Iron (% DV)"] = df["Iron (% DV)"].apply(lambda x:x.split("%")[0])
df[["Total Fat (g)","Vitamin A (% DV)","Vitamin C (% DV)","Calcium (% DV)","Iron (% DV)","Caffeine (mg)"]]=df[["Total Fat (g)","Vitamin A (% DV)","Vitamin C (% DV)","Calcium (% DV)","Iron (% DV)","Caffeine (mg)"]].astype("float")
df["Milk"].fillna("No Milk",inplace=True)


#------------------------------------------------------------------


# map figure
figure_map = px.scatter_geo(data_frame=df_map,lat="Latitude",lon="Longitude",color="Ownership Type",color_discrete_map={"Licensed":"#bcbd22","Joint Venture":"#d62728","Company Owned":"#17becf","Franchise":"#1f77b4"},hover_name="Store Name",hover_data={"Address":True,"Phone Number":True,"Ownership Type":False,"Longitude":False,"Latitude":False},template="ggplot2")
figure_map.update_layout(title={"text":"Find your nearest Starbucks","x":0.5,"y":1,"xanchor":"center","yanchor":"top"},font={"size":12})
figure_map.update_layout(margin={"t":0,"r":0,"b":0,"l":0})
figure_map.update_layout({"plot_bgcolor":"rgba(0,0,0,0)","paper_bgcolor":"rgba(0,0,0,0)"})
figure_map.update_layout(legend={"title":"","orientation":"h","x":0.5,"y":0.97,"xanchor":"center","bgcolor":"rgba(0,0,0,0)"})
figure_map.update_layout(font_family="Verdana",font_color="#8ABFA6")


# bar chart
def figure_bar(dataframe):
    colors = plotly.colors.qualitative.Plotly
    text_labels = [str(val) for val in dataframe["Amount"]]
    min_range = int(max(dataframe["Amount"]))+10
    figure = go.Figure(data=[go.Bar(x=dataframe["Nutrition"],y=dataframe["Amount"])])
    figure.update_traces(marker=dict(color=colors,line=dict(color='#262223',width=2)),text=text_labels,textposition="outside",)
    figure.update_layout(yaxis_range=[0,min_range],xaxis_title="",hovermode=False,showlegend=False,plot_bgcolor="#F2F2F2",paper_bgcolor="#F2F2F2")
    figure.update_layout(font_family="Verdana",font_color="#262223")
    return figure


# pie charts
def figure_pie(dataframe,title):
    figure = go.Figure(data=[go.Pie(labels=dataframe.index,values=dataframe["Percent"],title=title)])
    figure.update_traces(marker=dict(colors=["yellow","#F2F2F2"],line=dict(color='#262223',width=2)),sort=False,textposition="inside")
    figure.update_layout(hovermode=False,showlegend=False,margin={"t":10,"r":10,"b":10,"l":10},plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)")
    figure.update_layout(font_family="Verdana",font_color="#F2F2F2",font_size=16)
    return figure


#------------------------------------------------------------------


app = dash.Dash()

app.layout = html.Div([

    html.Div([

        html.H1("STARBUCKS",
        style={"font-family":"Verdana","color":"#F2F2F2","font-weight":"bold","font-size":"46px","letter-spacing":"7px","height":"50px","padding-top":"30px"}),

        html.Div("Customise your drink order and discover its nutritional content.",
        style={"font-family":"Verdana","color":"#8ABFA6","font-weight":"bold","font-size":"20px","text-align":"justify"}),

        dcc.Dropdown(id="category_dropdown",options=[{"label":i,"value":i} for i in df["Category"].unique()],placeholder="Select a category",
        style={"font-family":"Verdana","width":"90%","margin-left":"10px","margin-top":"17px"}),

        dcc.Dropdown(id="beverage_dropdown",placeholder="Select a beverage",
        style={"font-family":"Verdana","width":"90%","margin-left":"10px","margin-top":"17px"}),

        dcc.Dropdown(id="size_dropdown",placeholder="Select a size",
        style={"font-family":"Verdana","width":"90%","margin-left":"10px","margin-top":"17px"}),

        dcc.Dropdown(id="milk_dropdown",placeholder="Select a milk option",
        style={"font-family":"Verdana","width":"90%","margin-left":"10px","margin-top":"17px"}),

        html.Div("Note: this is not an exhaustive list.",
        style={"font-family":"Verdana","color":"#8ABFA6","font-style":"italic","font-size":"12px","margin-top":"9px"})],

    style={"display":"inline-block","width":"37%","margin-top":"50px","margin-left":"50px"}),

    dcc.Graph(id="map_figure",figure=figure_map,
    style={"display":"inline-block","width":"53%","vertical-align":"top","margin-top":"50px","padding-top":"25px","padding-left":"25px"}),

    html.Div(id="drink_output",
    style={"font-family":"Verdana","color":"#F2F2F2","font-weight":"bold","font-size":"20px","text-align":"center","width":"85%","margin-left":"auto","margin-right":"auto"}),

    html.Div([

        html.Div([

            html.Div([

                html.Div([html.Div("CALORIES",style={"background-color":"#017143","padding-top":"7px","padding-bottom":"7px"}),html.Div(id="calories_output",style={"background-color":"#F2F2F2","padding-top":"7px","padding-bottom":"7px"})],
                style={"font-family":"Verdana","text-align":"center","font-size":"18px","border-style":"solid","border-color":"#262223","display":"inline-block","width":"20%","margin-left":"70px","margin-right":"30px"}),

                html.Div([html.Div("CAFFEINE",style={"background-color":"#017143","padding-top":"7px","padding-bottom":"7px"}),html.Div(id="caffeine_output",style={"background-color":"#F2F2F2","padding-top":"7px","padding-bottom":"7px"})],
                style={"font-family":"Verdana","text-align":"center","font-size":"18px","border-style":"solid","border-color":"#262223","display":"inline-block","width":"20%","margin-left":"30px","margin-right":"30px"}),

                html.Div([html.Div("CHOLESTEROL",style={"background-color":"#017143","padding-top":"7px","padding-bottom":"7px"}),html.Div(id="cholesterol_output",style={"background-color":"#F2F2F2","padding-top":"7px","padding-bottom":"7px"})],
                style={"font-family":"Verdana","text-align":"center","font-size":"18px","border-style":"solid","border-color":"#262223","display":"inline-block","width":"20%","margin-left":"30px"})],

            style={"height":"15%"}),

            dcc.Graph(id="nutrition_figure",figure={},
            style={"height":"75%","border-style":"solid","border-color":"#262223"})],

        style={"display":"inline-block","width":"65%","height":"600px","padding-top":"10px","padding-left":"10px"}),

        html.Div([

            html.Div("Recommended Daily Allowance:",
            style={"font-family":"Verdana","color":"#262223","text-align":"center","font-size":"18px"}),

            dcc.Graph(id="vita_figure",figure={},
            style={"height":"20%"}),

            dcc.Graph(id="vitc_figure",figure={},
            style={"height":"20%"}),

            dcc.Graph(id="calci_figure",figure={},
            style={"height":"20%"}),

            dcc.Graph(id="iron_figure",figure={},
            style={"height":"20%"})],

        style={"display":"inline-block","width":"30%","height":"600px","vertical-align":"top"})],

    style={"width":"95%","padding-top":"20px","margin-left":"auto","margin-right":"auto","margin-bottom":"50px"})

],style={"background-color":"#0E5936"})


#------------------------------------------------------------------


#update beverage dropdown options
@app.callback(
    Output("beverage_dropdown","options"),
    [Input("category_dropdown","value")])

def set_beverage_options(selected_category):
    return [{"label":i,"value":i} for i in df[df["Category"]==selected_category]["Beverage"].unique()]


#update size dropdown options
@app.callback(
    Output("size_dropdown","options"),
    [Input("beverage_dropdown","value")])

def set_size_options(selected_beverage):
    return [{"label":i,"value":i} for i in df[df["Beverage"]==selected_beverage]["Size"].unique()]


#update milk dropdown options
@app.callback(
    Output("milk_dropdown","options"),
    [Input("size_dropdown","value"),
     Input("beverage_dropdown","value")])

def set_milk_options(selected_size,selected_beverage):
    return [{"label":i,"value":i} for i in df[(df["Size"]==selected_size)&(df["Beverage"]==selected_beverage)]["Milk"].unique()]


#update chosen drink
@app.callback(
    Output(component_id="drink_output",component_property="children"),
    [Input(component_id="size_dropdown",component_property="value"),
     Input(component_id="beverage_dropdown",component_property="value"),
     Input(component_id="milk_dropdown",component_property="value")])
def update_drink_output(selected_size,selected_beverage,selected_milk):
    if (selected_size is None)|(selected_beverage is None)|(selected_milk is None):
        container="You have not made or completed your drink order."

    else:
        container="Your drink order is a {size} {beverage} with {milk}.".format(size=selected_size,beverage=selected_beverage,milk=selected_milk)

    return container


#update all figures
@app.callback(
    [Output(component_id="calories_output",component_property="children"),
     Output(component_id="caffeine_output",component_property="children"),
     Output(component_id="cholesterol_output",component_property="children"),
     Output(component_id="nutrition_figure",component_property="figure"),
     Output(component_id="vita_figure",component_property="figure"),
     Output(component_id="vitc_figure",component_property="figure"),
     Output(component_id="calci_figure",component_property="figure"),
     Output(component_id="iron_figure",component_property="figure")],
    [Input(component_id="category_dropdown",component_property="value"),
     Input(component_id="beverage_dropdown",component_property="value"),
     Input(component_id="size_dropdown",component_property="value"),
     Input(component_id="milk_dropdown",component_property="value")])

def update_nutritional_figures(selected_category,selected_beverage,selected_size,selected_milk):
    if (selected_category is None)|(selected_beverage is None)|(selected_size is None)|(selected_milk is None):
        df_empty_nutrition = pd.DataFrame([["Total Fat (g)",0],["Trans Fat (g)",0],["Saturated Fat (g)",0],["Sodium (mg)",0],["Total Carbohydrates (g)",0],["Dietary Fibre (g)",0],["Sugars (g)",0],["Protein (g)",0]],columns=["Nutrition","Amount"])
        df_empty_pie = pd.DataFrame(data=[0,100],index=["Vit","Nil"],columns=["Percent"])

        calories = "0 cal"
        caffeine = "0 mg"
        cholesterol = "0 mg"

        figure_nutrition = figure_bar(df_empty_nutrition)

        figure_vita = figure_pie(df_empty_pie,"Vitamin A")

        figure_vitc = figure_pie(df_empty_pie,"Vitamin C")

        figure_calci = figure_pie(df_empty_pie,"Calcium")

        figure_iron = figure_pie(df_empty_pie,"Iron")

    else:
        dff = df[(df["Category"]==selected_category)&(df["Beverage"]==selected_beverage)&(df["Size"]==selected_size)&(df["Milk"]==selected_milk)]

        calories = "{} cal".format(int(dff["Calories"]))
        caffeine = "{} mg".format(int(dff["Caffeine (mg)"]))
        cholesterol = "{} mg".format(int(dff["Cholesterol (mg)"]))

        df_nutrition = dff[["Total Fat (g)","Trans Fat (g)","Saturated Fat (g)","Sodium (mg)","Total Carbohydrates (g)","Dietary Fibre (g)","Sugars (g)","Protein (g)"]]
        df_nutrition = df_nutrition.melt(var_name="Nutrition",value_name="Amount")
        figure_nutrition = figure_bar(df_nutrition)

        df_vita = pd.DataFrame(data=[int(dff["Vitamin A (% DV)"]),100-int(dff["Vitamin A (% DV)"])],index=["Vit","Nil"],columns=["Percent"])
        figure_vita = figure_pie(df_vita,"Vitamin A")

        df_vitc = pd.DataFrame(data=[int(dff["Vitamin C (% DV)"]),100-int(dff["Vitamin C (% DV)"])],index=["Vit","Nil"],columns=["Percent"])
        figure_vitc = figure_pie(df_vitc,"Vitamin C")

        df_calci = pd.DataFrame(data=[int(dff["Calcium (% DV)"]),100-int(dff["Calcium (% DV)"])],index=["Vit","Nil"],columns=["Percent"])
        figure_calci = figure_pie(df_calci,"Calcium")

        df_iron = pd.DataFrame(data=[int(dff["Iron (% DV)"]),100-int(dff["Iron (% DV)"])],index=["Vit","Nil"],columns=["Percent"])
        figure_iron = figure_pie(df_iron,"Iron")

    return calories,caffeine,cholesterol,figure_nutrition,figure_vita,figure_vitc,figure_calci,figure_iron


if __name__ == "__main__":
    app.run_server(debug=True)
