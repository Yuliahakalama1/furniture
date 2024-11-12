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

# Определение макета приложения
app.layout = html.Div([
    html.H1("Анализ данных о студентских оценках или успеваемости", style={'textAlign': 'center'}),
    html.Br(),

    # Выпадающий список для выбора ФИО
    html.Div([
        html.Label("Выберите ФИО:"),
        dcc.Dropdown(
            id='fio-dropdown',
            options=[{'label': 'Все', 'value': 'Все'}] + [{'label': fio, 'value': fio} for fio in data['ФИО'].unique()],
            value='Все',
            clearable=False,
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    # Выпадающий список для выбора предмета
    html.Div([
        html.Label("Выберите предмет:"),
        dcc.Dropdown(
            id='subject-dropdown',
            options=[{'label': 'Все', 'value': 'Все'}] + [{'label': subj, 'value': subj} for subj in
                                                          data['Предмет'].unique()],
            value='Все',
            clearable=False,
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Br(),

    # Таблица с полным списком студентов
    html.Div(id='grades-table', style={'marginTop': '20px'})
], style={'width': '100%', 'height': '100vh'})  # Устанавливаем ширину и высоту на весь экран


# Функция для генерации таблицы
def generate_table(dataframe):
    return html.Table([
        # Заголовки столбцов
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns], style={'border': '1px solid black'})
            # Границы для заголовков
        ),
        # Тело таблицы
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], style={'border': '1px solid black'}) for col in dataframe.columns
                # Границы для ячеек
            ]) for i in range(len(dataframe))  # Для каждой строки DataFrame
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse'})  # Полная ширина таблицы и убираем пробелы между границами


# Изначально отображаем полный список студентов
@app.callback(
    Output('grades-table', 'children'),
    Input('fio-dropdown', 'value'),
    Input('subject-dropdown', 'value')
)
def update_table(selected_fio, selected_subject):
    filtered_data = data.copy()

    if selected_fio != 'Все':
        filtered_data = filtered_data[filtered_data['ФИО'] == selected_fio]

    if selected_subject != 'Все':
        filtered_data = filtered_data[filtered_data['Предмет'] == selected_subject]

    return generate_table(filtered_data)


# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)