# Hurtownia Danych -  Uni project

This project is an interactive data analytics dashboard for sales data, created as a university project. It enables users to explore, filter, and visualize key sales metrics and trends from a data warehouse using a modern, responsive web interface.

---

## Features

- **Interactive Filtering:**  
  Filter data by year, sales category, sales channel, and price range using sidebar dropdowns.

- **Brutto/Netto Toggle:**  
  Instantly switch between gross (brutto) and net (netto) sales values.

- **Key Performance Indicators (KPIs):**  
  View real-time cards for:
    - Total sales
    - Average basket value
    - Number of transactions
    - Top brand

- **Rich Visualizations:**  
    - Sales trends over months and years (line chart)
    - Sales by season and month (bar chart)
    - Sales by country (bar chart)
    - Sales by weekday (bar chart)
    - Brand market share (pie chart)
    - Sales distribution by price range (bar chart)
    - Top 3 product categories (bar chart)
    - Geographic sales map (choropleth)

- **Auto-Refresh:**  
  Dashboard data refreshes automatically every 30 seconds to ensure up-to-date insights.

---

## Tech Stack

- **Python 3.x**
- [Dash](https://dash.plotly.com/) (Plotly)
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express & Graph Objects](https://plotly.com/python/)
- [SQLAlchemy](https://www.sqlalchemy.org/) & [pyodbc](https://github.com/mkleehammer/pyodbc) (for SQL Server database connection)
- [mlxtend](http://rasbt.github.io/mlxtend/) (for association rules, if extended)
- Microsoft SQL Server (cloud-hosted)

---

1. **Install Dependencies**
    ```
    pip install dash dash-bootstrap-components pandas plotly sqlalchemy pyodbc mlxtend
    ```

2. **Configure Database Connection**
    - The app connects to a remote SQL Server using SQLAlchemy and pyodbc.
    - Connection details are set in the code:
      ```
      mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes
      ```
    - You may need to adjust credentials or server details for your environment.

3. **Run the Application**
    ```
    python <dashboard>.py
    ```
    - By default, Dash runs on [http://127.0.0.1:8050](http://127.0.0.1:8050).

---

## Usage

- Use the sidebar to filter data by year, sales category, sales channel, and price range.
- Toggle between netto and brutto values.
- Explore KPIs and visualizations to analyze sales performance, trends, and breakdowns.
- The dashboard auto-updates every 30 seconds.

---

## Project Structure

- `dashboard.py`: Main dashboard application.
- SQL data source: Cloud-hosted SQL Server with a view `[dbo].[VisualizationView]` containing cleaned and joined sales data.

---

## Screenshots

![image](https://github.com/user-attachments/assets/824c84dd-3a1a-415b-80ec-f5ff7fe55486)
![491216842_568246972469506_8180322624816582191_n](https://github.com/user-attachments/assets/dd1be55e-88b4-4026-9010-1fd0c06bbdfb)
![image](https://github.com/user-attachments/assets/28d90008-435a-4edf-8e07-4893d581f92c)



