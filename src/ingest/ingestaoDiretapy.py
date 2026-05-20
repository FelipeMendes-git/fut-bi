from conexao import conectar
from pathlib import Path
import json

GAMES_IDS = [22912, 18235, 18244, 3750201, 3750240]

BASE = Path(__file__).parent.parent.parent / "data" / "raw"


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

for GAME_ID in GAMES_IDS:
    match_path = BASE / "matches" / f"{GAME_ID}.json"
    with open(match_path, encoding="utf-8") as f:
        matches = json.load(f)

    m = matches[0]
    home = m["home_team"]
    away = m["away_team"]
    home_manager = (home.get("managers") or [{}])[0].get("name")
    away_manager = (away.get("managers") or [{}])[0].get("name")
    stadium = m.get("stadium", {}).get("name")

    sql = """
        INSERT INTO games (
            game_id,
            team_1_id, team_1_name,
            team_2_id, team_2_name,
            home_score, away_score,
            home_manager, away_manager,
            stadium
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    row = (
        m["match_id"],
        home["home_team_id"],
        home["home_team_name"],
        away["away_team_id"],
        away["away_team_name"],
        m["home_score"],
        m["away_score"],
        home_manager,
        away_manager,
        stadium,
    )

    inserir(sql, row)


    file_path = BASE / "lineups" / f"{GAME_ID}.json"
    with open(file_path, encoding="utf-8") as f:
        lineups = json.load(f)

    sql = """
        INSERT INTO lineups (game, team_id, team_name, player_id, player_name, country, jersey_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    rows = [
        (
            GAME_ID,
            team["team_id"],
            team["team_name"],
            player["player_id"],
            player["player_name"],
            player["country"]["name"],
            player["jersey_number"],
        )
        for team in lineups
        for player in team["lineup"]
    ]

    inserir(sql, rows, many=True)


    eventPath = BASE / "events" / f"{GAME_ID}.json"
    with open(eventPath, encoding="utf-8") as f:
        events = json.load(f)

    sql = """
        INSERT INTO events (
            id, game, idx, period, minute, second, action, player_id, position,
            location_x, location_y,
            pass_length, pass_outcome, pass_end_x, pass_end_y,
            shot_xg, shot_outcome, shot_technique,
            duel_type, duel_outcome,
            key_pass_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    rows = []
    for event in events:
        if not event.get("player"):
            continue

        location  = event.get("location") or [None, None]
        pass_data = event.get("pass", {})
        shot_data = event.get("shot", {})
        duel_data = event.get("duel", {})
        pass_end  = pass_data.get("end_location") or [None, None]

        rows.append((
            event["id"],
            GAME_ID,
            event.get("index"),
            event.get("period"),
            event.get("minute"),
            event.get("second"),
            event.get("type", {}).get("name"),
            event["player"]["id"],
            event.get("position", {}).get("name"),
            location[0],
            location[1],
            pass_data.get("length"),
            pass_data.get("outcome", {}).get("name"),
            pass_end[0],
            pass_end[1],
            shot_data.get("statsbomb_xg"),
            shot_data.get("outcome", {}).get("name"),
            shot_data.get("technique", {}).get("name"),
            duel_data.get("type", {}).get("name"),
            duel_data.get("outcome", {}).get("name"),
            shot_data.get("key_pass_id"),
        ))

    inserir(sql, rows, many=True)