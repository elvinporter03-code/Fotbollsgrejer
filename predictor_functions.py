import csv  

def predict_match(team_a, team_b):
    home_w = 0.58
    away_w = 0.42
    drawrate = 0.28
    base_draw = (1-abs(home_w - away_w))/ drawrate

    with open("elo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        team_a_elo = None
        team_b_elo = None
        for row in reader:
            if row["Team"] == team_a:
                team_a_elo = float(row["Elo"])
            elif row["Team"] == team_b:
                team_b_elo = float(row["Elo"])
    expected_a = 1 / (1 + 10 ** ((team_b_elo - team_a_elo - 42) / 400))
    expected_b = 1 - expected_a
    d = (1-abs(expected_a - expected_b))/base_draw
    expected_a -= d/2
    expected_b -= d/2
    print(f"Förväntad sannolikhet för {team_a} att vinna: {expected_a:.2%} eller {1/expected_a} odds")
    print(f"Förväntad sannolikhet för {team_b} att vinna: {expected_b:.2%} eller {1/expected_b} odds")
    print(f"Förväntad sannolikhet för oavgjort: {d:.2%} eller {1/d} odds")

predict_match("GIF Sundsvall", "Östers IF")
predict_match("IFK Norrköping", "Varbergs BoIS")