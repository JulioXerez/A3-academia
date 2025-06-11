
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from functools import partial

# --- Importações do backend ---
from backend import (
    criar_tabelas, criar_admin_default, buscar_funcionario_login,
    verificar_senha, listar_membros, inserir_membro, atualizar_membro,
    excluir_membro, buscar_membro_id, listar_treinos, inserir_treino,
    atualizar_treino, excluir_treino, buscar_treino_id, listar_pagamentos,
    inserir_pagamento, listar_historico_atividades
)

class AcademiaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema da Academia")
        self.root.geometry("800x600")
        self.usuario_logado = None
        self.tela_login()

    def tela_login(self):
        self.limpar_tela()

        frame = tk.Frame(self.root)
        frame.pack(pady=100)

        tk.Label(frame, text="Login").grid(row=0, column=0, sticky='e')
        tk.Label(frame, text="Senha").grid(row=1, column=0, sticky='e')

        self.entry_login = tk.Entry(frame)
        self.entry_senha = tk.Entry(frame, show='*')
        self.entry_login.grid(row=0, column=1)
        self.entry_senha.grid(row=1, column=1)

        tk.Button(frame, text="Entrar", command=self.verificar_login).grid(row=2, columnspan=2, pady=10)

    def verificar_login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()
        funcionario = buscar_funcionario_login(login)
        if funcionario and verificar_senha(senha, funcionario[4]):
            self.usuario_logado = funcionario
            self.menu_principal()
        else:
            messagebox.showerror("Erro", "Login ou senha inválido.")

    def menu_principal(self):
        self.limpar_tela()

        tk.Label(self.root, text=f"Bem-vindo(a), {self.usuario_logado[1]}", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Button(frame, text="Gerenciar Membros", width=20, command=self.tela_gerenciar_membros).pack(pady=5)
        tk.Button(frame, text="Gerenciar Treinos", width=20, command=self.tela_gerenciar_treinos).pack(pady=5)
        tk.Button(frame, text="Gerenciar Pagamentos", width=20, command=self.tela_gerenciar_pagamentos).pack(pady=5)
        tk.Button(frame, text="Histórico de Atividades", width=20, command=self.tela_historico_atividades).pack(pady=5)
        tk.Button(frame, text="Sair", width=20, command=self.root.quit).pack(pady=5)

    # ======================== Membros ========================

    def tela_gerenciar_membros(self):
        self.limpar_tela()

        tk.Label(self.root, text="Gestão de Membros", font=("Arial", 14)).pack(pady=10)

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.tree_membros = ttk.Treeview(frame_top, columns=("ID", "Nome", "CPF", "Telefone"), show='headings')
        for col in ("ID", "Nome", "CPF", "Telefone"):
            self.tree_membros.heading(col, text=col)
        self.tree_membros.pack()

        self.carregar_membros()

        frame_bot = tk.Frame(self.root)
        frame_bot.pack(pady=10)

        tk.Button(frame_bot, text="Cadastrar Novo", command=self.tela_cadastrar_membro).grid(row=0, column=0, padx=5)
        tk.Button(frame_bot, text="Atualizar Selecionado", command=self.tela_atualizar_membro).grid(row=0, column=1, padx=5)
        tk.Button(frame_bot, text="Excluir Selecionado", command=self.excluir_membro).grid(row=0, column=2, padx=5)
        tk.Button(frame_bot, text="Voltar", command=self.menu_principal).grid(row=0, column=3, padx=5)

    def carregar_membros(self):
        for item in self.tree_membros.get_children():
            self.tree_membros.delete(item)
        for membro in listar_membros():
            self.tree_membros.insert('', 'end', values=membro)

    def tela_cadastrar_membro(self):
        self.tela_formulario_membro("Cadastrar Membro", inserir_membro)

    def tela_atualizar_membro(self):
        selecionado = self.tree_membros.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para atualizar.")
            return
        membro_id = self.tree_membros.item(selecionado[0])['values'][0]
        membro = buscar_membro_id(membro_id)
        self.tela_formulario_membro("Atualizar Membro", partial(atualizar_membro, membro_id), membro)

    def excluir_membro(self):
        selecionado = self.tree_membros.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um membro para excluir.")
            return
        membro_id = self.tree_membros.item(selecionado[0])['values'][0]
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este membro?"):
            excluir_membro(membro_id)
            self.carregar_membros()

    def tela_formulario_membro(self, titulo, funcao_salvar, dados=None):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)

        labels = ["Nome", "CPF", "Telefone", "Endereço"]
        entradas = []
        for i, label in enumerate(labels):
            tk.Label(janela, text=label).grid(row=i, column=0)
            entrada = tk.Entry(janela)
            entrada.grid(row=i, column=1)
            if dados:
                entrada.insert(0, dados[i+1])
            entradas.append(entrada)

        def salvar():
            nome = entradas[0].get()
            cpf = entradas[1].get()
            telefone = entradas[2].get()
            endereco = entradas[3].get()
            data_cadastro = datetime.date.today().isoformat()
            if dados:
                funcao_salvar(nome, cpf, telefone, endereco)
            else:
                funcao_salvar(nome, cpf, telefone, endereco, data_cadastro)
            janela.destroy()
            self.carregar_membros()

        tk.Button(janela, text="Salvar", command=salvar).grid(row=len(labels), columnspan=2, pady=10)

    # ======================== Treinos ========================

    def tela_gerenciar_treinos(self):
        self.limpar_tela()

        tk.Label(self.root, text="Gestão de Treinos", font=("Arial", 14)).pack(pady=10)

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.tree_treinos = ttk.Treeview(frame_top, columns=("ID", "Nome do Treino", "Duração", "Descrição"), show='headings')
        for col in ("ID", "Nome do Treino", "Duração", "Descrição"):
            self.tree_treinos.heading(col, text=col)
        self.tree_treinos.pack()

        self.carregar_treinos()

        frame_bot = tk.Frame(self.root)
        frame_bot.pack(pady=10)

        tk.Button(frame_bot, text="Cadastrar Novo Treino", command=self.tela_cadastrar_treino).grid(row=0, column=0, padx=5)
        tk.Button(frame_bot, text="Atualizar Selecionado", command=self.tela_atualizar_treino).grid(row=0, column=1, padx=5)
        tk.Button(frame_bot, text="Excluir Selecionado", command=self.excluir_treino).grid(row=0, column=2, padx=5)
        tk.Button(frame_bot, text="Voltar", command=self.menu_principal).grid(row=0, column=3, padx=5)

    def carregar_treinos(self):
        for item in self.tree_treinos.get_children():
            self.tree_treinos.delete(item)
        for treino in listar_treinos():
            self.tree_treinos.insert('', 'end', values=treino)

    def tela_cadastrar_treino(self):
        self.tela_formulario_treino("Cadastrar Treino", inserir_treino)

    def tela_atualizar_treino(self):
        selecionado = self.tree_treinos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um treino para atualizar.")
            return
        treino_id = self.tree_treinos.item(selecionado[0])['values'][0]
        treino = buscar_treino_id(treino_id)
        self.tela_formulario_treino("Atualizar Treino", partial(atualizar_treino, treino_id), treino)

    def excluir_treino(self):
        selecionado = self.tree_treinos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um treino para excluir.")
            return
        treino_id = self.tree_treinos.item(selecionado[0])['values'][0]
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este treino?"):
            excluir_treino(treino_id)
            self.carregar_treinos()

    def tela_formulario_treino(self, titulo, funcao_salvar, dados=None):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)

        labels = ["Nome do Treino", "Duração (min)", "Descrição"]
        entradas = []
        for i, label in enumerate(labels):
            tk.Label(janela, text=label).grid(row=i, column=0)
            entrada = tk.Entry(janela)
            entrada.grid(row=i, column=1)
            if dados:
                entrada.insert(0, dados[i+1])
            entradas.append(entrada)

        def salvar():
            nome = entradas[0].get()
            duracao = entradas[1].get()
            descricao = entradas[2].get()
            if dados:
                funcao_salvar(nome, duracao, descricao)
            else:
                funcao_salvar(nome, duracao, descricao)  # Adicione data ou outros parâmetros se necessário
            janela.destroy()
            self.carregar_treinos()

        tk.Button(janela, text="Salvar", command=salvar).grid(row=len(labels), columnspan=2, pady=10)

    # ======================== Pagamentos ========================

    def tela_gerenciar_pagamentos(self):
        self.limpar_tela()

        tk.Label(self.root, text="Gestão de Pagamentos", font=("Arial", 14)).pack(pady=10)

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.tree_pagamentos = ttk.Treeview(frame_top, columns=("ID", "Membro", "Valor", "Data"), show='headings')
        for col in ("ID", "Membro", "Valor", "Data"):
            self.tree_pagamentos.heading(col, text=col)
        self.tree_pagamentos.pack()

        self.carregar_pagamentos()

        frame_bot = tk.Frame(self.root)
        frame_bot.pack(pady=10)

        tk.Button(frame_bot, text="Registrar Pagamento", command=self.tela_registrar_pagamento).grid(row=0, column=0, padx=5)
        tk.Button(frame_bot, text="Voltar", command=self.menu_principal).grid(row=0, column=1, padx=5)

    def carregar_pagamentos(self):
        for item in self.tree_pagamentos.get_children():
            self.tree_pagamentos.delete(item)
        for pagamento in listar_pagamentos():
            self.tree_pagamentos.insert('', 'end', values=pagamento)

    def tela_registrar_pagamento(self):
        self.tela_formulario_pagamento("Registrar Pagamento", inserir_pagamento)

    def tela_formulario_pagamento(self, titulo, funcao_salvar, dados=None):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)

        labels = ["ID do Membro", "Valor", "Data"]
        entradas = []
        for i, label in enumerate(labels):
            tk.Label(janela, text=label).grid(row=i, column=0)
            entrada = tk.Entry(janela)
            entrada.grid(row=i, column=1)
            if dados:
                entrada.insert(0, dados[i+1])
            entradas.append(entrada)

        def salvar():
            id_membro = entradas[0].get()
            valor = entradas[1].get()
            data = entradas[2].get()  # Adicione validação para a data
            funcao_salvar(id_membro, valor, data)  # Função para salvar pagamento
            janela.destroy()
            self.carregar_pagamentos()

        tk.Button(janela, text="Salvar", command=salvar).grid(row=len(labels), columnspan=2, pady=10)

    # ======================== Histórico de Atividades ========================

    def tela_historico_atividades(self):
        self.limpar_tela()

        tk.Label(self.root, text="Histórico de Atividades", font=("Arial", 14)).pack(pady=10)

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.tree_historico = ttk.Treeview(frame_top, columns=("ID", "Membro", "Atividade", "Data", "Duração"), show='headings')
        for col in ("ID", "Membro", "Atividade", "Data", "Duração"):
            self.tree_historico.heading(col, text=col)
        self.tree_historico.pack()

        self.carregar_historico()

        frame_bot = tk.Frame(self.root)
        frame_bot.pack(pady=10)

        tk.Button(frame_bot, text="Voltar", command=self.menu_principal).grid(row=0, column=0, padx=5)

    def carregar_historico(self):
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
        for atividade in listar_historico_atividades():
            self.tree_historico.insert('', 'end', values=atividade)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    criar_tabelas()
    criar_admin_default()

    root = tk.Tk()
    app = AcademiaApp(root)
    root.mainloop()
