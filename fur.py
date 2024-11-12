import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

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
    ], style={'width': '50%', 'display': 'inline-block'}),

    # Выпадающий список для выбора предмета (для таблицы)
    html.Div([
        html.Label("Выберите предмет для таблицы:"),
        dcc.Dropdown(
            id='subject-dropdown-table',
            options=[{'label': 'Все', 'value': 'Все'}] + [{'label': subj, 'value': subj} for subj in
                                                          data['Предмет'].unique()],
            value='Все',
            clearable=False,
        ),
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Br(),

    # Таблица с полным списком студентов
    html.Div(id='grades-table', style={'marginTop': '20px'}),

    # Два отступа после таблицы
    html.Br(),
    html.Br(),

    # Выпадающий список для выбора предмета (для диаграммы)
    html.Div([
        html.Label("Выберите предмет для диаграммы:"),
        dcc.Dropdown(
            id='subject-dropdown-chart',
            options=[{'label': subj, 'value': subj} for subj in data['Предмет'].unique()],
            value=data['Предмет'].unique()[0],  # Устанавливаем значение по умолчанию на первый предмет
            clearable=False,
        ),
    ], style={'width': '100%', 'display': 'block', 'marginBottom': '20px'}),  # Устанавливаем ширину на 100%

    # Диаграмма успеваемости студентов по предметам
    dcc.Graph(id='performance-chart')
], style={'width': '100%', 'height': '100vh'})  # Устанавливаем ширину и высоту на весь экран


# Функция для генерации таблицы
def generate_table(dataframe):
    return html.Table([
        # Заголовки столбцов
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns], style={'border': '1px solid black'})
        ),
        # Тело таблицы
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], style={'border': '1px solid black'}) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ], style={'width': '100%', 'borderCollapse': 'collapse'})  # Полная ширина таблицы


# Изначально отображаем полный список студентов и диаграмму
@app.callback(
    [Output('grades-table', 'children'),
     Output('performance-chart', 'figure')],
    [Input('fio-dropdown', 'value'),
     Input('subject-dropdown-table', 'value'),
     Input('subject-dropdown-chart', 'value')]
)
def update_table(selected_fio, selected_subject_table, selected_subject_chart):
    filtered_data = data.copy()

    if selected_fio != 'Все':
        filtered_data = filtered_data[filtered_data['ФИО'] == selected_fio]

    if selected_subject_table != 'Все':
        filtered_data = filtered_data[filtered_data['Предмет'] == selected_subject_table]

    table = generate_table(filtered_data)

    # Фильтрация данных для диаграммы по выбранному предмету
    performance_data = data[data['Предмет'] == selected_subject_chart]

    if not performance_data.empty:
        fig = px.bar(performance_data,
                     x='ФИО',
                     y='Оценка',  # Предполагаем, что у вас есть колонка "Оценка"
                     color='Предмет',
                     title=f"Успеваемость студентов по предмету: {selected_subject_chart}")

        fig.update_layout(title_x=0.5)  # Центрируем заголовок диаграммы
    else:
        fig = px.bar(title="Нет данных для отображения")

    return table, fig


# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)