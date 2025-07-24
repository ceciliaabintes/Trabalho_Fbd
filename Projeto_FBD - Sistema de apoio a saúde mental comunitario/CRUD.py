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

def get_users_df(filter_text=""):
    query = """
    SELECT 
        p.CPF AS cpf,
        p.Nome AS nome,
        p.Email AS email,
        u.DataNascim AS datanascim,
        u.Rua AS rua,
        u.Bairro AS bairro,
        u.Cidade AS cidade,
        u.Estado AS estado
    FROM 
        Pessoa p
    JOIN 
        Usuario u ON p.CPF = u.CPF
    """
    if filter_text:
        query += f" WHERE p.Nome ILIKE '%%{filter_text}%%' OR p.Email ILIKE '%%{filter_text}%%'"
    
    query += " ORDER BY p.Nome;"

    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query), connection)
        
        if not df.empty:
            df['datanascim'] = pd.to_datetime(df['datanascim']).dt.strftime('%d/%m/%Y')
        return df
    except Exception as e:
        pn.state.notifications.error(f'Erro ao buscar usuários: {e}')
        return pd.DataFrame()

def add_user(cpf, nome, email, datanascim, rua, bairro, cidade, estado): ##funcao p adicionar usuario
    today = datetime.date.today()
    age = today.year - datanascim.year - ((today.month, today.day) < (datanascim.month, datanascim.day))
    if age < 16:
        pn.state.notifications.error('Erro: O usuário deve ser maior de 16 anos.') ##
        return

    insert_pessoa = text("INSERT INTO Pessoa (CPF, Nome, Email) VALUES (:cpf, :nome, :email)")
    insert_usuario = text("INSERT INTO Usuario (CPF, Rua, Bairro, Cidade, Estado, DataNascim) VALUES (:cpf, :rua, :bairro, :cidade, :estado, :datanascim)")

    with engine.begin() as connection:
        try:
            connection.execute(insert_pessoa, {"cpf": cpf, "nome": nome, "email": email})
            connection.execute(insert_usuario, {"cpf": cpf, "rua": rua, "bairro": bairro, "cidade": cidade, "estado": estado, "datanascim": datanascim})
            pn.state.notifications.success(f'Usuário {nome} adicionado com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao adicionar usuário: {e}')

def update_user(cpf, nome, email, datanascim, rua, bairro, cidade, estado):
    update_pessoa = text("UPDATE Pessoa SET Nome = :nome, Email = :email WHERE CPF = :cpf")
    update_usuario = text("UPDATE Usuario SET Rua = :rua, Bairro = :bairro, Cidade = :cidade, Estado = :estado, DataNascim = :datanascim WHERE CPF = :cpf")

    with engine.begin() as connection:
        try:
            connection.execute(update_pessoa, {"nome": nome, "email": email, "cpf": cpf})
            connection.execute(update_usuario, {"rua": rua, "bairro": bairro, "cidade": cidade, "estado": estado, "datanascim": datanascim, "cpf": cpf})
            pn.state.notifications.success(f'Usuário {nome} atualizado com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao atualizar usuário: {e}')

def delete_user(cpf):
    delete_acessa = text("DELETE FROM Acessa WHERE CPF = :cpf")
    delete_atendimento = text("DELETE FROM Atendimento WHERE CPF = :cpf")
    delete_telefone = text("DELETE FROM Usuario_Telefone WHERE CPF = :cpf")
    delete_usuario = text("DELETE FROM Usuario WHERE CPF = :cpf")
    delete_pessoa = text("DELETE FROM Pessoa WHERE CPF = :cpf")

    with engine.begin() as connection:
        try:
            connection.execute(delete_acessa, {"cpf": cpf})
            connection.execute(delete_atendimento, {"cpf": cpf})
            connection.execute(delete_telefone, {"cpf": cpf})
            connection.execute(delete_usuario, {"cpf": cpf})
            connection.execute(delete_pessoa, {"cpf": cpf})
            pn.state.notifications.success(f'Usuário com CPF {cpf} removido com sucesso!')
        except Exception as e:
            pn.state.notifications.error(f'Erro ao remover usuário: {e}')

