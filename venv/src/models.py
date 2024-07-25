import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from src.database import setup_database, get_eventos, add_evento, update_evento, delete_evento

class TelaAgenda:
    bege_claro = '#fefae0'
    bege_escuro = '#faedcd'
    marrom = '#d4a373'
    verde_claro = '#e9edc9'
    verde_escuro = '#ccd5ae'

    def __init__(self):
        setup_database()
        self.root = Tk()
        self.config()
        self.frame_superior()
        self.frame_forms()
        self.root.bind("<Button-1>", self.on_click)
        self.frame_calendario()
        self.frame_tabela()
        self.root.mainloop()

    def config(self):
        self.root.title('Agenda Automatizada')
        width = 800
        height = 600
        y = 170

        screen_width = self.root.winfo_screenwidth()
        x = (screen_width // 2) - (width // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.configure(bg=self.bege_claro)

    def frame_superior(self):
        self.frame_cima = Frame(self.root, bg=self.marrom)
        self.frame_cima.place(relwidth=1, relheight=0.1, rely=0)

        self.label_titulo = Label(self.frame_cima, text="Agenda", bg=self.marrom, fg=self.bege_claro, font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

    def frame_forms(self):
        self.frame_forms = Frame(self.root, bg=self.bege_escuro)
        self.frame_forms.place(relwidth=1, relheight=0.3, rely=0.1)

        # Labels for inputs
        labels = [
            ("Tipo do Evento", 0.05, 0.12),
            ("Nome", 0.05, 0.43),
            ("Data (dd/mm/aaaa)", 0.05, 0.75),
            ("Local", 0.35, 0.12),
            ("Telefone (xx) xxxxxxxxx", 0.35, 0.43),
            ("Pacote ou Valor", 0.35, 0.75)
        ]

        self.entries = []
        for text, x, y in labels:
            label = Label(self.frame_forms, text=text, bg=self.bege_escuro, fg='black', font=("Arial", 12))
            label.place(relx=x, rely=y - 0.05, anchor=W)
            
            entry = Entry(self.frame_forms, font=("Arial", 14))
            entry.place(relx=x, rely=y, width=200, height=30)
            self.entries.append(entry)
            
            # Bind events for formatting
            if text.startswith("Data"):
                entry.bind("<KeyRelease>", self.format_date)
            elif text.startswith("Telefone"):
                entry.bind("<KeyRelease>", self.format_phone)

        self.botaoAdicionar = Button(self.frame_forms, text='Adicionar', font=("Arial", 14), command=self.adicionar_evento)
        self.botaoAdicionar.place(relx=0.73, rely=0.12, width=100, height=30)

        self.botaoAtualizar = Button(self.frame_forms, text='Atualizar', font=("Arial", 14), command=self.atualizar_evento)
        self.botaoAtualizar.place(relx=0.73, rely=0.43, width=100, height=30)

        self.botaoExcluir = Button(self.frame_forms, text='Excluir', font=("Arial", 14), command=self.excluir_evento)
        self.botaoExcluir.place(relx=0.73, rely=0.75, width=100, height=30)

        self.botaoLimpar = Button(self.frame_forms, text='Limpar', font=("Arial", 14), command=self.limpar_inputs)
        self.botaoLimpar.place(relx=0.61, rely=0.75, width=80, height=30)

    def format_date(self, event):
        date_entry = self.entries[2]
        date_text = date_entry.get()
        date_text = re.sub(r'\D', '', date_text)
        if len(date_text) > 2 and date_text[2] != '/':
            date_text = date_text[:2] + '/' + date_text[2:]
        if len(date_text) > 5 and date_text[5] != '/':
            date_text = date_text[:5] + '/' + date_text[5:9]
        date_entry.delete(0, END)
        date_entry.insert(0, date_text)

    def format_phone(self, event):
        phone_entry = self.entries[4]
        phone_text = phone_entry.get()
        phone_text = re.sub(r'\D', '', phone_text)  # Remove non-digit characters
        
        if len(phone_text) > 2:
            ddd = phone_text[:2]
            phone_text = f'({ddd}) {phone_text[2:11]}'
        
        phone_entry.delete(0, END)
        phone_entry.insert(0, phone_text)

    def on_click(self, event):
        widget = event.widget
        if widget == self.tree:
            selected_item = self.tree.selection()
            if selected_item:
                item = self.tree.item(selected_item)
                self.load_to_inputs(item["values"])

    def frame_calendario(self):
        self.frame_calendario = Frame(self.root)
        self.frame_calendario.place(relwidth=0.45, relheight=0.53, relx=0.02, rely=0.43)

        self.calendario = Calendar(self.frame_calendario, selectmode='day', year=2024, month=7, day=24)
        self.calendario.pack(expand=True, fill='both')

    def frame_tabela(self):
        self.frame_tabela = Frame(self.root)
        self.frame_tabela.place(relwidth=0.45, relheight=0.53, relx=0.51, rely=0.43)

        # Adding horizontal scrollbar
        scrollbar_x = Scrollbar(self.frame_tabela, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(self.frame_tabela, columns=("id", "tipo", "nome", "data", "local", "telefone", "pacote"), show='headings', xscrollcommand=scrollbar_x.set)
        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("data", text="Data")
        self.tree.heading("local", text="Local")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("pacote", text="Pacote")
        self.tree.pack(expand=True, fill='both')

        # Configuring scrollbar
        scrollbar_x.config(command=self.tree.xview)

        # Adjusting column widths to fit all data
        self.tree.column("id", width=50)
        self.tree.column("tipo", width=100)
        self.tree.column("nome", width=150)
        self.tree.column("data", width=100)
        self.tree.column("local", width=150)
        self.tree.column("telefone", width=120)
        self.tree.column("pacote", width=100)

        self.load_eventos()

    def load_eventos(self):
        eventos = get_eventos()
        for evento in self.tree.get_children():
            self.tree.delete(evento)
        for evento in eventos:
            self.tree.insert("", "end", values=evento)

    def load_to_inputs(self, values):
        for i, value in enumerate(values[1:]):  # Skip the ID value
            self.entries[i].delete(0, END)
            self.entries[i].insert(0, value)

    def adicionar_evento(self):
        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        data = self.entries[2].get()
        local = self.entries[3].get()
        telefone = self.entries[4].get()
        pacote = self.entries[5].get()

        if not self.validate_inputs(tipo, nome, data, local, telefone, pacote):
            return

        add_evento(tipo, nome, data, local, telefone, pacote)
        self.load_eventos()
        self.limpar_inputs()

    def atualizar_evento(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum evento selecionado!")
            return

        tipo = self.entries[0].get()
        nome = self.entries[1].get()
        data = self.entries[2].get()
        local = self.entries[3].get()
        telefone = self.entries[4].get()
        pacote = self.entries[5].get()

        if not self.validate_inputs(tipo, nome, data, local, telefone, pacote):
            return

        item = self.tree.item(selected_item)
        evento_id = item["values"][0]  # Get the ID from the selected item

        update_evento(evento_id, tipo, nome, data, local, telefone, pacote)
        self.load_eventos()
        self.limpar_inputs()

    def excluir_evento(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum evento selecionado!")
            return
        item = self.tree.item(selected_item)
        evento_id = item["values"][0]  # Get the ID from the selected item

        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este evento?")
        if confirm:
            delete_evento(evento_id)
            self.load_eventos()
            self.limpar_inputs()

    def limpar_inputs(self):
        for entry in self.entries:
            entry.delete(0, END)

    def validate_inputs(self, tipo, nome, data, local, telefone, pacote):
        # Validate if all inputs are filled
        if not (tipo and nome and data and local and telefone and pacote):
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return False

        # Validate date format
        if not re.match(r'\d{2}/\d{2}/\d{4}', data):
            messagebox.showwarning("Aviso", "A data deve estar no formato dd/mm/aaaa!")
            return False

        # Validate phone format
        if not re.match(r'\(\d{2}\) \d{8,9}', telefone):
            messagebox.showwarning("Aviso", "O telefone deve estar no formato (xx) xxxxxxxxx!")
            return False

        return True