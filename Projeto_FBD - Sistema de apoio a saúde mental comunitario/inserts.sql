-- 1. Tabela Pessoa
INSERT INTO Pessoa (CPF, ID_PESSOA, Nome, Email) VALUES
('111.111.111-11', 101, 'Ana Clara Souza', 'ana.souza@email.com'),
('222.222.222-22', 102, 'Bruno Costa', 'bruno.costa@email.com'),
('333.333.333-33', 103, 'Carla Dias', 'carla.dias@email.com'),
('444.444.444-44', 104, 'Daniel Martins', 'daniel.m@email.com'),
('555.555.555-55', 105, 'Eduarda Lima', 'duda.lima@email.com'),
('666.666.666-66', 106, 'Felipe Alves', 'felipe.alves@email.com'),
('777.777.777-77', 107, 'Gabriela Rocha', 'gabi.rocha@email.com'),
('888.888.888-88', 108, 'Heitor Pereira', 'heitor.p@email.com'),
('999.999.999-99', 109, 'Isabela Santos', 'isa.santos@email.com'),
('000.000.000-00', 110, 'João Mendes', 'joao.mendes@email.com'),
('123.456.789-10', 201, 'Dr. Ricardo Borges', 'ricardo.borges@email.pro'),
('109.876.543-21', 202, 'Dra. Lúcia Guimarães', 'lucia.g@email.pro'),
('234.567.890-12', 203, 'Dr. Marcos Andrade', 'marcos.a@email.pro'),
('210.987.654-32', 204, 'Dra. Vanessa Campos', 'vanessa.c@email.pro'),
('345.678.901-23', 205, 'Dr. Fernando Ribeiro', 'fernando.r@email.pro'),
('321.098.765-43', 206, 'Dra. Beatriz Oliveira', 'beatriz.o@email.pro'),
('456.789.012-34', 207, 'Dr. Otávio Nogueira', 'otavio.n@email.pro'),
('432.109.876-54', 208, 'Dra. Helena Costa', 'helena.c@email.pro'),
('567.890.123-45', 209, 'Dr. Gustavo Ferreira', 'gustavo.f@email.pro'),
('543.210.987-65', 210, 'Dra. Sofia Almeida', 'sofia.a@email.pro');

-- 2. Tabela Usuario
INSERT INTO Usuario (CPF, Rua, Bairro, Cidade, Estado, DataNascim) VALUES
('111.111.111-11', 'Rua das Acácias, 123', 'Jardim das Flores', 'São Paulo', 'SP', '1990-05-15'),
('222.222.222-22', 'Avenida Atlântica, 456', 'Leme', 'Rio de Janeiro', 'RJ', '1988-11-20'),
('333.333.333-33', 'Alameda Santos, 789', 'Paraíso', 'São Paulo', 'SP', '1995-02-10'),
('444.444.444-44', 'Rua do Futuro, 101', 'Graças', 'Recife', 'PE', '2000-07-30'),
('555.555.555-55', 'Rua Duque de Caxias, 112', 'Moinhos de Vento', 'Porto Alegre', 'RS', '1992-09-01'),
('666.666.666-66', 'Avenida Getúlio Vargas, 223', 'Funcionários', 'Belo Horizonte', 'MG', '1985-12-25'),
('777.777.777-77', 'Rua Comendador Araújo, 334', 'Batel', 'Curitiba', 'PR', '1998-03-18'),
('888.888.888-88', 'SQN 308 Bloco C, 445', 'Asa Norte', 'Brasília', 'DF', '1993-06-05'),
('999.999.999-99', 'Rua Frei Caneca, 556', 'Consolação', 'São Paulo', 'SP', '2001-10-12'),
('000.000.000-00', 'Avenida da Abolição, 667', 'Mucuripe', 'Fortaleza', 'CE', '1997-04-08');

