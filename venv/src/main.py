from src.database import setup_database
from src.models import TelaAgenda

if __name__ == "__main__":
    setup_database()  # Configura o banco de dados
    TelaAgenda()  # Inicia a interface gráfica6 