import csv

def update_elo():
    create_base_stats()
    with open("superettan_resultat.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
        for row in reversed(data):
            team_a = row["hemmalag"]
            team_b = row["bortalag"]
            result = int(row["hemma_mal"]) - int(row["borta_mal"])
            if result > 0: 
                result = 1
            elif result < 0:
                result = 0
            else: 
                result = 0.5
            elochange_a = calculate_elo(team_a, team_b, result)
            elochange_b = calculate_elo(team_b, team_a, 1-result)
            update_csvs(team_a, elochange_a, result)
            update_csvs(team_b, elochange_b, 1-result)
            print(f"Updated Elo for {team_a} to {elochange_a} and {team_b} to {elochange_b} based on result {result}")
def update_csvs(team, new_elo, result):
    rows = []
    k = None
    with open("elo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Team"] == team:
                row["Elo"] = new_elo
                if float(row["last_result"]) == result:
                    row["K"] = min(float(row["K"]) + 1, 50)
                else:
                    row["K"] = max(float(row["K"]) - 1, 10)
                k = row["K"]
                row["last_result"] = str(result)
            rows.append(row)

    with open("elo.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Team", "Elo", "K", "last_result"])
        writer.writeheader()
        writer.writerows(rows)

    with open(f"{team}.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([team, new_elo, k])
def calculate_elo(team_a, team_b, result):
    with open("elo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        team_a_elo = None
        team_b_elo = None
        k = None
        for row in reader:
            if row["Team"] == team_a:
                team_a_elo = float(row["Elo"])
                k1 = float(row["K"])
            elif row["Team"] == team_b:
                team_b_elo = float(row["Elo"])
                k2 = float(row["K"])
    k = (k1 + k2) / 2
    expected_a = 1 / (1 + 10 ** ((team_b_elo - team_a_elo) / 400))
    score_a = abs(0-result)
    new_team_a_elo = team_a_elo + k * (score_a - expected_a)

    return new_team_a_elo
def create_base_stats():
    base_k = 30
    base_elo = 1500
    teams = {
        "Helsingborgs IF": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Landskrona BoIS": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Örebro SK": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "GIF Sundsvall": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Varbergs BoIS": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Norrby IF": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "IK Brage": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Ljungskile SK": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "IK Oddevold": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "IFK Norrköping": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Nordic United FC": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Östersunds FK": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Östers IF": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "IFK Värnamo": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Sandvikens IF": {"elo": base_elo, "k": base_k, "last_result": 0.5},
        "Falkenbergs FF": {"elo": base_elo, "k": base_k, "last_result": 0.5},
    }
    with open("elo.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Team", "Elo", "K", "last_result"])
        for team, stats in teams.items():
            writer.writerow([team, stats["elo"], stats["k"], stats["last_result"]])
            with open(f"{team}.csv", "w", encoding="utf-8", newline="") as f:
                writer2 = csv.writer(f)
                writer2.writerow(["Team", "Elo", "K"])


update_elo()