-- 3. Tabela Psicologo
INSERT INTO Psicologo (CRP, CPF, Nome, Email) VALUES
('CRP/01-1001', '123.456.789-10', 'Dr. Ricardo Borges', 'ricardo.borges@email.pro'),
('CRP/02-2002', '109.876.543-21', 'Dra. Lúcia Guimarães', 'lucia.g@email.pro'),
('CRP/01-3003', '234.567.890-12', 'Dr. Marcos Andrade', 'marcos.a@email.pro'),
('CRP/03-4004', '210.987.654-32', 'Dra. Vanessa Campos', 'vanessa.c@email.pro'),
('CRP/04-5005', '345.678.901-23', 'Dr. Fernando Ribeiro', 'fernando.r@email.pro'),
('CRP/01-6006', '321.098.765-43', 'Dra. Beatriz Oliveira', 'beatriz.o@email.pro'),
('CRP/05-7007', '456.789.012-34', 'Dr. Otávio Nogueira', 'otavio.n@email.pro'),
('CRP/02-8008', '432.109.876-54', 'Dra. Helena Costa', 'helena.c@email.pro'),
('CRP/01-9009', '567.890.123-45', 'Dr. Gustavo Ferreira', 'gustavo.f@email.pro'),
('CRP/06-1010', '543.210.987-65', 'Dra. Sofia Almeida', 'sofia.a@email.pro');

-- 4. Tabela Usuario_Telefone
INSERT INTO Usuario_Telefone (CPF, Telefone) VALUES
('111.111.111-11', '(11) 98765-4321'),
('222.222.222-22', '(21) 91234-5678'),
('333.333.333-33', '(11) 98888-7777'),
('444.444.444-44', '(81) 99999-6666'),
('555.555.555-55', '(51) 95555-4444'),
('666.666.666-66', '(31) 93333-2222'),
('777.777.777-77', '(41) 92222-1111'),
('888.888.888-88', '(61) 91111-0000'),
('999.999.999-99', '(11) 97777-8888'),
('000.000.000-00', '(85) 96666-9999');

-- 5. Tabela Psicologo_Telefone
INSERT INTO Psicologo_Telefone (CRP, Telefone) VALUES
('CRP/01-1001', '(11) 91122-3344'),
('CRP/02-2002', '(71) 92233-4455'),
('CRP/01-3003', '(11) 93344-5566'),
('CRP/03-4004', '(21) 94455-6677'),
('CRP/04-5005', '(31) 95566-7788'),
('CRP/01-6006', '(11) 96677-8899'),
('CRP/05-7007', '(41) 97788-9900'),
('CRP/02-8008', '(71) 98899-0011'),
('CRP/01-9009', '(11) 99900-1122'),
('CRP/06-1010', '61) 90011-2233');

-- 6. Tabela Especialidade
INSERT INTO Especialidade (ID_ESPECIALIDADE, Nome_Especialidade) VALUES
(1, 'Terapia Cognitivo-Comportamental'),
(2, 'Psicanálise'),
(3, 'Terapia de Casal e Família'),
(4, 'Transtornos de Ansiedade'),
(5, 'Transtornos de Humor (Depressão, Bipolaridade)'),
(6, 'Psicologia Infantil'),
(7, 'Orientação Vocacional e de Carreira'),
(8, 'Gestalt-Terapia'),
(9, 'Manejo de Estresse e Burnout'),
(10, 'Terapia Focada em Mindfulness');

-- 7. Tabela Psicologo_Especialidade
INSERT INTO Psicologo_Especialidade (CRP, ID_ESPECIALIDADE) VALUES
('CRP/01-1001', 1),
('CRP/01-1001', 4),
('CRP/02-2002', 2),
('CRP/01-3003', 4),
('CRP/04-5005', 3),
('CRP/01-6006', 9),
('CRP/05-7007', 6),
('CRP/01-9009', 10),
('CRP/06-1010', 8),
('CRP/02-8008', 5);

-- 8. Tabela MaterialApoio
INSERT INTO MaterialApoio (ID_MATERIAL, Titulo, Tipo, ConteudoURL, Autor) VALUES
(101, '5 Ferramentas da TCC para o Dia a Dia', 'Artigo', 'http://site.com/artigo-tcc', 'Dr. Ricardo Borges'),
(102, 'O Inconsciente na Prática: Conceitos da Psicanálise', 'Vídeo', 'http://googleusercontent.com/youtube.com/psicanalise', 'Dra. Lúcia Guimarães'),
(103, 'Meditação Guiada de 10 Minutos para Foco', 'Áudio', 'http://site.com/audio-mindfulness', 'Dr. Gustavo Ferreira'),
(104, 'Comunicação Não-Violenta no Casamento', 'Artigo', 'http://site.com/artigo-casal', 'Dr. Fernando Ribeiro'),
(105, 'Ansiedade Social: Como Superar o Medo', 'Artigo', 'http://site.com/artigo-ansiedade', 'Dr. Marcos Andrade'),
(106, 'Lidando com a Birra: Um Guia para Pais', 'Vídeo', 'http://googleusercontent.com/youtube.com/birra', 'Dr. Otávio Nogueira'),
(107, 'Sinais de Burnout e Como Pedir Ajuda', 'Artigo', 'http://site.com/artigo-burnout', 'Dra. Beatriz Oliveira'),
(108, 'O que esperar da primeira sessão de terapia?', 'Vídeo', 'http://googleusercontent.com/youtube.com/primeira-sessao', 'Dra. Vanessa Campos'),
(109, 'Entendendo a Ciclotimia e o Transtorno Bipolar', 'Artigo', 'http://site.com/artigo-humor', 'Dra. Helena Costa'),
(110, 'Exercício de Aceitação da Gestalt-Terapia', 'Artigo', 'http://site.com/artigo-gestalt', 'Dra. Sofia Almeida');

