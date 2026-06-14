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

plot_elo_graphs_interactive()