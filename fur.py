import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Попытка загрузить данные из CSV файла
try:
    data = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/1_q4zKfhrJ3yuSs3T21MNNkhoq2hYIxqErV618Xne5Io/gviz/tq?tqx=out:csv')
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")
    data = pd.DataFrame()  # Создаем пустой DataFrame в случае ошибки

# Создание экземпляра приложения Dash
app = dash.Dash(__name__)


# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)