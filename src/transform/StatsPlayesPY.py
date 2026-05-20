import pandas as pd
from conexao import query, conectar

GAMES_IDS = [22912, 18235, 18244, 3750201, 3750240]


def inserir(sql, params, many=False):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, params) if many else cursor.execute(sql, params)
        conn.commit()
        print(f"{cursor.rowcount} registro(s) inserido(s).")
    finally:
        cursor.close()
        conn.close()


sql_stats = """
    SELECT
        l.player_id,
        l.jersey_number,
        l.team_name AS team_player,

        COUNT(CASE WHEN e.action = 'Pass' THEN 1 END)
            AS tentativas_passe,

        ROUND(
            COUNT(CASE WHEN e.action = 'Pass' AND e.pass_outcome IS NULL THEN 1 END)
            / NULLIF(COUNT(CASE WHEN e.action = 'Pass' THEN 1 END), 0) * 100
        , 1)
            AS perc_acerto_passe,

        COUNT(CASE WHEN e.action = 'Shot' THEN 1 END)
            AS tentativas_chute,

        COUNT(CASE WHEN e.action = 'Shot' AND e.shot_outcome != 'Off T' THEN 1 END)
            AS chutes_no_gol,

        ROUND(SUM(e.shot_xg), 3)
            AS xg_total,

        COUNT(CASE WHEN e.action = 'Ball Recovery' THEN 1 END)
            AS bolas_recuperadas,

        COUNT(CASE WHEN e.action = 'Shot' AND e.shot_outcome = 'Goal' THEN 1 END)
            AS gols,

        COUNT(DISTINCT goal_shot.id)
            AS assistencias,

        COUNT(CASE WHEN e.action = 'Pass' AND e.pass_end_x > e.location_x THEN 1 END)
            AS passes_frente,

        ROUND(AVG(CASE WHEN e.action = 'Pass' THEN e.pass_length END), 2)
            AS distancia_media_passe,

        ROUND(
            COUNT(CASE WHEN e.action = 'Pass' AND e.pass_end_x > e.location_x AND e.pass_outcome IS NULL THEN 1 END)
            / NULLIF(COUNT(CASE WHEN e.action = 'Pass' AND e.pass_end_x > e.location_x THEN 1 END), 0) * 100
        , 1)
            AS aproveit_passe_frente

    FROM events e
    JOIN games g ON e.game = g.game_id
    JOIN lineups l ON g.game_id = l.game AND e.player_id = l.player_id
    LEFT JOIN events goal_shot
        ON goal_shot.key_pass_id = e.id
        AND goal_shot.game = e.game
        AND goal_shot.shot_outcome = 'Goal'
    WHERE g.game_id = %s
    GROUP BY l.player_id, l.jersey_number, l.team_name
    ORDER BY l.team_name, l.jersey_number
"""

sql_insert = """
    INSERT INTO stats_player (
        game_id, player_id, jersey_number, team_name,
        tentativas_passe, perc_acerto_passe,
        tentativas_chute, chutes_no_gol,
        xg_total, bolas_recuperadas,
        gols, assistencias,
        passes_frente, distancia_media_passe, aproveit_passe_frente
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for jogo in GAMES_IDS:
    stats = pd.DataFrame(query(sql_stats).param(jogo).execute())

    rows = [
        (
            jogo,
            row["player_id"],
            row["jersey_number"],
            row["team_player"],
            row["tentativas_passe"],
            row["perc_acerto_passe"],
            row["tentativas_chute"],
            row["chutes_no_gol"],
            row["xg_total"],
            row["bolas_recuperadas"],
            row["gols"],
            row["assistencias"],
            row["passes_frente"],
            row["distancia_media_passe"],
            row["aproveit_passe_frente"],
        )
        for _, row in stats.iterrows()
    ]

    inserir(sql_insert, rows, many=True)
    print(f"Jogo {jogo} processado.")
