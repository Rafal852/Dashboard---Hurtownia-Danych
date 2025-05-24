from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mlxtend.frequent_patterns import apriori, association_rules
import pyodbc
from sqlalchemy import create_engine
import datetime

#df_clean = pd.read_excel('cleaned_data.xlsx', engine='openpyxl')

engine = create_engine(
    "mssql+pyodbc://sshrewds_SQLLogin_1:2vm9wmynr4@hd-wsb-2025-g5.mssql.somee.com/hd-wsb-2025-g5?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes"
)

# Load view
df_clean = pd.read_sql("SELECT * FROM [dbo].[VisualizationView]", engine)

#Bootstrap Cyborg theme
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.CYBORG,
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ]
)

def create_kpi_card(title, value, icon, color="#00e39b", growth=None, sparkline_data=None):

    if growth is not None:
        arrow = '▲' if growth > 0 else '▼' if growth < 0 else ''
        growth_color = '#00e39b' if growth > 0 else '#ff0000' if growth < 0 else '#d5dbe0'
        growth_text = f"{arrow} {abs(growth):.1f}%"
    else:
        growth_text = ""
        growth_color = '#d5dbe0'

    card_content = [
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas fa-{icon} fa-2x", style={"color": color}),
                html.Div([
                    html.P(title, className="mb-1", style={"color": "#b7bbc8"}),
                    html.H4(value, className="mb-0", style={"color": "#fff"}),
                    html.Span(growth_text, style={"color": growth_color, "fontSize": "0.9rem"})
                ], style={"marginLeft": "12px"})
            ], style={"display": "flex", "alignItems": "center"})
        ])
    ]
    
    #Sparkline with trend
    if sparkline_data is not None:
        fig = go.Figure(go.Scatter(
            x=list(range(len(sparkline_data))),
            y=sparkline_data,
            mode='lines+markers',
            line=dict(width=2, color=color),
            marker=dict(size=4),
            hoverinfo='none'
        ))
        fig.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=40
        )
        card_content.append(
            dbc.CardFooter(
                dcc.Graph(figure=fig, config={'displayModeBar': False}),
                style={"padding": "0", "backgroundColor": "transparent"}
            )
        )
    
    return dbc.Card(
        card_content,
        style={"backgroundColor": "#22242b", "border": "none", "boxShadow": "0 2px 8px #111"},
        className="mb-3"
    )

    
def brutto_netto_toggle():
    return html.Div([
        dbc.Label("Typ wartości:", className="mr-2", style={"color": "#d5dbe0"}),
        html.Div([
            dbc.Label("Netto", className="mr-2", style={"color": "#d5dbe0"}),
            dbc.Switch(
                id='value-type-toggle',
                value=False,
                className="custom-switch",
                style={"fontSize": 20}
            ),
            dbc.Label("Brutto", className="ml-2", style={"color": "#d5dbe0"}),
        ], style={"display": "flex", "alignItems": "center"}),
        dbc.Tooltip(
            "Przełącz między wartościami netto (bez VAT) i brutto (z VAT)",
            target="value-type-toggle",
            placement="top"
        )
    ], style={"marginBottom": "20px", "display": "flex", "alignItems": "center"})