pn.extension('tabulator', notifications=True)
##input do usuario (cadastro)
cpf_input = pn.widgets.TextInput(name='CPF', placeholder='123.456.789-00', max_length=14, width=380)
nome_input = pn.widgets.TextInput(name='Nome Completo', placeholder='Digite o nome completo', width=380)
email_input = pn.widgets.TextInput(name='E-mail', placeholder='usuario@email.com', width=380)
datanascim_input = pn.widgets.DatePicker(name='Data de Nascimento', width=380)
rua_input = pn.widgets.TextInput(name='Rua', placeholder='Ex: Rua das Flores, 123', width=380)
bairro_input = pn.widgets.TextInput(name='Bairro', placeholder='Ex: Centro', width=380)
cidade_input = pn.widgets.TextInput(name='Cidade', placeholder='Ex: São Paulo', width=380)
estado_input = pn.widgets.TextInput(name='Estado', placeholder='Ex: SP', max_length=2, width=380)

add_button = pn.widgets.Button(name='Salvar Novo Usuário', button_type='primary')
update_button = pn.widgets.Button(name='Atualizar Usuário Selecionado', button_type='primary', disabled=True)
delete_button = pn.widgets.Button(name='Remover Usuário Selecionado', button_type='danger', disabled=True)
clear_button = pn.widgets.Button(name='Limpar Formulário', button_type='light')

tabulator = pn.widgets.Tabulator(
    get_users_df(), 
    layout='fit_data_table', 
    pagination='remote', 
    page_size=10,
    selectable=1, 
    header_filters=True,
    hidden_columns=['cpf']
)

filter_input = pn.widgets.TextInput(placeholder='Filtrar por nome ou e-mail')

def clear_form(*events):
    cpf_input.value = ''
    nome_input.value = ''
    email_input.value = ''
    datanascim_input.value = None
    rua_input.value = ''
    bairro_input.value = ''
    cidade_input.value = ''
    estado_input.value = ''
    cpf_input.disabled = False
    update_button.disabled = True
    delete_button.disabled = True
    tabulator.selection = []

def filter_table(event):
    tabulator.value = get_users_df(event.new)

filter_input.param.watch(filter_table, 'value')

def load_selection(event):
    if not event.new:
        clear_form()
        return

    selected_row_index = event.new[0]
    selected_user = tabulator.value.iloc[selected_row_index]

    cpf_input.value = selected_user['cpf']
    cpf_input.disabled = True
    nome_input.value = selected_user['nome']
    email_input.value = selected_user['email']
    datanascim_input.value = datetime.datetime.strptime(selected_user['datanascim'], '%d/%m/%Y').date()
    rua_input.value = selected_user['rua']
    bairro_input.value = selected_user['bairro']
    cidade_input.value = selected_user['cidade']
    estado_input.value = selected_user['estado']

    update_button.disabled = False
    delete_button.disabled = False

tabulator.param.watch(load_selection, 'selection')

def add_user_callback(event):
    if not all([cpf_input.value, nome_input.value, email_input.value, datanascim_input.value]):
        pn.state.notifications.warning('Por favor, preencha todos os campos obrigatórios (CPF, Nome, E-mail, Data Nasc.).')
        return
    add_user(
        cpf = cpf_input.value,
        nome = nome_input.value,
        email = email_input.value,
        datanascim = datanascim_input.value,
        rua = rua_input.value,
        bairro = bairro_input.value,
        cidade = cidade_input.value,
        estado = estado_input.value.upper()
    )
    tabulator.value = get_users_df(filter_input.value)
    clear_form()

add_button.on_click(add_user_callback)

def update_user_callback(event):
    update_user(
        cpf = cpf_input.value,
        nome = nome_input.value,
        email = email_input.value,
        datanascim = datanascim_input.value,
        rua = rua_input.value,
        bairro = bairro_input.value,
        cidade = cidade_input.value,
        estado = estado_input.value.upper()
    )
    tabulator.value = get_users_df(filter_input.value)
    clear_form()

update_button.on_click(update_user_callback)

def delete_user_callback(event):
    cpf_to_delete = cpf_input.value
    delete_user(cpf_to_delete)
    tabulator.value = get_users_df(filter_input.value)
    clear_form()

delete_button.on_click(delete_user_callback)
clear_button.on_click(clear_form)

form_card = pn.Card(
    pn.Column(
        cpf_input,
        nome_input,
        email_input,
        datanascim_input,
        rua_input,
        bairro_input,
        cidade_input,
        estado_input,
        pn.Row(add_button, update_button),
        pn.Row(delete_button, clear_button)
    ),
    title = 'Formulário de Usuário',
    collapsed = False
)

template = pn.template.FastListTemplate(
    site = "Gestão de Usuários",
    title = "Saúde Mental Comunitária",
    sidebar = [form_card],
    main = [
        pn.Column(
            pn.pane.Markdown("### Usuários Cadastrados"),
            pn.Row(
                pn.pane.Markdown("#### Filtrar:"),
                filter_input,
                align='center'
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