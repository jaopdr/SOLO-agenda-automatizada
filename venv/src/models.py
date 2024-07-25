import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from src.database import setup_database, get_eventos, get_eventos_by_date, add_evento, update_evento, delete_evento

class TelaAgenda:
    # Cores usadas na interface
    bege_claro = '#fefae0'
    bege_escuro = '#faedcd'
    marrom = '#d4a373'

    def __init__(self):
        # Configurações iniciais
        setup_database()
        self.root = Tk()
        self.configurar()
        self.frame_superior()
        self.frame_formularios()
        self.frame_calendario()
        self.frame_tabela()
        self.root.bind("<Button-1>", self.on_click)  # Bind para atualizar os campos de entrada com os dados do item selecionado
        self.root.mainloop()

    # Configura a janela principal
    def configurar(self):
        self.root.title('Agenda Automatizada')
        largura, altura, y = 800, 600, 170
        largura_tela = self.root.winfo_screenwidth()
        x = (largura_tela // 2) - (largura // 2)
        self.root.geometry(f'{largura}x{altura}+{x}+{y}')
        self.root.configure(bg=self.bege_claro)

    # Cria o frame superior contendo o título
    def frame_superior(self):
        self.frame_cima = Frame(self.root, bg=self.marrom)
        self.frame_cima.place(relwidth=1, relheight=0.1, rely=0)

        self.label_titulo = Label(self.frame_cima, text="Agenda", bg=self.marrom, fg=self.bege_claro, font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

    # Cria o frame dos formulários e os botões de ação
    def frame_formularios(self):
        self.frame_formularios = Frame(self.root, bg=self.bege_escuro)
        self.frame_formularios.place(relwidth=1, relheight=0.3, rely=0.1)

        # Labels e campos de entrada
        labels = [
            ("Tipo do Evento", 0.05, 0.12),
            ("Nome", 0.05, 0.43),
            ("Data (dd/mm/aaaa)", 0.05, 0.75),
            ("Local", 0.31, 0.12),
            ("Telefone (xx) xxxxxxxxx", 0.31, 0.43),
            ("Pacote", 0.31, 0.75),
            ("Valor", 0.57, 0.12)
        ]

        self.entries = []
        for texto, x, y in labels:
            label = Label(self.frame_formularios, text=texto, bg=self.bege_escuro, fg='black', font=("Arial", 12))
            label.place(relx=x, rely=y - 0.05, anchor=W)
            
            entrada = Entry(self.frame_formularios, font=("Arial", 14))
            entrada.place(relx=x, rely=y, width=200, height=30)
            self.entries.append(entrada)
            
            # Bind para formatação de data, telefone e valor
            if texto.startswith("Data"):
                entrada.bind("<KeyRelease>", self.formatar_data)
            elif texto.startswith("Telefone"):
                entrada.bind("<KeyRelease>", self.formatar_telefone)
            elif texto.startswith("Valor"):
                entrada.bind("<KeyRelease>", self.formatar_valor)

        # Botões de ação
        self.botao_adicionar = Button(self.frame_formularios, text='Adicionar', font=("Arial", 14), command=self.adicionar_evento)
        self.botao_adicionar.place(relx=0.85, rely=0.12, width=100, height=30)

        self.botao_atualizar = Button(self.frame_formularios, text='Atualizar', font=("Arial", 14), command=self.atualizar_evento)
        self.botao_atualizar.place(relx=0.85, rely=0.43, width=100, height=30)

        self.botao_excluir = Button(self.frame_formularios, text='Excluir', font=("Arial", 14), command=self.excluir_evento)
        self.botao_excluir.place(relx=0.85, rely=0.75, width=100, height=30)

        self.botao_limpar = Button(self.frame_formularios, text='Limpar', font=("Arial", 14), command=self.limpar_inputs)
        self.botao_limpar.place(relx=0.61, rely=0.75, width=80, height=30)

    # Cria o frame do calendário e o botão para mostrar todos os eventos
    def frame_calendario(self):
        self.frame_calendario = Frame(self.root, bg=self.bege_claro)
        self.frame_calendario.place(relwidth=0.45, relheight=0.53, relx=0.02, rely=0.43)

        # Cria o widget Calendar
        self.calendario = Calendar(self.frame_calendario, selectmode='day', year=2024)
        self.calendario.place(relwidth=1, relheight=0.8, rely=0, relx=0)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_select)

        # Botão para mostrar todos os eventos
        self.botao_reset_data = Button(self.frame_calendario, text='Mostrar Todos os Eventos', font=("Arial", 14), command=self.resetar_dados)
        self.botao_reset_data.place(width=300, height=30, rely=0.9, relx=0.5, anchor=CENTER)

    # Cria o frame da tabela de eventos com a barra de rolagem
    def frame_tabela(self):
        self.frame_tabela = Frame(self.root)
        self.frame_tabela.place(relwidth=0.45, relheight=0.53, relx=0.51, rely=0.43)

        # Adiciona a barra de rolagem horizontal
        scrollbar_x = Scrollbar(self.frame_tabela, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        # Cria a Treeview para a tabela de eventos
        self.tree = ttk.Treeview(self.frame_tabela, columns=("id", "tipo", "nome", "data", "local", "telefone", "pacote", "valor"), show='headings', xscrollcommand=scrollbar_x.set)
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("data", text="Data")
        self.tree.heading("local", text="Local")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("pacote", text="Pacote")
        self.tree.heading("valor", text="Valor")
        self.tree.pack(expand=True, fill='both')

        # Configura a barra de rolagem
        scrollbar_x.config(command=self.tree.xview)

        # Ajusta a largura das colunas
        self.tree.column("id", width=50)
        self.tree.column("tipo", width=100)
        self.tree.column("nome", width=150)
        self.tree.column("data", width=100)
        self.tree.column("local", width=150)
        self.tree.column("telefone", width=120)
        self.tree.column("pacote", width=100)
        self.tree.column("valor", width=100)

        self.carregar_eventos()

    # Atualiza a tabela com os eventos do dia selecionado no calendário
    def on_date_select(self, event):
        data_selecionada = self.calendario.get_date()
        eventos = get_eventos_by_date(data_selecionada)
        self.tree.delete(*self.tree.get_children())  # Limpa as linhas existentes
        for evento in eventos:
            self.tree.insert("", "end", values=evento)

    # Limpa a seleção do calendário e recarrega todos os eventos
    def resetar_dados(self):
        self.calendario.selection_clear()
        self.carregar_eventos()

    # Carrega todos os eventos na tabela
    def carregar_eventos(self):
        eventos = get_eventos()
        self.tree.delete(*self.tree.get_children())  # Limpa as linhas existentes
        for evento in eventos:
            self.tree.insert("", "end", values=evento)

    # Carrega os dados do evento selecionado nos campos de entrada
    def carregar_inputs(self, valores):
        for i, valor in enumerate(valores[1:]):  # Ignora o valor do ID
            self.entries[i].delete(0, END)
            self.entries[i].insert(0, valor)

    # Adiciona um novo evento ao banco de dados
    def adicionar_evento(self):
        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        data = self.entries[2].get()
        local = self.entries[3].get()
        telefone = self.entries[4].get()
        pacote = self.entries[5].get()
        valor = self.entries[6].get()

        if not self.validar_inputs(tipo, nome, data, local, telefone, pacote, valor):
            return

        add_evento(tipo, nome, data, local, telefone, pacote, valor)
        self.carregar_eventos()
        self.limpar_inputs()

    # Atualiza um evento existente no banco de dados
    def atualizar_evento(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Nenhum evento selecionado!")
            return

        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        data = self.entries[2].get()
        local = self.entries[3].get()
        telefone = self.entries[4].get()
        pacote = self.entries[5].get()
        valor = self.entries[6].get()

        if not self.validar_inputs(tipo, nome, data, local, telefone, pacote, valor):
            return

        item = self.tree.item(item_selecionado)
        evento_id = item["values"][0]  # Obtém o ID do item selecionado

        update_evento(evento_id, tipo, nome, data, local, telefone, pacote, valor)
        self.carregar_eventos()
        self.limpar_inputs()

    # Exclui um evento do banco de dados
    def excluir_evento(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Nenhum evento selecionado!")
            return
        item = self.tree.item(item_selecionado)
        evento_id = item["values"][0]  # Obtém o ID do item selecionado

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este evento?")
        if confirmacao:
            delete_evento(evento_id)
            self.carregar_eventos()
            self.limpar_inputs()

    # Limpa todos os campos de entrada
    def limpar_inputs(self):
        for entrada in self.entries:
            entrada.delete(0, END)

    def validar_inputs(self, tipo, nome, data, local, telefone, pacote, valor):
        if not (tipo and nome and data and local and telefone and pacote and valor):
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return False

        # Valida o formato da data
        if not re.match(r'\d{2}/\d{2}/\d{4}', data):
            messagebox.showwarning("Aviso", "A data deve estar no formato dd/mm/aaaa!")
            return False

        # Valida o formato do telefone
        if not re.match(r'\(\d{2}\) \d{8,9}', telefone):
            messagebox.showwarning("Aviso", "O telefone deve estar no formato (xx) xxxxxxxxx!")
            return False

        # Valida o formato do valor
        if not re.match(r'^\d+$', valor):  # Verifica se o valor contém apenas números
            messagebox.showwarning("Aviso", "O valor deve ser um número válido!")
            return False

        return True

    # Formata a data enquanto o usuário digita
    def formatar_data(self, event):
        entrada_data = self.entries[2]
        texto_data = entrada_data.get()
        texto_data = re.sub(r'\D', '', texto_data)
        if len(texto_data) > 2 and texto_data[2] != '/':
            texto_data = texto_data[:2] + '/' + texto_data[2:]
        if len(texto_data) > 5 and texto_data[5] != '/':
            texto_data = texto_data[:5] + '/' + texto_data[5:9]
        entrada_data.delete(0, END)
        entrada_data.insert(0, texto_data)

    # Formata o telefone enquanto o usuário digita
    def formatar_telefone(self, event):
        entrada_telefone = self.entries[4]
        texto_telefone = entrada_telefone.get()
        texto_telefone = re.sub(r'\D', '', texto_telefone)  # Remove caracteres não numéricos
        
        if len(texto_telefone) > 2:
            ddd = texto_telefone[:2]
            texto_telefone = f'({ddd}) {texto_telefone[2:11]}'
        
        entrada_telefone.delete(0, END)
        entrada_telefone.insert(0, texto_telefone)

    def formatar_valor(self, event):
        entrada_valor = self.entries[6]
        texto_valor = entrada_valor.get()
        texto_valor = re.sub(r'[^0-9]', '', texto_valor)  # Remove caracteres não numéricos
        entrada_valor.delete(0, END)
        entrada_valor.insert(0, texto_valor)

    # Atualiza os campos de entrada com base na seleção na tabela
    def on_click(self, event):
        widget = event.widget
        if widget == self.tree:
            item_selecionado = self.tree.selection()
            if item_selecionado:
                item = self.tree.item(item_selecionado)
                self.carregar_inputs(item["values"])