import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela original de desinfecções
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS baias_desinfeccao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_baia INTEGER NOT NULL,
                data_desinfeccao DATE NOT NULL,
                metodo TEXT NOT NULL,
                observacao TEXT,
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
                atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # NOVA TABELA: Agendamentos de desinfecção
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos_desinfeccao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_baia INTEGER NOT NULL,
                data_agendamento DATE NOT NULL,
                metodo TEXT NOT NULL,
                observacao TEXT,
                status TEXT DEFAULT 'pendente',
                criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
                atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    # Métodos para desinfecções
    def get_all_desinfeccoes(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM baias_desinfeccao ORDER BY data_desinfeccao DESC')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append(dict(row))
        
        conn.close()
        return result
    
    def insert_desinfeccao(self, numero_baia, data_desinfeccao, metodo, observacao):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO baias_desinfeccao (numero_baia, data_desinfeccao, metodo, observacao)
            VALUES (?, ?, ?, ?)
        ''', (numero_baia, data_desinfeccao, metodo, observacao))
        
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        
        return last_id
    
    def update_desinfeccao(self, id, numero_baia, data_desinfeccao, metodo, observacao):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE baias_desinfeccao 
            SET numero_baia = ?, data_desinfeccao = ?, metodo = ?, observacao = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (numero_baia, data_desinfeccao, metodo, observacao, id))
        
        conn.commit()
        conn.close()
    
    def delete_desinfeccao(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM baias_desinfeccao WHERE id = ?', (id,))
        
        conn.commit()
        conn.close()
    
    # NOVOS MÉTODOS: Agendamentos
    def get_all_agendamentos(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM agendamentos_desinfeccao ORDER BY data_agendamento ASC')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append(dict(row))
        
        conn.close()
        return result
    
    def insert_agendamento(self, numero_baia, data_agendamento, metodo, observacao):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO agendamentos_desinfeccao (numero_baia, data_agendamento, metodo, observacao)
            VALUES (?, ?, ?, ?)
        ''', (numero_baia, data_agendamento, metodo, observacao))
        
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        
        return last_id
    
    def update_agendamento_status(self, id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE agendamentos_desinfeccao 
            SET status = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, id))
        
        conn.commit()
        conn.close()
    
    def delete_agendamento(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM agendamentos_desinfeccao WHERE id = ?', (id,))
        
        conn.commit()
        conn.close()