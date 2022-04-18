from shutil import ignore_patterns
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def make_graph(stock_data, revenue_data, stock):
    """
    Function which takes a dataframe with stock data, a dataframe with revenue data,
    and the name of the stock
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# Question One: Use yfinance to Extract Stock Data
tesla = yf.Ticker('TSLA')

tesla_data = tesla.history(period = "max")

tesla_data.reset_index(inplace = True)
tesla_data.head()

# Question Two: Use Webscrapping to Extract Tesla Revenue Data 
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")
tesla_revenue = pd.DataFrame(columns= ['Date', 'Revenue'])
tesla_body = soup.find_all("tbody")[1]

for row in tesla_body.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")

    tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index= True)
    tesla_revenue

tesla_revenue.dropna(inplace = True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail(5)

# Question 3: Use yfinance to Extract Stock Data
gme = yf.Ticker("GME")
gme_data = gme.history(period = "max")
gme_data.reset_index(inplace = True)
gme_data.head(5)


# Question 4: Use Webscrapping to Extract GME Revenue Data
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html5lib")

gme_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])
gme_body = soup.find_all("tbody")[1]

for row in gme_body.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")

    gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue }, ignore_index = True)

gme_revenue.dropna(inplace = True)

gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.tail(5)

# Question 5: Plot Tesla Stock Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')

# Question 6: Plot GameStop Stock Graph
make_graph(gme_data, gme_revenue, 'GameStop')