app.layout = dbc.Container(fluid=True, style={"height": "100vh", "padding": "0"}, children=[
    dbc.Row([
        
        #Sidebar
        dbc.Col([
            html.H2("Hurtownia Danych Dashboard", className="my-4", style={"color": "#d5dbe0", "font-size": "46px", "text-align": "left"}),
            html.Hr(style={"borderColor": "#333"}),
            dbc.Label("Wybierz Rok:", style={"color": "#d5dbe0"}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': y, 'value': y} for y in sorted(df_clean['Rok'].unique())],
                placeholder="Wszystkie lata",
                className="mb-3",
                style={
                        "backgroundColor": "#2f3542",  
                        "color": "#d5dbe0",  
                        "borderColor": "#333",  
                        "borderRadius": "4px",  
                    },
            ),
            dbc.Label("Kategoria Sprzedaży:", style={"color": "#d5dbe0"}),
            dcc.Dropdown(
                id='sales-category-dropdown',
                options=[{'label': c, 'value': c} for c in df_clean['Kategoria sprzedaży'].unique()],
                placeholder="Wszystkie",
                className="mb-3",
                style={
                        "backgroundColor": "#2f3542",  
                        "color": "#d5dbe0",  
                        "borderColor": "#333", 
                        "borderRadius": "4px",  
                    }
            ),
            dbc.Label("Kanał sprzedaży:", style={"color": "#d5dbe0"}),
            dcc.Dropdown(
                id='channel-dropdown',
                options=[{'label': c, 'value': c} for c in df_clean['Kanał sprzedaży'].unique()],
                placeholder="Wszystkie",
                className="mb-3",
                style={
                        "backgroundColor": "#2f3542",  
                        "color": "#d5dbe0",  
                        "borderColor": "#333",  
                        "borderRadius": "4px", 
                    }
            ),
            dbc.Label("Przedział Cenowy:", style={"color": "#d5dbe0"}),
            dcc.Dropdown(
                id='price-range-dropdown',
                options=[{'label': r, 'value': r} for r in df_clean['Przedział cenowy'].unique()],
                placeholder="Wszystkie",
                className="mb-3",
                style={
                        "backgroundColor": "#2f3542",  
                        "color": "#d5dbe0",  
                        "borderColor": "#333", 
                        "borderRadius": "4px",  
                    }
            ),
            html.Hr(style={"borderColor": "#333"}),
            brutto_netto_toggle()
        ], width=2, style={"backgroundColor": "#1b1d26", "height": "100vh", "padding": "24px", "position": "fixed", "left": 0, "top": 0, "bottom": 0, "overflowY": "auto"}),

        dbc.Col([

    #KPI Cards
    dbc.Row([
        dbc.Col(html.Div(id='kpi-total-sales'), width=3),
        dbc.Col(html.Div(id='kpi-basket-value'), width=3),
        dbc.Col(html.Div(id='kpi-transactions'), width=3),
        dbc.Col(html.Div(id='kpi-top-brand'), width=3)
    ], className="mb-4", style={"marginLeft": "0", "marginRight": "0"}),

   #Line chart
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='sales-line-chart', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=12
        )
    ], className="mb-4"),

    #Sales vs Country charts
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='sales-graph', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='country-sales-graph', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        )
    ], className="mb-4 gx-3"), 

    # Weekday vs Brand charts
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='weekday-sales-graph', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='brand-share-graph', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        )
    ], className="mb-4 gx-3"),

    # top3_brand and sales_by_price_range
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.Graph(id='price-range-distribution', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        ),
        dbc.Col(
            html.Div(
                dcc.Graph(id='top5-bar-chart', style={'height': '400px', 'width': '100%'}),
                style={
                    "backgroundColor": "#2e2f38",
                    "borderRadius": "6px",
                    "padding": "8px",
                    "height": "100%",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
                }
            ),
            width=6
        )
    ], className="mb-4 gx-3"),
    
    # Map
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3("Mapa sprzedaży według krajów", className="text-center mb-3", style={"color": "#d5dbe0"}),
                dcc.Graph(id='country-map', style={'height': '800px', 'width': '100%'})
            ],
            style={
                "backgroundColor": "#2e2f38",
                "borderRadius": "6px",
                "padding": "8px",
                "height": "100%",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.5)"
            }),
            width=12
        )
    ])

], width={"size": 10, "offset": 2}, style={"padding": "32px", "backgroundColor": "#23252e", "minHeight": "100vh"})
    ], style={"margin": "0"}),

    #Interval 30s:
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  
        n_intervals=0
    )
    
])

