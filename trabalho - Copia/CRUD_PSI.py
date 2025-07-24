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

def get_psychologists_df(filter_text=""):
    query = """
    SELECT 
        p.CPF AS cpf,
        p.Nome AS nome,
        p.Email AS email,
        ps.CRP AS crp,
        ps.Data_nascimento AS data_nascimento,
        (SELECT Telefone FROM Psicologo_Telefone WHERE CRP = ps.CRP LIMIT 1) AS telefone
    FROM 
        Pessoa p
    JOIN 
        Psicologo ps ON p.CPF = ps.CPF
    """
    if filter_text:
        query += f" WHERE p.Nome ILIKE '%%{filter_text}%%' OR p.Email ILIKE '%%{filter_text}%%' OR ps.CRP ILIKE '%%{filter_text}%%'"
    
    query += " ORDER BY p.Nome;"

    try:
        with engine.connect() as connection:
            df= pd.read_sql(text(query), connection)
        
        if not df.empty and 'data_nascimento' in df.columns:
            df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce').dt.strftime('%d/%m/%Y')
            df.fillna({'data_nascimento': ''}, inplace=True)

        return df
    except Exception as e:
        pn.state.notifications.error(f'Erro ao buscar psicólogos: {e}')
        return pd.DataFrame()

def add_psychologist(cpf, nome, email, crp, telefone, data_nascimento):
    insert_pessoa = text("INSERT INTO Pessoa (CPF, Nome, Email) VALUES (:cpf, :nome, :email)")
    insert_psicologo = text("INSERT INTO Psicologo (CRP, CPF, Nome, Email, Data_nascimento) VALUES (:crp, :cpf, :nome, :email, :data_nascimento)")
    insert_telefone = text("INSERT INTO Psicologo_Telefone (CRP, Telefone) VALUES (:crp, :telefone)")

    with engine.begin() as connection:
        try:
            connection.execute(insert_pessoa, {"cpf": cpf, "nome": nome, "email": email})
            connection.execute(insert_psicologo, {"crp": crp, "cpf": cpf, "nome": nome, "email": email, "data_nascimento": data_nascimento})
            if telefone:
                connection.execute(insert_telefone, {"crp": crp, "telefone": telefone})
            
            pn.state.notifications.success(f'Psicólogo {nome} adicionado com sucesso!')

        except Exception as e:
            pn.state.notifications.error(f'Erro ao adicionar psicólogo: {e}')

def update_psychologist(cpf, nome, email, crp, telefone, data_nascimento):
    update_pessoa = text("UPDATE Pessoa SET Nome = :nome, Email = :email WHERE CPF = :cpf")
    update_psicologo = text("UPDATE Psicologo SET Nome = :nome, Email = :email, Data_nascimento = :data_nascimento WHERE CRP = :crp")
    
    delete_telefone = text("DELETE FROM Psicologo_Telefone WHERE CRP = :crp")
    insert_telefone = text("INSERT INTO Psicologo_Telefone (CRP, Telefone) VALUES (:crp, :telefone)")

    with engine.begin() as connection:
        try:
            connection.execute(update_pessoa, {"nome": nome, "email": email, "cpf": cpf})
            connection.execute(update_psicologo, {"nome": nome, "email": email, "crp": crp, "data_nascimento": data_nascimento})
            
            connection.execute(delete_telefone, {"crp": crp})
            if telefone:
                connection.execute(insert_telefone, {"crp": crp, "telefone": telefone})

            pn.state.notifications.success(f'Psicólogo {nome} atualizado com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao atualizar psicólogo: {e}')

def delete_psychologist(crp, cpf):
    delete_atendimento = text("DELETE FROM Atendimento WHERE CRP = :crp")
    delete_disponibilidade = text("DELETE FROM Disponibilidade WHERE CRP = :crp")
    delete_especialidade = text("DELETE FROM Psicologo_Especialidade WHERE CRP = :crp")
    delete_telefone = text("DELETE FROM Psicologo_Telefone WHERE CRP = :crp")
    delete_psicologo = text("DELETE FROM Psicologo WHERE CRP = :crp")
    delete_pessoa = text("DELETE FROM Pessoa WHERE CPF = :cpf")

    with engine.begin() as connection:
        try:
            connection.execute(delete_atendimento, {"crp": crp})
            connection.execute(delete_disponibilidade, {"crp": crp})
            connection.execute(delete_especialidade, {"crp": crp})
            connection.execute(delete_telefone, {"crp": crp})
            connection.execute(delete_psicologo, {"crp": crp})
            connection.execute(delete_pessoa, {"cpf": cpf})
            pn.state.notifications.success(f'Psicólogo com CRP {crp} removido com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao remover psicólogo: {e}')

pn.extension('tabulator', notifications=True)

