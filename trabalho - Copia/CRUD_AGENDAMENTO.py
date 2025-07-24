import os
import pandas as pd
import panel as pn
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import datetime

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

def get_users_list():
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text("SELECT Nome, CPF FROM Pessoa JOIN Usuario USING(CPF) ORDER BY Nome"), connection)
            return list(zip(df['Nome'], df['CPF']))
    except Exception:
        return []

def get_psychologists_list():
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text("SELECT Nome, CRP FROM Psicologo ORDER BY Nome"), connection)
            return list(zip(df['Nome'], df['CRP']))
    except Exception:
        return []

def get_appointments_df(filter_text=""):
    query = """
    SELECT
        a.ID_ATENDIMENTO AS id_atendimento,
        a.Data AS data,
        a.Hora AS hora,
        a.Status AS status,
        paciente.Nome AS paciente,
        psicologo.Nome AS psicologo,
        a.CPF AS cpf_paciente,
        a.CRP AS crp_psicologo
    FROM
        Atendimento a
    JOIN
        Usuario u ON a.CPF = u.CPF
    JOIN
        Pessoa paciente ON u.CPF = paciente.CPF
    JOIN
        Psicologo p ON a.CRP = p.CRP
    JOIN
        Pessoa psicologo ON p.CPF = psicologo.CPF
    """
    if filter_text:
        query += f" WHERE paciente.Nome ILIKE '%%{filter_text}%%' OR psicologo.Nome ILIKE '%%{filter_text}%%' OR a.Status ILIKE '%%{filter_text}%%'"
    
    query += " ORDER BY a.Data, a.Hora;"

    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query), connection)
        if not df.empty:
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S').dt.strftime('%H:%M')
        return df
    except Exception as e:
        pn.state.notifications.error(f'Erro ao buscar atendimentos: {e}')
        return pd.DataFrame()

def add_appointment(data, hora, status, cpf_paciente, crp_psicologo):
    try:
        appointment_dt = datetime.datetime.combine(data, datetime.datetime.strptime(hora, '%H:%M').time())
        if appointment_dt <= datetime.datetime.now():
            pn.state.notifications.error('Erro: A data e hora do atendimento devem ser futuras.')
            return
    except ValueError:
        pn.state.notifications.error('Erro: Formato de hora inválido. Use HH:MM.')
        return

    with engine.begin() as connection:
        check_conflict = text("SELECT COUNT(*) FROM Atendimento WHERE CRP = :crp AND Data = :data AND Hora = :hora")
        conflict_count = connection.execute(check_conflict, {"crp": crp_psicologo, "data": data, "hora": hora}).scalar()
        if conflict_count > 0:
            pn.state.notifications.error('Erro: O psicólogo já possui um atendimento neste horário.')
            return

        get_max_id = text("SELECT COALESCE(MAX(ID_ATENDIMENTO), 0) FROM Atendimento")
        new_id = connection.execute(get_max_id).scalar() + 1

        insert_query = text("""
            INSERT INTO Atendimento (ID_ATENDIMENTO, Data, Hora, Status, CPF, CRP)
            VALUES (:id, :data, :hora, :status, :cpf, :crp)
        """)
        try:
            connection.execute(insert_query, {"id": new_id, "data": data, "hora": hora, "status": status, "cpf": cpf_paciente, "crp": crp_psicologo})
            pn.state.notifications.success(f'Atendimento ID {new_id} agendado com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao agendar atendimento: {e}')

def update_appointment(id_atendimento, data, hora, status, cpf_paciente, crp_psicologo):
    with engine.begin() as connection:
        check_conflict = text("SELECT COUNT(*) FROM Atendimento WHERE CRP = :crp AND Data = :data AND Hora = :hora AND ID_ATENDIMENTO != :id")
        conflict_count = connection.execute(check_conflict, {"crp": crp_psicologo, "data": data, "hora": hora, "id": id_atendimento}).scalar()
        if conflict_count > 0:
            pn.state.notifications.error('Erro: O psicólogo já possui outro atendimento neste horário.')
            return
            
        update_query = text("""
            UPDATE Atendimento
            SET Data = :data, Hora = :hora, Status = :status, CPF = :cpf, CRP = :crp
            WHERE ID_ATENDIMENTO = :id
        """)
        try:
            connection.execute(update_query, {"data": data, "hora": hora, "status": status, "cpf": cpf_paciente, "crp": crp_psicologo, "id": id_atendimento})
            pn.state.notifications.success(f'Atendimento ID {id_atendimento} atualizado com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao atualizar atendimento: {e}')

def delete_appointment(id_atendimento):
    with engine.begin() as connection:
        delete_query = text("DELETE FROM Atendimento WHERE ID_ATENDIMENTO = :id")
        try:
            connection.execute(delete_query, {"id": id_atendimento})
            pn.state.notifications.success(f'Atendimento ID {id_atendimento} removido com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao remover atendimento: {e}')