@app.callback([
    Output('sales-line-chart', 'figure'),
    Output('sales-graph', 'figure'),
    Output('country-sales-graph', 'figure'),
    Output('weekday-sales-graph', 'figure'),
    Output('brand-share-graph', 'figure'),
    Output('country-map', 'figure'),
    Output('kpi-total-sales', 'children'),
    Output('kpi-basket-value', 'children'),
    Output('kpi-transactions', 'children'),
    Output('kpi-top-brand', 'children'),
    Output('price-range-distribution', 'figure'),
    Output('top5-bar-chart', 'figure')
], [
    Input('year-dropdown', 'value'),
    Input('sales-category-dropdown', 'value'),
    Input('channel-dropdown', 'value'),
    Input('price-range-dropdown', 'value'),
    Input('value-type-toggle', 'value'),
    Input('interval-component', 'n_intervals')
])
def update_dashboard(year, category, channel, price_range, is_brutto, n_intervals):

    print(f"Data refreshed from SQL at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    df_clean = pd.read_sql("SELECT * FROM [dbo].[VisualizationView]", engine)
    

    df = df_clean.copy()
    
    if year: df = df[df['Rok'] == year]
    if category: df = df[df['Kategoria sprzedaży'] == category]
    if channel: df = df[df['Kanał sprzedaży'] == channel]
    if price_range: df = df[df['Przedział cenowy'] == price_range]
    value_type = 'Sprzedaż (brutto)' if is_brutto else 'Sprzedaż (netto)'

    #KPIs
    total_sales = df[value_type].sum()
    total_qty = df['Ilość'].sum()
    avg_basket = (total_sales / total_qty) if total_qty else 0
    transactions = df.shape[0]
    top_brand = df.groupby('Marka')[value_type].sum().idxmax() if not df.empty else "-"

    #KPI Cards
    kpi_total_sales = create_kpi_card("Łączna sprzedaż", f"{total_sales:,.2f} zł", "money-bill-wave", "#00e39b")
    kpi_basket_value = create_kpi_card("Średni koszyk", f"{avg_basket:,.2f} zł", "shopping-cart", "#f39c12")
    kpi_transactions = create_kpi_card("Transakcje", f"{transactions}", "receipt", "#3498db")
    kpi_top_brand = create_kpi_card("Top marka", top_brand, "star", "#e74c3c")

    custom_colors = ['#1B9E77', '#D95F02', '#7570B3', '#E7298A', '#66A61E', '#E6AB02', '#A6761D', '#666666']

    #Top 3 Products
    top5_brands = df.groupby('Kategoria produktu')[value_type].sum().sort_values(ascending=False).head(3).reset_index()
    top5_fig = px.bar(
        top5_brands,
        x=value_type,
        y='Kategoria produktu',
        orientation='h',
        title="Top 3 Kategorii Produktu wg Sprzedaży",
        text_auto='.2s',
        color_discrete_sequence=['#E7298A']
        
    )
    top5_fig.update_layout(
        paper_bgcolor='#23252e',
        plot_bgcolor='#23252e',
        font_color='#d5dbe0',
        yaxis=dict(autorange="reversed"),
    )
    
     #Price Range Sales Graph
    sales_by_price_range = df.groupby('Przedział cenowy').agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()

    price_range_fig = px.bar(
        sales_by_price_range, 
        y='Przedział cenowy', 
        x=value_type, 
        orientation='h',
        title="Sprzedaż wg Przedziałów Cenowych",
        hover_data={
            'Przedział cenowy': True,
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },
        color_discrete_sequence=['#E6AB02']
    )
    price_range_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    

    #Line chart: Sales over months, grouped by year
    df_line = df_clean.copy()
    if category: df_line = df_line[df_line['Kategoria sprzedaży'] == category]
    if channel: df_line = df_line[df_line['Kanał sprzedaży'] == channel]
    if price_range: df_line = df_line[df_line['Przedział cenowy'] == price_range]
    value_type_line = value_type
    line_df = df_line.groupby(['Rok', 'Miesiąc']).agg({
        value_type_line: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()
    sales_line_fig = px.line(
        line_df, x='Miesiąc', y=value_type_line, color='Rok',
        markers=True,
        title="Sprzedaż wg miesięcy (grupowanie wg lat)",
        hover_data={
            'Miesiąc': True,
            'Rok': True,
            value_type_line: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },color_discrete_sequence=custom_colors
    )
    sales_line_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    #Sales by month (bar, season)
    sales_month_season = df.groupby(['Miesiąc', 'Sezon']).agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()
    sales_fig = px.bar(
        sales_month_season, x='Miesiąc', y=value_type, color='Sezon',
        title="Miesięczna sprzedaż wg sezonu",
        hover_data={
            'Miesiąc': True,
            'Sezon': True,
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },
        color_discrete_sequence=custom_colors
    )
    sales_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    #Sales by country
    country_sales = df.groupby('Kraj').agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index().sort_values(value_type, ascending=False)
    country_fig = px.bar(
        country_sales, x='Kraj', y=value_type, title="Sprzedaż według kraju",
        hover_data={
            'Kraj': True,
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },
        color_discrete_sequence=custom_colors
    )
    country_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    #Weekday sales
    weekday_sales = df.groupby('Dzień tygodnia').agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()
    weekday_fig = px.bar(
        weekday_sales, x='Dzień tygodnia', y=value_type, title="Sprzedaż wg dnia tygodnia",
        hover_data={
            'Dzień tygodnia': True,
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },
        color_discrete_sequence=['#66A61E']
    )
    weekday_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    #Brand share
    brand_share = df.groupby('Marka').agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()
    brand_fig = px.pie(
        brand_share, names='Marka', values=value_type, title="Udział marek",
        hover_data={
            'Marka': True,
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        },
        color_discrete_sequence=custom_colors
    )
    brand_fig.update_layout(paper_bgcolor='#23252e', plot_bgcolor='#23252e', font_color='#d5dbe0')

    #Map
    map_df = df.groupby(['Kraj', 'Kod kraju']).agg({
        value_type: 'sum',
        'Ilość': 'sum',
        'VAT': 'sum'
    }).reset_index()
    map_df['iso_alpha'] = map_df['Kod kraju']
    map_fig = px.choropleth(
        map_df, locations='iso_alpha', color=value_type, hover_name='Kraj',
        color_continuous_scale=px.colors.sequential.Viridis, projection='natural earth',
        hover_data={
            value_type: ':.2f',
            'Ilość': True,
            'VAT': ':.2f'
        }
    )
    map_fig.update_layout(geo=dict(bgcolor='#23252e'), paper_bgcolor='#23252e', font_color='#d5dbe0')

    return (
        sales_line_fig,
        sales_fig,
        country_fig,
        weekday_fig,
        brand_fig,
        map_fig,
        kpi_total_sales,
        kpi_basket_value,
        kpi_transactions,
        kpi_top_brand,
        price_range_fig,
        top5_fig
    )

if __name__ == '__main__':
    app.run(debug=True)
