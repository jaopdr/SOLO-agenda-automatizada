import sqlite3

def setup_database():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        nome TEXT NOT NULL,
        data TEXT NOT NULL,
        local TEXT NOT NULL,
        telefone TEXT NOT NULL,
        pacote TEXT NOT NULL,
        valor REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def get_eventos():
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos")
    eventos = cursor.fetchall()
    conn.close()
    return eventos

def get_eventos_by_date(date):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos WHERE data=?", (date,))
    eventos = cursor.fetchall()
    conn.close()
    return eventos

def add_evento(tipo, nome, data, local, telefone, pacote, valor):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos (tipo, nome, data, local, telefone, pacote, valor) VALUES (?, ?, ?, ?, ?, ?, ?)", (tipo, nome, data, local, telefone, pacote, float(valor)))
    conn.commit()
    conn.close()

def update_evento(evento_id, tipo, nome, data, local, telefone, pacote, valor):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET tipo=?, nome=?, data=?, local=?, telefone=?, pacote=?, valor=? WHERE id=?", (tipo, nome, data, local, telefone, pacote, float(valor), evento_id))
    conn.commit()
    conn.close()

def delete_evento(evento_id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id=?", (evento_id,))
    conn.commit()
    conn.close()