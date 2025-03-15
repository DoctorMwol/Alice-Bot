import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Função para conectar ao banco de dados
def start_database():
    connection = mysql.connector.connect(
        host= os.getenv("HOST"),       # Endereço do servidor MySQL (pode ser um IP ou domínio)
        user=os.getenv("USER"),            # Usuário do banco de dados
        password=os.getenv("PASSWORD"), # Senha do usuário
        database=os.getenv("DATABASE"),     # Nome do banco de dados
        port=os.getenv("PORT")        # Porta do servidor MySQL (padrão é 3306)
    )
    cursor = connection.cursor()
    return connection, cursor

# Função para procurar o usuário
def search_user(user_id):
    connection, cursor = start_database()

    query = f"SELECT * FROM jokenpo_scores WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()

    # Fechar a conexão após a operação
    connection.commit()
    cursor.close()
    connection.close()

    return result

# Função para atualizar o score de um usuário
def update_score(user_id, wins, losses, draws, score=1):
    connection, cursor = start_database()

    query = f"""
    UPDATE jokenpo_scores
    SET wins = wins + {wins}, losses = losses + {losses}, draws = draws + {draws}, total_score = total_score + {score}
    WHERE id = {user_id};
    """
    cursor.execute(query)
    connection.commit()
    #print(f"Score do usuário {user_id} atualizado: {wins} vitórias, {losses} derrotas, {draws} empates e {score} pontos.")

    # Fechar a conexão após a operação
    cursor.close()
    connection.close()

# Função para verificar e criar o usuário, se não encontrado
def check_and_create_user(user_id):
    user = search_user(user_id)
    
    if not user:
        connection, cursor = start_database()

        # Inserir o ID do usuário do Discord na tabela
        query = f"""
        INSERT INTO jokenpo_scores (id, games_played, wins, losses, draws, total_score)
        VALUES ({user_id}, 0, 0, 0, 0, 0)
        """
        cursor.execute(query)
        connection.commit()
        #print(f"Usuário {user_id} criado no banco de dados.")

        cursor.close()
        connection.close()

# Função para recuperar estatísticas do usuário
def get_user_stats(user_id):
    connection, cursor = start_database()

    query = f"SELECT wins, losses, draws, (wins + losses + draws) AS total_games FROM jokenpo_scores WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()

    # Fechar a conexão após a operação
    cursor.close()
    connection.close()

    if result:
        wins, losses, draws, total_games = result
        return {
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "total_games": total_games
        }
    else:
        return None # Retorna None se o usuário não for encontrado