-- 9. Tabela Acessa
INSERT INTO Acessa (CPF, ID_MATERIAL) VALUES
('111.111.111-11', 101),
('111.111.111-11', 105),
('222.222.222-22', 102),
('333.333.333-33', 101),
('444.444.444-44', 104),
('555.555.555-55', 108),
('777.777.777-77', 103),
('777.777.777-77', 107),
('888.888.888-88', 109),
('000.000.000-00', 106);

-- 10. Tabela Disponibilidade
INSERT INTO Disponibilidade (ID_DISPONIBILIDADE, DiaSemana, HoraInicio, HoraFim, CRP) VALUES
(1, 'Segunda-feira', '09:00:00', '12:00:00', 'CRP/01-1001'),
(2, 'Segunda-feira', '14:00:00', '18:00:00', 'CRP/01-1001'),
(3, 'Terça-feira', '10:00:00', '14:00:00', 'CRP/02-2002'),
(4, 'Quarta-feira', '08:00:00', '12:00:00', 'CRP/01-3003'),
(5, 'Quarta-feira', '18:00:00', '21:00:00', 'CRP/02-8008'),
(6, 'Quinta-feira', '13:00:00', '17:00:00', 'CRP/01-6006'),
(7, 'Sexta-feira', '09:00:00', '12:00:00', 'CRP/04-5005'),
(8, 'Sexta-feira', '14:00:00', '18:00:00', 'CRP/04-5005'),
(9, 'Sábado', '09:00:00', '13:00:00', 'CRP/01-9009'),
(10, 'Terça-feira', '15:00:00', '19:00:00', 'CRP/06-1010');

-- 11. Tabela Atendimento
INSERT INTO Atendimento (ID_ATENDIMENTO, Data, Hora, Status, ResumoSessao, CPF, CRP) VALUES
(1, '2025-07-21', '10:00:00', 'Realizado', 'Sessão inicial para TCC. Paciente apresentou queixas de ansiedade generalizada.', '111.111.111-11', 'CRP/01-1001'),
(2, '2025-07-28', '10:00:00', 'Agendado', NULL, '111.111.111-11', 'CRP/01-1001'),
(3, '2025-07-22', '15:00:00', 'Realizado', 'Exploração de temas da infância e sua relação com padrões atuais.', '222.222.222-22', 'CRP/02-2002'),
(4, '2025-07-30', '09:00:00', 'Agendado', NULL, '333.333.333-33', 'CRP/01-3003'),
(5, '2025-08-01', '16:00:00', 'Agendado', NULL, '555.555.555-55', 'CRP/04-5005'),
(6, '2025-07-24', '14:00:00', 'Realizado', 'Foco em técnicas de relaxamento e identificação de gatilhos de estresse.', '666.666.666-66', 'CRP/01-6006'),
(7, '2025-08-06', '11:00:00', 'Agendado', NULL, '777.777.777-77', 'CRP/05-7007'),
(8, '2025-07-16', '17:00:00', 'Cancelado', 'Cliente cancelou por imprevisto familiar.', '888.888.888-88', 'CRP/02-8008'),
(9, '2025-07-24', '11:00:00', 'Realizado', 'Prática de mindfulness para atenção plena e redução de pensamentos intrusivos.', '999.999.999-99', 'CRP/01-9009'),
(10, '2025-08-11', '10:00:00', 'Agendado', NULL, '444.444.444-44', 'CRP/01-3003');