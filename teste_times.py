from conexao import query

# Cria tabela
query("""
    CREATE TABLE IF NOT EXISTS times (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        pais VARCHAR(50)
    )
""").execute()

# Insere
(
    query("INSERT INTO times (nome, pais) VALUES (%s, %s)")
    .params("Flamengo", "Brasil")
    .execute()
)

# Consulta
times = query("SELECT * FROM times").execute()
print(times)
