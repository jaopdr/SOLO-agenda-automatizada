import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from src.database import setup_database, get_eventos, get_eventos_by_date, get_eventos_por_nome,add_evento, update_evento, delete_evento

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
        largura, altura, y = 900, 700, 130
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
            ("Cerimonialista", 0.05, 0.75),
            ("Data", 0.22, 0.12),
            ("Dia do Noivo", 0.22, 0.43),
            ("Dia da Noiva", 0.22, 0.75),
            ("Cerimônia", 0.39, 0.12),
            ("Recepção", 0.39, 0.43),
            ("Telefone", 0.39, 0.75),
            ("Pacote", 0.56, 0.12),
            ("Valor", 0.56, 0.43)
        ]

        self.entries = []
        for texto, x, y in labels:
            label = Label(self.frame_formularios, text=texto, bg=self.bege_escuro, fg='black', font=("Arial", 12))
            label.place(relx=x, rely=y - 0.05, anchor=W)
            
            entrada = Entry(self.frame_formularios, font=("Arial", 14))
            entrada.place(relx=x, rely=y, relwidth=0.15, height=30)
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
        self.botao_adicionar.place(relx=0.8, rely=0.12, width=100, height=30)

        self.botao_atualizar = Button(self.frame_formularios, text='Atualizar', font=("Arial", 14), command=self.atualizar_evento)
        self.botao_atualizar.place(relx=0.8, rely=0.43, width=100, height=30)

        self.botao_excluir = Button(self.frame_formularios, text='Excluir', font=("Arial", 14), command=self.excluir_evento)
        self.botao_excluir.place(relx=0.8, rely=0.75, width=100, height=30)

        self.botao_limpar = Button(self.frame_formularios, text='Limpar', font=("Arial", 14), command=self.limpar_inputs)
        self.botao_limpar.place(relx=0.56, rely=0.75, relwidth=0.15, height=30)

    # Cria o frame do calendário e o botão para mostrar todos os eventos
    def frame_calendario(self):
        self.frame_calendario = Frame(self.root, bg=self.bege_claro)
        self.frame_calendario.place(relwidth=0.45, relheight=0.53, relx=0.02, rely=0.43)

        # Cria o widget Calendar
        self.calendario = Calendar(self.frame_calendario, selectmode='day', year=2024)
        self.calendario.place(relwidth=1, relheight=0.8, rely=0, relx=0)
        self.calendario.bind("<<CalendarSelected>>", self.on_date_select)

        # Botão para mostrar todos os eventos
        self.botao_reset_data = Button(self.frame_calendario, text='Mostrar Todos', font=("Arial", 13), command=self.resetar_dados)
        self.botao_reset_data.place(relwidth=0.35, height=30, rely=0.9, relx=0)

        label = Label(self.frame_calendario, text='Procurar por Nome', bg=self.bege_claro, fg='black', font=("Arial", 12))
        label.place(relx=0.4, rely=0.9 - 0.035, anchor=W)

        self.insert_procura = Entry(self.frame_calendario, font=("Arial", 14))
        self.insert_procura.place(relwidth=0.4, height=30, rely=0.9, relx=0.4)

        self.botao_procura = Button(self.frame_calendario, text='Procurar', font=("Arial", 13), command=self.procurar_evento_por_nome)
        self.botao_procura.place(relwidth=0.2, height=30, rely=0.9, relx=0.8)

    # Cria o frame da tabela de eventos com a barra de rolagem
    def frame_tabela(self):
        self.frame_tabela = Frame(self.root)
        self.frame_tabela.place(relwidth=0.45, relheight=0.53, relx=0.51, rely=0.43)

        # Adiciona a barra de rolagem horizontal
        scrollbar_x = Scrollbar(self.frame_tabela, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        # Cria a Treeview para a tabela de eventos
        self.tree = ttk.Treeview(self.frame_tabela, columns=("id", "tipo", "nome", "cerimonialista", "data", "dia do noivo", "dia da noiva", "cerimonia", "recepção", "telefone", "pacote", "valor"), show='headings', xscrollcommand=scrollbar_x.set)
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cerimonialista", text="Cerimonialista")
        self.tree.heading("data", text="Data")
        self.tree.heading("dia do noivo", text="Dia do Noivo")
        self.tree.heading("dia da noiva", text="Dia da Noiva")
        self.tree.heading("cerimonia", text="Cerimônia")
        self.tree.heading("recepção", text="Recepção")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("pacote", text="Pacote")
        self.tree.heading("valor", text="Valor")
        self.tree.pack(expand=True, fill='both')

        # Configura a barra de rolagem
        scrollbar_x.config(command=self.tree.xview)

        # Ajusta a largura das colunas
        self.tree.column("id", width=0)
        self.tree.column("tipo", width=100)
        self.tree.column("nome", width=150)
        self.tree.column("cerimonialista", width=150)
        self.tree.column("data", width=100)
        self.tree.column("dia do noivo", width=100)
        self.tree.column("dia da noiva", width=100)
        self.tree.column("cerimonia", width=150)
        self.tree.column("recepção", width=150)
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

    def procurar_evento_por_nome(self):
        nome = self.insert_procura.get()
        if not nome:
            messagebox.showwarning("Aviso", "Digite um nome para procurar.")
            return

        eventos = get_eventos_por_nome(nome)  # Correção aqui
        self.tree.delete(*self.tree.get_children())  # Limpa as linhas existentes
        for evento in eventos:
            self.tree.insert("", "end", values=evento)

    # Adiciona um novo evento ao banco de dados
    def adicionar_evento(self):
        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        cerimonialista = self.entries[2].get()
        data = self.entries[3].get()
        dia_noivo = self.entries[4].get()
        dia_noiva = self.entries[5].get()
        cerimonia = self.entries[6].get()
        recepcao = self.entries[7].get()
        telefone = self.entries[8].get()
        pacote = self.entries[9].get()
        valor = self.entries[10].get()

        if not self.validar_inputs(tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor):
            return

        add_evento(tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor)
        self.carregar_eventos()
        self.limpar_inputs()

    def atualizar_evento(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um evento para atualizar.")
            return

        id_evento = self.tree.item(item_selecionado, 'values')[0]
        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        cerimonialista = self.entries[2].get()
        data = self.entries[3].get()
        dia_noivo = self.entries[4].get()
        dia_noiva = self.entries[5].get()
        cerimonia = self.entries[6].get()
        recepcao = self.entries[7].get()
        telefone = self.entries[8].get()
        pacote = self.entries[9].get()
        valor = self.entries[10].get()

        if not self.validar_inputs(tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor):
            return

        update_evento(id_evento, tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor)
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
        self.insert_procura.delete(0, END)

    def validar_inputs(self, tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor):
        if not (tipo and nome and cerimonialista and data and dia_noivo and dia_noiva and cerimonia and recepcao and telefone and pacote and valor):
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

        # Valida o formato do valor, permitindo o símbolo 'R$'
        if not re.match(r'R\$ \d+([.,]\d+)?$', valor):
            messagebox.showwarning("Aviso", "O valor deve ser um número válido com o formato R$ xxxxx,xx!")
            return False

        return True

    # Formata a data enquanto o usuário digita
    def formatar_data(self, event):
        entrada_data = self.entries[3]
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
        entrada_telefone = self.entries[8]
        texto_telefone = entrada_telefone.get()
        texto_telefone = re.sub(r'\D', '', texto_telefone)  # Remove caracteres não numéricos
        
        if len(texto_telefone) > 2:
            ddd = texto_telefone[:2]
            texto_telefone = f'({ddd}) {texto_telefone[2:11]}'
        
        entrada_telefone.delete(0, END)
        entrada_telefone.insert(0, texto_telefone)

    def formatar_valor(self, event):
        entrada = event.widget
        texto = entrada.get()
        # Remove caracteres não numéricos, mas mantém o símbolo 'R$'
        texto_formatado = re.sub(r'[^\d]', '', texto)
        if texto_formatado:
            texto_formatado = f'R$ {int(texto_formatado):,}'.replace(',', '.')
        entrada.delete(0, END)
        entrada.insert(0, texto_formatado)

    # Atualiza os campos de entrada com base na seleção na tabela
    def on_click(self, event):
        widget = event.widget
        if widget == self.tree:
            item_selecionado = self.tree.selection()
            if item_selecionado:
                item = self.tree.item(item_selecionado)
                self.carregar_inputs(item["values"])