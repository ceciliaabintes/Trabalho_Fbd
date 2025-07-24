import os
import pandas as pd
import panel as pn
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

try:
    engine = create_engine(DATABASE_URL)
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()

def get_realized_appointment_ids():
    query = "SELECT ID_ATENDIMENTO FROM Atendimento WHERE Status = 'Realizado' ORDER BY ID_ATENDIMENTO"
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query), connection)
            return [None] + sorted(df['id_atendimento'].tolist())
    except Exception as e:
        print(f"Erro ao buscar IDs de atendimento: {e}")
        return [None]

def get_session_summary(appointment_id):
    if not appointment_id:
        return "Selecione um ID de atendimento acima."
    
    query = text("SELECT ResumoSessao FROM Atendimento WHERE ID_ATENDIMENTO = :id")
    try:
        with engine.connect() as connection:
            summary = connection.execute(query, {'id': appointment_id}).scalar()
        return summary or "Nenhum resumo disponível para esta sessão."
    except Exception as e:
        pn.state.notifications.error(f'Erro ao buscar resumo: {e}')
        return "Erro ao carregar o resumo."

pn.extension(notifications=True)

appointment_select = pn.widgets.Select(
    name="Selecione o ID do Atendimento", 
    options=get_realized_appointment_ids(),
    width=400
)

summary_display = pn.pane.Markdown(
    get_session_summary(appointment_select.value),
    min_height=300,
    width=600,
    styles={'background-color': '#2E2E2E', 'border': '1px solid #444', 'padding': '10px', 'border-radius': '5px', 'color': 'white'}
)

def update_summary_display(event):
    selected_id = event.new
    summary_text = get_session_summary(selected_id)
    summary_display.object = summary_text

appointment_select.param.watch(update_summary_display, 'value')

template = pn.template.FastListTemplate(
    site="Consulta de Atendimentos",
    title="Saúde Mental Comunitária",
    sidebar=[],
    main=[
        pn.Column(
            pn.pane.Markdown("## Consulta de Resumo de Atendimento"),
            pn.Spacer(height=20),
            appointment_select,
            pn.Spacer(height=20),
            pn.pane.Markdown("#### Resumo da Sessão (Confidencial)"),
            summary_display,
            align='center'
        )
    ],
    theme = 'dark',
    favicon = 'https://static.vecteezy.com/ti/vetor-gratis/p1/1895427-maos-segurando-cerebro-simbolo-da-saude-mental-gratis-vetor.jpg',
    header_background = '#2F4F4F',
    header_color = 'white'
)

template.servable()
