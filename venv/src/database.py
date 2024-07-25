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
        pacote TEXT NOT NULL
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

def add_evento(tipo, nome, data, local, telefone, pacote):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos (tipo, nome, data, local, telefone, pacote) VALUES (?, ?, ?, ?, ?, ?)", (tipo, nome, data, local, telefone, pacote))
    conn.commit()
    conn.close()

def update_evento(evento_id, tipo, nome, data, local, telefone, pacote):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET tipo=?, nome=?, data=?, local=?, telefone=?, pacote=? WHERE id=?", (tipo, nome, data, local, telefone, pacote, evento_id))
    conn.commit()
    conn.close()

def delete_evento(evento_id):
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id=?", (evento_id,))
    conn.commit()
    conn.close()