crp_input = pn.widgets.TextInput(name='CRP', placeholder='Ex: CRP/01-12345', width=380)
cpf_input = pn.widgets.TextInput(name='CPF', placeholder='123.456.789-00', max_length=14, width=380)
nome_input = pn.widgets.TextInput(name='Nome Completo', placeholder='Digite o nome completo', width=380)
email_input = pn.widgets.TextInput(name='E-mail', placeholder='psicologo@email.com', width=380)
datanascim_input = pn.widgets.DatePicker(name='Data de Nascimento', width=380)
telefone_input = pn.widgets.TextInput(name='Telefone', placeholder='(XX) 9XXXX-XXXX', width=380)

add_button = pn.widgets.Button(name='Salvar Novo Psicólogo', button_type='primary')
update_button = pn.widgets.Button(name='Atualizar Psicólogo', button_type='primary', disabled=True)
delete_button = pn.widgets.Button(name='Remover Psicólogo', button_type='danger', disabled=True)
clear_button = pn.widgets.Button(name='Limpar Formulário', button_type='light')

tabulator = pn.widgets.Tabulator(
    get_psychologists_df(), 
    layout = 'fit_data_table', 
    pagination = 'remote', 
    page_size = 10,
    selectable = 1,
    header_filters = True,
    hidden_columns = ['cpf']
)

filter_input = pn.widgets.TextInput(placeholder='Filtrar por nome, e-mail ou CRP...')

def clear_form(*events):
    crp_input.value = ''
    cpf_input.value = ''
    nome_input.value = ''
    email_input.value = ''
    telefone_input.value = ''
    datanascim_input.value = None
    
    crp_input.disabled = False
    cpf_input.disabled = False
    
    update_button.disabled = True
    delete_button.disabled = True
    tabulator.selection = []

def filter_table(event):
    tabulator.value = get_psychologists_df(event.new)

filter_input.param.watch(filter_table, 'value')

def load_selection(event):
    if not event.new:
        clear_form()
        return

    selected_row_index = event.new[0]
    selected_psy = tabulator.value.iloc[selected_row_index]

    crp_input.value = selected_psy['crp']
    cpf_input.value = selected_psy['cpf']
    nome_input.value = selected_psy['nome']
    email_input.value = selected_psy['email']
    telefone_input.value = selected_psy.get('telefone', '')

    if selected_psy.get('data_nascimento'):
        try:
            datanascim_input.value = datetime.datetime.strptime(selected_psy['data_nascimento'], '%d/%m/%Y').date()
        except (ValueError, TypeError):
            datanascim_input.value = None
    else:
        datanascim_input.value = None

    crp_input.disabled = True
    cpf_input.disabled = True

    update_button.disabled = False
    delete_button.disabled = False

tabulator.param.watch(load_selection, 'selection')

def add_button_callback(event):
    if not all([crp_input.value, cpf_input.value, nome_input.value, email_input.value, datanascim_input.value]):
        pn.state.notifications.warning('Por favor, preencha todos os campos obrigatórios.')
        return
    add_psychologist(
        crp = crp_input.value,
        cpf = cpf_input.value,
        nome = nome_input.value,
        email = email_input.value,
        telefone = telefone_input.value,
        data_nascimento = datanascim_input.value
    )
    tabulator.value = get_psychologists_df(filter_input.value)
    clear_form()

add_button.on_click(add_button_callback)

def update_button_callback(event):
    update_psychologist(
        crp = crp_input.value,
        cpf = cpf_input.value,
        nome = nome_input.value,
        email = email_input.value,
        telefone = telefone_input.value,
        data_nascimento = datanascim_input.value
    )
    tabulator.value = get_psychologists_df(filter_input.value)
    clear_form()

update_button.on_click(update_button_callback)

def delete_button_callback(event):
    delete_psychologist(crp=crp_input.value, cpf=cpf_input.value)
    tabulator.value = get_psychologists_df(filter_input.value)
    clear_form()

delete_button.on_click(delete_button_callback)
clear_button.on_click(clear_form)

form_card = pn.Card(
    pn.Column(
        crp_input,
        cpf_input,
        nome_input,
        email_input,
        datanascim_input,
        telefone_input,
        pn.Row(add_button, update_button),
        pn.Row(delete_button, clear_button)
    ),
    title = 'Formulário de Psicólogo',
    collapsed = False
)

template = pn.template.FastListTemplate(
    site = "Gestão de Psicologos",
    title = "Saúde Mental Comunitária",
    sidebar = [form_card],
    main = [
        pn.Column(
            pn.pane.Markdown("### Psicólogos Cadastrados"),
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
    header_background =  '#2F4F4F',
    header_color = 'white',
    sidebar_width = 400
)

template.servable()