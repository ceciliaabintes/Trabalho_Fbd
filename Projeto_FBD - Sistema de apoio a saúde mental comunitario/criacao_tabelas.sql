CREATE TABLE Pessoa (
    CPF VARCHAR(14) PRIMARY KEY,
    ID_PESSOA INT UNIQUE,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Usuario (
    CPF VARCHAR(14) PRIMARY KEY,
    Rua VARCHAR(255),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    Estado CHAR(2),
    DataNascim DATE NOT NULL,
    CONSTRAINT fk_usuario_pessoa FOREIGN KEY (CPF) REFERENCES Pessoa(CPF)
);

CREATE TABLE Usuario_Telefone (
    CPF VARCHAR(14),
    Telefone VARCHAR(20),
    PRIMARY KEY (CPF, Telefone),
    CONSTRAINT fk_telefone_usuario FOREIGN KEY (CPF) REFERENCES Usuario(CPF)
);

CREATE TABLE Psicologo (
    CRP VARCHAR(20) PRIMARY KEY,
    CPF VARCHAR(14) NOT NULL UNIQUE,
    Nome VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT fk_psicologo_pessoa FOREIGN KEY (CPF) REFERENCES Pessoa(CPF)
);

CREATE TABLE Psicologo_Telefone (
    CRP VARCHAR(20),
    Telefone VARCHAR(20),
    PRIMARY KEY (CRP, Telefone),
    CONSTRAINT fk_telefone_psicologo FOREIGN KEY (CRP) REFERENCES Psicologo(CRP)
);

CREATE TABLE Especialidade (
    ID_ESPECIALIDADE INT PRIMARY KEY,
    Nome_Especialidade VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Psicologo_Especialidade (
    CRP VARCHAR(20),
    ID_ESPECIALIDADE INT,
    PRIMARY KEY (CRP, ID_ESPECIALIDADE),
    CONSTRAINT fk_possui_psicologo FOREIGN KEY (CRP) REFERENCES Psicologo(CRP),
    CONSTRAINT fk_possui_especialidade FOREIGN KEY (ID_ESPECIALIDADE) REFERENCES Especialidade(ID_ESPECIALIDADE)
);

CREATE TABLE MaterialApoio (
    ID_MATERIAL INT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL UNIQUE,
    Tipo VARCHAR(50),
    ConteudoURL VARCHAR(255),
    Autor VARCHAR(255)
);

CREATE TABLE Acessa (
    CPF VARCHAR(14),
    ID_MATERIAL INT,
    PRIMARY KEY (CPF, ID_MATERIAL),
    CONSTRAINT fk_acessa_usuario FOREIGN KEY (CPF) REFERENCES Usuario(CPF),
    CONSTRAINT fk_acessa_material FOREIGN KEY (ID_MATERIAL) REFERENCES MaterialApoio(ID_MATERIAL)
);

CREATE TABLE Disponibilidade (
    ID_DISPONIBILIDADE INT PRIMARY KEY,
    DiaSemana VARCHAR(20) NOT NULL,
    HoraInicio TIME NOT NULL,
    HoraFim TIME NOT NULL,
    CRP VARCHAR(20) NOT NULL,
    CONSTRAINT fk_disponibilidade_psicologo FOREIGN KEY (CRP) REFERENCES Psicologo(CRP)
);

CREATE TABLE Atendimento (
    ID_ATENDIMENTO INT PRIMARY KEY,
    Data DATE NOT NULL,
    Hora TIME NOT NULL,
    Status VARCHAR(50),
    ResumoSessao TEXT,
    CPF VARCHAR(14) NOT NULL,
    CRP VARCHAR(20) NOT NULL,
    CONSTRAINT fk_atendimento_usuario FOREIGN KEY (CPF) REFERENCES Usuario(CPF),
    CONSTRAINT fk_atendimento_psicologo FOREIGN KEY (CRP) REFERENCES Psicologo(CRP)
);
Select * from  Atendimento;
update Psicologo_Telefone set telefone = '(61) 90011-2233' where crp = 'CRP/06-1010';