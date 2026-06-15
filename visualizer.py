import matplotlib.pyplot as plt
import csv
from pathlib import Path
import numpy as np

def plot_elo_graphs_interactive():
    # Hitta alla lag-filer
    lag_filer = list(Path(".").glob("*.csv"))
    lag_filer = [f for f in lag_filer if f.stem not in ["superettan_resultat", "elo"]]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    lines = []  # Spara alla linjer
    labels = []  # Spara alla lagnamn
    
    for fil in lag_filer:
        lag_namn = fil.stem
        
        with open(fil, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            elo_values = []
            for row in reader:
                elo_values.append(float(row["Elo"]))
        
        if elo_values:
            line, = ax.plot(elo_values, label=lag_namn, linewidth=2, marker='o', markersize=3)
            lines.append(line)
            labels.append(lag_namn)
    
    # Skapa annotation för hover
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w", alpha=0.8),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    
    def update_annot(line, label, ind):
        """Uppdatera annotation med laginfo"""
        x_data, y_data = line.get_data()
        x = x_data[ind["ind"][0]]
        y = y_data[ind["ind"][0]]
        annot.xy = (x, y)
        text = f"{label}\nOmgång: {int(x+1)}\nElo: {y:.0f}"
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor('lightyellow')
    
    def hover(event):
        """Hantera hover-event"""
        vis = annot.get_visible()
        if event.inaxes == ax:
            for line, label in zip(lines, labels):
                cont, ind = line.contains(event)
                if cont:
                    update_annot(line, label, ind)
                    annot.set_visible(True)
                    # Highlighta linjen
                    line.set_linewidth(4)
                    line.set_alpha(1.0)
                    fig.canvas.draw_idle()
                    return
            
            # Om ingen linje hittas, göm annotation
            annot.set_visible(False)
            # Återställ alla linjer
            for line in lines:
                line.set_linewidth(2)
                line.set_alpha(1.0)
            fig.canvas.draw_idle()
    
    # Koppla hover-funktionen
    fig.canvas.mpl_connect("motion_notify_event", hover)
    
    ax.set_xlabel("Omgång", fontsize=12)
    ax.set_ylabel("Elo", fontsize=12)
    ax.set_title("Elo-utveckling över tid (Hovra för laginfo)", fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
def show_table():
    elo_data = []
    table_data = []
    with open("elo.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            elo_data.append(row)
            table_data.append(row)
    
    elo_data.sort(key=lambda x: float(x["Elo"]), reverse=True)
    table_data.sort(key=lambda x: float(x["points"]), reverse=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = [[row["Team"], row["Elo"], row["points"]] for row in table_data]
    table = ax.table(cellText=table_data, colLabels=["Team", "Elo", "Poäng"], loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    
    plt.title("Elo-ranking av lagen", fontsize=16, fontweight='bold')
    plt.show()
def plot_elo_vs_points():
    # Hämta senaste Elo från lag-filer
    lag_elo = {}
    lag_filer = list(Path(".").glob("*.csv"))
    lag_filer = [f for f in lag_filer if f.stem not in ["superettan_resultat", "elo"]]
    
    for fil in lag_filer:
        with open(fil, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                lag_elo[fil.stem] = float(rows[-1]["Elo"])
    
    # Räkna tabellpoäng från superettan_resultat.csv
    lag_points = {}
    with open("superettan_resultat.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hemmalag = row["hemmalag"]
            bortalag = row["bortalag"]
            hemmamal = int(row["hemma_mal"])
            bortamal = int(row["borta_mal"])
            
            # Initiera poäng om laget inte finns
            if hemmalag not in lag_points:
                lag_points[hemmalag] = 0
            if bortalag not in lag_points:
                lag_points[bortalag] = 0
            
            # Fördela poäng
            if hemmamal > bortamal:
                lag_points[hemmalag] += 3
            elif hemmamal < bortamal:
                lag_points[bortalag] += 3
            else:
                lag_points[hemmalag] += 1
                lag_points[bortalag] += 1
    
    # Matcha lag som finns i båda datasets
    common_teams = set(lag_elo.keys()) & set(lag_points.keys())
    
    x = []  # Tabellpoäng
    y = []  # Elo
    labels = []
    
    for team in common_teams:
        x.append(lag_points[team])
        y.append(lag_elo[team])
        labels.append(team)
    
    # Skapa plot
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Scatter plot
    scatter = ax.scatter(x, y, s=100, c=y, cmap='RdYlGn', edgecolors='black', linewidth=1, alpha=0.8)
    
    # Lägg till lagnamn vid varje punkt
    for i, label in enumerate(labels):
        # Offset för att inte texten ska ligga exakt på punkten
        offset_x = 0.3
        offset_y = 2
        
        # Växla offset för att undvika överlapp
        if i % 2 == 0:
            offset_y = 2
        else:
            offset_y = -8
        
        ax.annotate(label, (x[i], y[i]), 
                   xytext=(offset_x, offset_y), 
                   textcoords='offset points',
                   fontsize=8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', alpha=0.5))
    
    # Trendlinje
    if len(x) > 1:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(min(x), max(x), 100)
        ax.plot(x_trend, p(x_trend), "--", color='gray', alpha=0.5, label='Trendlinje')
    
    ax.set_xlabel("Tabellpoäng", fontsize=12, fontweight='bold')
    ax.set_ylabel("Elo", fontsize=12, fontweight='bold')
    ax.set_title("Elo vs Tabellpoäng - Superettan", fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Färgskala
    cbar = plt.colorbar(scatter)
    cbar.set_label('Elo', fontweight='bold')
    
    plt.tight_layout()
    plt.show()

show_table()