import yfinance as yf
from datetime import date
import streamlit as st
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objects as go

START = "2017-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast')
stock = st.sidebar.text_input('Symbol', value= 'AAPL')

n_months = st.slider('Months of prediction:', 1, 12)
period = n_months * 30

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace= True)
    return data
  
data_load_state = st.text("Loading data...")
data = load_data(stock)
data_load_state.text("Loading data... done!")

st.subheader("Raw Data")
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= data['Date'], y= data['Open'], name= 'stock_open'))
    fig.add_trace(go.Scatter(x= data['Date'], y= data['Close'], name= "stock_close"))
    fig.layout.update(title_text= 'Time Series data with Rangeslider', xaxis_rangeslider_visible= True)
    st.plotly_chart(fig)

plot_raw_data()


# Predict stock prices with Prophet
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns= {'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods= period)
forecast = m.predict(future)


# Plot the Stock Price Forecast
st.subheader('Stock Price Forecast')
st.write(forecast.tail())

st.write(f"Forecast plot for {n_months} months")
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)


