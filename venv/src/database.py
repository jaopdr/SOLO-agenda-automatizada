import sqlite3

def setup_database():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        nome TEXT NOT NULL,
        cerimonialista TEXT NOT NULL,
        data TEXT NOT NULL,
        dia_noivo TEXT NOT NULL,
        dia_noiva TEXT NOT NULL,
        cerimonia TEXT NOT NULL,
        recepcao TEXT NOT NULL,
        telefone TEXT NOT NULL,
        pacote TEXT NOT NULL,
        valor TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def get_eventos():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos ORDER BY data ASC")
    eventos = cursor.fetchall()
    conn.close()
    return eventos


def get_eventos_by_date(date):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos WHERE data=? ORDER BY data ASC", (date,))
    eventos = cursor.fetchall()
    conn.close()
    return eventos

def get_eventos_por_nome(nome):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    query = "SELECT * FROM eventos WHERE nome LIKE ? ORDER BY data ASC"
    cursor.execute(query, ('%' + nome + '%',))
    eventos = cursor.fetchall()
    conn.close()
    return eventos

def add_evento(tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos (tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor))
    conn.commit()
    conn.close()

def update_evento(evento_id, tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET tipo=?, nome=?, cerimonialista=?, data=?, dia_noivo=?, dia_noiva=?, cerimonia=?, recepcao=?, telefone=?, pacote=?, valor=? WHERE id=?", (tipo, nome, cerimonialista, data, dia_noivo, dia_noiva, cerimonia, recepcao, telefone, pacote, valor, evento_id))
    conn.commit()
    conn.close()

def delete_evento(evento_id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id=?", (evento_id,))
    conn.commit()
    conn.close()