pn.extension('tabulator', notifications=True)

id_atendimento_input = pn.widgets.TextInput(name = 'ID Atendimento', disabled = True, width = 380)
paciente_select = pn.widgets.Select(name = 'Paciente', options = get_users_list(), width = 380)
psicologo_select = pn.widgets.Select(name = 'Psicólogo', options = get_psychologists_list(), width = 380)
data_input = pn.widgets.DatePicker(name = 'Data do Atendimento', width = 380)
hora_input = pn.widgets.TextInput(name = 'Hora (HH:MM)', placeholder = 'Ex: 14:30', width = 380)
status_select = pn.widgets.Select(name = 'Status', options = ['Pendente', 'Confirmado', 'Cancelado', 'Realizado'], width = 380)

add_button = pn.widgets.Button(name = 'Agendar Novo Atendimento', button_type = 'primary')
update_button = pn.widgets.Button(name = 'Atualizar Atendimento', button_type = 'primary', disabled = True)
delete_button = pn.widgets.Button(name = 'Remover Atendimento', button_type = 'danger', disabled = True)
clear_button = pn.widgets.Button(name = 'Limpar Formulário', button_type = 'light')

tabulator = pn.widgets.Tabulator(
    get_appointments_df(),
    layout = 'fit_data_table',
    pagination = 'remote',
    page_size = 10,
    selectable = 1,
    header_filters = True,
    hidden_columns = ['id_atendimento', 'cpf_paciente', 'crp_psicologo']
)

filter_input = pn.widgets.TextInput(placeholder='Filtrar por paciente, psicólogo ou status...')

def clear_form(*events):
    id_atendimento_input.value = ''
    paciente_select.value = None
    psicologo_select.value = None
    data_input.value = None
    hora_input.value = ''
    status_select.value = 'Pendente'
    
    update_button.disabled = True
    delete_button.disabled = True
    tabulator.selection = []

def filter_table(event):
    tabulator.value = get_appointments_df(event.new)

filter_input.param.watch(filter_table, 'value')

def load_selection(event):
    if not event.new:
        clear_form()
        return

    selected_row_index = event.new[0]
    selected_app = tabulator.value.iloc[selected_row_index]
    
    id_atendimento_input.value = str(selected_app['id_atendimento'])
    paciente_select.value = selected_app['cpf_paciente']
    psicologo_select.value = selected_app['crp_psicologo']
    data_input.value = datetime.datetime.strptime(selected_app['data'], '%d/%m/%Y').date()
    hora_input.value = selected_app['hora']
    status_select.value = selected_app['status']

    update_button.disabled = False
    delete_button.disabled = False

tabulator.param.watch(load_selection, 'selection')

def add_button_callback(event):
    if not all([data_input.value, hora_input.value, paciente_select.value, psicologo_select.value]):
        pn.state.notifications.warning('Por favor, preencha todos os campos obrigatórios.')
        return
    add_appointment(
        data = data_input.value,
        hora = hora_input.value,
        status = status_select.value,
        cpf_paciente = paciente_select.value,
        crp_psicologo = psicologo_select.value
    )
    tabulator.value = get_appointments_df(filter_input.value)
    clear_form()

add_button.on_click(add_button_callback)

def update_button_callback(event):
    update_appointment(
        id_atendimento = int(id_atendimento_input.value),
        data = data_input.value,
        hora = hora_input.value,
        status = status_select.value,
        cpf_paciente = paciente_select.value,
        crp_psicologo = psicologo_select.value
    )
    tabulator.value = get_appointments_df(filter_input.value)
    clear_form()

update_button.on_click(update_button_callback)

def delete_button_callback(event):
    delete_appointment(id_atendimento=int(id_atendimento_input.value))
    tabulator.value = get_appointments_df(filter_input.value)
    clear_form()

delete_button.on_click(delete_button_callback)
clear_button.on_click(clear_form)

form_card = pn.Card(
    pn.Column(
        id_atendimento_input,
        paciente_select,
        psicologo_select,
        data_input,
        hora_input,
        status_select,
        pn.Row(add_button, update_button),
        pn.Row(delete_button, clear_button)
    ),
    title = 'Formulário de Atendimento',
    collapsed = False
)

template = pn.template.FastListTemplate(
    site = "Gestão de Atendimentos",
    title = "Saúde Mental Comunitária",
    sidebar = [form_card],
    main = [
        pn.Column(
            pn.pane.Markdown("### Lista de Atendimentos Agendados"),
            pn.Row(
                pn.pane.Markdown("#### Filtrar:"),
                filter_input,
                align = 'center'
            ),
            tabulator
        )
    ],
    theme = 'dark',
    favicon = 'https://static.vecteezy.com/ti/vetor-gratis/p1/1895427-maos-segurando-cerebro-simbolo-da-saude-mental-gratis-vetor.jpg',
    header_background = '#2F4F4F',
    header_color = 'white',
    sidebar_width = 400
)

template.servable()