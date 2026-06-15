import tkinter as tk
from tkinter import ttk
import csv
import numpy as np
from elo_calc import calculate_elo, update_csvs, update_elo
from visualizer import show_table

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
    d = (1 - abs(expected_a - expected_b)) / base_draw
    expected_a -= d/2
    expected_b -= d/2
    return expected_a, expected_b, d
def predictor_widget():
    # Läs in lag
    teams = []
    with open("elo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams.append(row["Team"])
    teams.sort()
    
    def update_odds(*args):
        team_a = combo_a.get()
        team_b = combo_b.get()
        
        if team_a and team_b and team_a != team_b:
            home_prob, away_prob, draw_prob = predict_match(team_a, team_b)
            
            result_text.set(
                f'HEMMA: {team_a}\n'
                f'Vinstchans: {home_prob:.1%}\n'
                f'Odds: {np.round(1/home_prob, 2)}\n\n'
                f'OAVGJORT: {draw_prob:.1%}\n'
                f'Odds: {np.round(1/draw_prob, 2)}\n\n'
                f'BORTA: {team_b}\n'
                f'Vinstchans: {away_prob:.1%}\n'
                f'Odds: {np.round(1/away_prob, 2)}\n\n'

            )
        else:
            result_text.set('Välj två olika lag')
    
    # Skapa fönster
    root = tk.Tk()
    root.title("Matchodds Predictor - Superettan")
    root.geometry("750x600")
    
    # Rubrik
    tk.Label(root, text="Välj lag för matchsimulering", 
             font=("Arial", 16, "bold")).pack(pady=20)
    
    # Dropdown-menyer
    frame = tk.Frame(root)
    frame.pack(pady=20)
    
    tk.Label(frame, text="Hemmalag:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    combo_a = ttk.Combobox(frame, values=teams, width=20, state="readonly")
    combo_a.grid(row=0, column=1, padx=10)
    combo_a.set(teams[0])
    combo_a.bind('<<ComboboxSelected>>', update_odds)
    
    tk.Label(frame, text="vs", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10)
    
    tk.Label(frame, text="Bortalag:", font=("Arial", 12)).grid(row=0, column=3, padx=10)
    combo_b = ttk.Combobox(frame, values=teams, width=20, state="readonly")
    combo_b.grid(row=0, column=4, padx=10)
    combo_b.set(teams[1])
    combo_b.bind('<<ComboboxSelected>>', update_odds)
    
    # Resultatvisning
    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, 
                           font=("Arial", 12), justify="center",
                           bg="lightyellow", relief="solid", padx=20, pady=20)
    result_label.pack(pady=30, fill="both", expand=True, padx=50)
    
    # Starta
    update_odds()
    root.mainloop()
def predict_season():
    update_elo()
    with open("kommande_matcher.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team_a = row["hemmalag"]
            team_b = row["bortalag"]
            home_prob, away_prob, draw_prob = predict_match(team_a, team_b)
            random_num = np.random.rand()
            if random_num < home_prob:
                result = 1
            elif random_num < home_prob + draw_prob:
                result = 0.5
            else:
                result = 0
            elochanges = calculate_elo(team_a, team_b, result)
            update_csvs(team_a, elochanges[0], result)
            update_csvs(team_b, elochanges[1], 1-result)
def get_average_elo_points(all_results):
    from collections import defaultdict
    
    teams = defaultdict(lambda: {'elo_sum': 0, 'points_sum': 0, 'count': 0})
    
    for team, elo, points in all_results:
        teams[team]['elo_sum'] += float(elo)
        teams[team]['points_sum'] += int(points)
        teams[team]['count'] += 1
    
    averages = {}
    for team, data in teams.items():
        averages[team] = {
            'avg_elo': data['elo_sum'] / data['count'],
            'avg_points': data['points_sum'] / data['count']
        }
    
    return averages
def simulate_season(nr):
    all_results = []
    for i in range(nr):
        print(f"Simulering {i+1}/{nr}")
        predict_season()
        with open("elo.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_results.append((row['Team'], float(row['Elo']), float(row['points'])))
    
    averages = get_average_elo_points(all_results)
    with open("elo.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Team", "Elo", "K", "last_result", "points"])
        for team, data in averages.items():
            writer.writerow([team, data['avg_elo'], 0, 0, data['avg_points']])
    show_table()

simulate_season(100)