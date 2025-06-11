#!/usr/bin/env python3
# coding: utf-8

import sqlite3
import hashlib
import datetime
import getpass

DATABASE_NAME = "academia.db"

def criar_conexao():
    return sqlite3.connect(DATABASE_NAME)

def criar_tabelas():
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Membros (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            CPF TEXT UNIQUE NOT NULL,
            Telefone TEXT,
            Endereco TEXT,
            Data_Cadastro TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Treinos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Membro INTEGER NOT NULL,
            Tipo TEXT,
            Descricao TEXT,
            Duracao INTEGER,
            Data_Inicio TEXT,
            FOREIGN KEY (ID_Membro) REFERENCES Membros(ID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pagamentos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Membro INTEGER NOT NULL,
            Valor REAL,
            Data_Pagamento TEXT,
            Status TEXT,
            FOREIGN KEY (ID_Membro) REFERENCES Membros(ID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Historico_Atividades (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Membro INTEGER NOT NULL,
            Atividade TEXT,
            Data TEXT,
            Tempo_Execucao INTEGER,
            FOREIGN KEY (ID_Membro) REFERENCES Membros(ID)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Funcionarios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Cargo TEXT,
            Login TEXT UNIQUE NOT NULL,
            Senha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def verificar_senha(senha_digitada, senha_hash):
    """Verifica se senha digitada corresponde ao hash salvo"""
    return hash_senha(senha_digitada) == senha_hash

# --- Funções CRUD ---

def inserir_membro(nome, cpf, telefone, endereco, data_cadastro):
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Membros (Nome, CPF, Telefone, Endereco, Data_Cadastro)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, telefone, endereco, data_cadastro))
        conn.commit()
        print("Membro cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já cadastrado.")
    finally:
        conn.close()

def listar_membros():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Nome, CPF, Telefone FROM Membros ORDER BY Nome")
    membros = cursor.fetchall()
    conn.close()
    return membros

def buscar_membro_id(id_membro):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Membros WHERE ID = ?", (id_membro,))
    membro = cursor.fetchone()
    conn.close()
    return membro

def atualizar_membro(id_membro, nome, cpf, telefone, endereco):
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Membros SET Nome = ?, CPF = ?, Telefone = ?, Endereco = ?
            WHERE ID = ?
        """, (nome, cpf, telefone, endereco, id_membro))
        conn.commit()
        print("Membro atualizado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já cadastrado em outro membro.")
    finally:
        conn.close()

def excluir_membro(id_membro):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Membros WHERE ID = ?", (id_membro,))
    conn.commit()
    conn.close()
    print("Membro excluído com sucesso!")

def inserir_treino(id_membro, tipo, descricao, duracao, data_inicio):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Treinos (ID_Membro, Tipo, Descricao, Duracao, Data_Inicio)
        VALUES (?, ?, ?, ?, ?)
    """, (id_membro, tipo, descricao, duracao, data_inicio))
    conn.commit()
    conn.close()
    print("Treino cadastrado com sucesso!")

def listar_treinos(id_membro=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    if id_membro:
        cursor.execute("SELECT * FROM Treinos WHERE ID_Membro = ? ORDER BY Data_Inicio DESC", (id_membro,))
    else:
        cursor.execute("SELECT * FROM Treinos ORDER BY Data_Inicio DESC")
    treinos = cursor.fetchall()
    conn.close()
    return treinos

def buscar_treino_id(id_treino):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Treinos WHERE ID = ?", (id_treino,))
    treino = cursor.fetchone()
    conn.close()
    return treino

def atualizar_treino(id_treino, id_membro, tipo, descricao, duracao, data_inicio):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Treinos SET ID_Membro = ?, Tipo = ?, Descricao = ?, Duracao = ?, Data_Inicio = ?
        WHERE ID = ?
    """, (id_membro, tipo, descricao, duracao, data_inicio, id_treino))
    conn.commit()
    conn.close()
    print("Treino atualizado com sucesso!")

def excluir_treino(id_treino):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Treinos WHERE ID = ?", (id_treino,))
    conn.commit()
    conn.close()
    print("Treino excluído com sucesso!")

def inserir_pagamento(id_membro, valor, data_pagamento, status):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Pagamentos (ID_Membro, Valor, Data_Pagamento, Status)
        VALUES (?, ?, ?, ?)
    """, (id_membro, valor, data_pagamento, status))
    conn.commit()
    conn.close()
    print("Pagamento registrado com sucesso!")

def listar_pagamentos(id_membro=None):
    conn = criar_conexao()
    cursor = conn.cursor()
    if id_membro:
        cursor.execute("SELECT * FROM Pagamentos WHERE ID_Membro = ? ORDER BY Data_Pagamento DESC", (id_membro,))
    else:
        cursor.execute("SELECT * FROM Pagamentos ORDER BY Data_Pagamento DESC")
    pagamentos = cursor.fetchall()
    conn.close()
    return pagamentos

def inserir_atividade(id_membro, atividade, data, tempo_execucao):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Historico_Atividades (ID_Membro, Atividade, Data, Tempo_Execucao)
        VALUES (?, ?, ?, ?)
    """, (id_membro, atividade, data, tempo_execucao))
    conn.commit()
    conn.close()
    print("Atividade registrada com sucesso!")

def listar_atividades(id_membro):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Historico_Atividades WHERE ID_Membro = ? ORDER BY Data DESC", (id_membro,))
    atividades = cursor.fetchall()
    conn.close()
    return atividades

def inserir_funcionario(nome, cargo, login, senha):
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        senha_hash = hash_senha(senha)
        cursor.execute("""
            INSERT INTO Funcionarios (Nome, Cargo, Login, Senha)
            VALUES (?, ?, ?, ?)
        """, (nome, cargo, login, senha_hash))
        conn.commit()
        print("Funcionário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Login já utilizado.")
    finally:
        conn.close()

def buscar_funcionario_login(login):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Funcionarios WHERE Login = ?", (login,))
    funcionario = cursor.fetchone()
    conn.close()
    return funcionario

# --- Telas e menus interativos CLI ---

def tela_login():
    print("\n=== LOGIN DO FUNCIONÁRIO ===")
    login = input("Login: ").strip()
    senha = getpass.getpass("Senha: ")
    funcionario = buscar_funcionario_login(login)
    if funcionario and verificar_senha(senha, funcionario[4]):
        print(f"Bem-vindo(a) {funcionario[1]}!\n")
        return True
    print("Login inválido.\n")
    return False

def tela_cadastro_membro():
    print("\n=== CADASTRAR MEMBRO ===")
    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()
    telefone = input("Telefone: ").strip()
    endereco = input("Endereço: ").strip()
    data_cadastro = datetime.date.today().isoformat()
    inserir_membro(nome, cpf, telefone, endereco, data_cadastro)

def menu_membros():
    while True:
        print("\n--- Gestão de Membros ---")
        print("1 - Listar membros")
        print("2 - Cadastrar membro")
        print("3 - Atualizar membro")
        print("4 - Excluir membro")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == '1':
            membros = listar_membros()
            if membros:
                print("\nID | Nome | CPF | Telefone")
                for m in membros:
                    print(f"{m[0]} | {m[1]} | {m[2]} | {m[3]}")
            else:
                print("Nenhum membro cadastrado.")
        elif escolha == '2':
            tela_cadastro_membro()
        elif escolha == '3':
            try:
                id_m = int(input("ID do membro para atualizar: "))
                membro = buscar_membro_id(id_m)
                if not membro:
                    print("Membro não encontrado!")
                    continue
                print(f"Atualizando: {membro[1]} (CPF: {membro[2]})")
                nome = input(f"Nome [{membro[1]}]: ").strip() or membro[1]
                cpf = input(f"CPF [{membro[2]}]: ").strip() or membro[2]
                telefone = input(f"Telefone [{membro[3]}]: ").strip() or membro[3]
                endereco = input(f"Endereço [{membro[4]}]: ").strip() or membro[4]
                atualizar_membro(id_m, nome, cpf, telefone, endereco)
            except ValueError:
                print("ID inválido.")
        elif escolha == '4':
            try:
                id_m = int(input("ID do membro para excluir: "))
                excluir_membro(id_m)
            except ValueError:
                print("ID inválido.")
        elif escolha == '0':
            break
        else:
            print("Opção inválida.")

def tela_gerenciamento_treinos():
    while True:
        print("\n--- Gerenciamento de Treinos ---")
        print("1 - Listar treinos")
        print("2 - Cadastrar treino")
        print("3 - Atualizar treino")
        print("4 - Excluir treino")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == '1':
            try:
                membro_filter = input("Filtrar por ID do membro? (s/n): ").strip().lower()
                if membro_filter == 's':
                    id_m = int(input("ID do membro: "))
                    treinos = listar_treinos(id_m)
                else:
                    treinos = listar_treinos()
                if treinos:
                    print("\nID | ID_Membro | Tipo | Descrição | Duração(min) | Data Início")
                    for t in treinos:
                        print(f"{t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]}")
                else:
                    print("Nenhum treino encontrado.")
            except ValueError:
                print("ID inválido.")
        elif escolha == '2':
            try:
                id_m = int(input("ID do membro: "))
                tipo = input("Tipo do treino: ")
                desc = input("Descrição: ")
                dur = int(input("Duração (min): "))
                data_inicio = input("Data Início (AAAA-MM-DD): ")
                inserir_treino(id_m, tipo, desc, dur, data_inicio)
            except ValueError:
                print("Dados inválidos.")
        elif escolha == '3':
            try:
                id_t = int(input("ID do treino para atualizar: "))
                treino = buscar_treino_id(id_t)
                if not treino:
                    print("Treino não encontrado.")
                    continue
                id_m = int(input(f"ID Membro [{treino[1]}]: ") or treino[1])
                tipo = input(f"Tipo [{treino[2]}]: ") or treino[2]
                desc = input(f"Descrição [{treino[3]}]: ") or treino[3]
                dur = int(input(f"Duração (min) [{treino[4]}]: ") or treino[4])
                data_inicio = input(f"Data Início [{treino[5]}]: ") or treino[5]
                atualizar_treino(id_t, id_m, tipo, desc, dur, data_inicio)
            except ValueError:
                print("Entrada inválida.")
        elif escolha == '4':
            try:
                id_t = int(input("ID do treino para excluir: "))
                excluir_treino(id_t)
            except ValueError:
                print("ID inválido.")
        elif escolha == '0':
            break
        else:
            print("Opção inválida.")

def tela_registro_pagamentos():
    while True:
        print("\n--- Registro de Pagamentos ---")
        print("1 - Listar pagamentos")
        print("2 - Registrar pagamento")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha == '1':
            try:
                filtro = input("Filtrar por ID do membro? (s/n): ").strip().lower()
                if filtro == 's':
                    id_m = int(input("ID do membro: "))
                    pagamentos = listar_pagamentos(id_m)
                else:
                    pagamentos = listar_pagamentos()
                if pagamentos:
                    print("\nID | ID_Membro | Valor | Data Pagamento | Status")
                    for p in pagamentos:
                        print(f"{p[0]} | {p[1]} | {p[2]:.2f} | {p[3]} | {p[4]}")
                else:
                    print("Nenhum pagamento encontrado.")
            except ValueError:
                print("ID inválido.")
        elif escolha == '2':
            try:
                id_m = int(input("ID do membro: "))
                valor = float(input("Valor: "))
                data_pgto = datetime.date.today().isoformat()
                status = input("Status do pagamento: ")
                inserir_pagamento(id_m, valor, data_pgto, status)
            except ValueError:
                print("Entrada inválida.")
        elif escolha == '0':
            break
        else:
            print("Opção inválida.")

def tela_historico_atividades():
    print("\n--- Histórico de Atividades ---")
    try:
        id_m = int(input("ID do membro: "))
        atividades = listar_atividades(id_m)
        if atividades:
            print("\nID | Atividade | Data | Tempo Execução (min)")
            for a in atividades:
                print(f"{a[0]} | {a[2]} | {a[3]} | {a[4]}")
        else:
            print("Nenhuma atividade encontrada para esse membro.")
    except ValueError:
        print("ID inválido.")

def menu_principal():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Gerenciar Membros")
        print("2 - Gerenciar Treinos")
        print("3 - Registrar Pagamentos")
        print("4 - Histórico de Atividades")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == '1':
            menu_membros()
        elif escolha == '2':
            tela_gerenciamento_treinos()
        elif escolha == '3':
            tela_registro_pagamentos()
        elif escolha == '4':
            tela_historico_atividades()
        elif escolha == '0':
            print("Encerrando sistema. Até logo!")
            break
        else:
            print("Opção inválida.")

def criar_admin_default():
    """Cria usuário admin padrão se não existir"""
    admin = buscar_funcionario_login("admin")
    if not admin:
        print("Criando usuário administrador padrão (login: admin, senha: admin)")
        inserir_funcionario("Administrador", "Administrador", "admin", "admin")

def main():
    criar_tabelas()
    criar_admin_default()

    if tela_login():
        menu_principal()
    else:
        print("Não foi possível realizar login. Encerrando.")

if __name__ == "__main__":
    main()

