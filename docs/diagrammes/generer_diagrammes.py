"""Source des diagrammes du livrable 1 (MaintiDoc).

Usage : python generer_diagrammes.py
Produit les fichiers PNG dans le dossier du script.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).parent
BLEU, BLEU_C, GRIS, GRIS_C, ROUGE, VERT, ENCRE = "#1F4E79", "#E4EDF5", "#6B7280", "#F1F3F5", "#C2410C", "#2F6B4F", "#1F2933"
ROUGE_C, VERT_C = "#FDEDE3", "#E3F1E9"


def boite(ax, x, y, w, h, titre, sous="", fond=BLEU_C, bord=BLEU, ts=9.5, ss=7.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12", fc=fond, ec=bord, lw=1.2, zorder=2))
    if sous:
        ax.text(x + w / 2, y + h * 0.68, titre, ha="center", va="center", fontsize=ts, fontweight="bold", color=ENCRE, zorder=3)
        ax.text(x + w / 2, y + h * 0.3, sous, ha="center", va="center", fontsize=ss, color=ENCRE, zorder=3, linespacing=1.15)
    else:
        ax.text(x + w / 2, y + h / 2, titre, ha="center", va="center", fontsize=ts, fontweight="bold", color=ENCRE, zorder=3)


def fleche(ax, a, b, texte="", dx=0.0, dy=0.0, couleur=GRIS, style="-|>", ls="-", ha="center", rad=0.0, fs=7.4):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=11, color=couleur, lw=1.2, ls=ls, zorder=1,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))
    if texte:
        ax.text((a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy, texte, fontsize=fs, color=ENCRE, ha=ha, va="center", zorder=4,
                bbox=dict(fc="white", ec="none", pad=0.8, alpha=0.95), linespacing=1.1)


def pastille(ax, x, y, code):
    ax.text(x, y, code, fontsize=8, fontweight="bold", color="white", ha="center", va="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.28", fc=ROUGE, ec="white", lw=0.8))


def figure(w, h, xmax, ymax):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    fig.subplots_adjust(0.005, 0.005, 0.995, 0.995)
    return fig, ax


def sauver(fig, nom):
    fig.savefig(OUT / nom, dpi=200)
    plt.close(fig)


def architecture():
    fig, ax = figure(7.6, 7.3, 15.2, 14.6)
    # ligne haute
    boite(ax, 0.3, 12.7, 3.0, 1.6, "Utilisateur", "technicien,\nresponsable", fond=GRIS_C, bord=GRIS)
    boite(ax, 4.2, 12.7, 3.5, 1.6, "Interface web", "Streamlit")
    boite(ax, 9.2, 12.7, 5.7, 1.6, "API", "FastAPI : identité et droits")
    fleche(ax, (3.3, 13.5), (4.2, 13.5))
    fleche(ax, (7.7, 13.75), (9.2, 13.75), "question,\nphoto", dy=0.48)
    fleche(ax, (9.2, 13.2), (7.7, 13.2), "réponse", dy=-0.32)
    # orchestration et verification
    boite(ax, 0.3, 9.6, 9.5, 1.7, "Orchestration", "LangGraph : état, transitions, limites de boucle, pause pour validation")
    boite(ax, 11.0, 9.6, 3.9, 1.7, "Vérification", "citations et format\n(Pydantic)")
    fleche(ax, (9.5, 12.7), (9.5, 11.3), "requête + droits", dx=-0.12, ha="right")
    fleche(ax, (13.0, 11.3), (13.0, 12.7), "réponse validée\nou clarification", dx=0.12, ha="left")
    fleche(ax, (9.8, 10.45), (11.0, 10.45), "brouillon,\nsources", dy=0.48, fs=6.8)
    # branches
    boite(ax, 0.3, 6.2, 4.6, 2.3, "Recherche documentaire", "texte (BGE-M3), image (type CLIP)\nfusion RRF, reranker\nindex Qdrant", ts=9.2, ss=7.4)
    boite(ax, 5.3, 6.2, 4.5, 2.3, "Modèle vision-langage", "Qwen2.5-VL-7B prévu\ninférence Transformers\nrepli : modèle plus petit", ts=9.2)
    boite(ax, 10.4, 6.2, 4.5, 2.3, "Client MCP", "appelle les outils, ne décide\njamais seul de créer un ticket")
    fleche(ax, (2.6, 9.6), (2.6, 8.5), "question + groupes\n/ éléments trouvés", dx=0.12, ha="left", style="<|-|>")
    fleche(ax, (7.55, 9.6), (7.55, 8.5), "photo, extraits\n/ texte produit", dx=0.12, ha="left", style="<|-|>")
    fleche(ax, (9.6, 9.6), (11.2, 8.5), "appel d'outil\n/ résultat", dx=1.25, dy=0.05, style="<|-|>")
    # ligne basse
    boite(ax, 0.3, 2.9, 3.6, 2.2, "Ingestion", "PyMuPDF, OCR local\nlancée à part, avant\nles requêtes", fond=GRIS_C, bord=GRIS)
    boite(ax, 5.3, 2.9, 4.5, 2.2, "Stockage", "PostgreSQL : métadonnées, droits\nMinIO : fichiers d'origine", fond=GRIS_C, bord=GRIS, ss=7.4)
    boite(ax, 10.4, 3.2, 4.5, 1.9, "Serveur MCP maintenance", "historique, tickets ouverts,\ncréation avec jeton", ts=9)
    fleche(ax, (1.6, 5.1), (1.6, 6.2), "index", dx=0.12, ha="left", ls="--")
    fleche(ax, (3.9, 4.0), (5.3, 4.0), "métadonnées,\nfichiers", dy=0.52, fs=7.0)
    fleche(ax, (4.3, 6.2), (5.9, 5.1), "pages\nautorisées", dx=0.75, dy=0.15, style="<|-|>")
    fleche(ax, (12.65, 6.2), (12.65, 5.1), "get_*, create_ticket", dx=0.12, ha="left")
    boite(ax, 10.4, 0.3, 4.5, 1.9, "Validation humaine", "ticket exact affiché dans\nl'interface, puis accord ou refus", fond=ROUGE_C, bord=ROUGE, ts=9, ss=7.4)
    fleche(ax, (12.65, 2.2), (12.65, 3.2), "jeton d'approbation", dx=0.12, ha="left", couleur=ROUGE)
    # legende
    legende = [
        ("C1", "droits vérifiés à l'entrée de l'API"),
        ("C2", "filtre par groupe avant la recherche et à l'ouverture des pages"),
        ("C3", "chaque citation existe et soutient l'affirmation"),
        ("C4", "approbation humaine du contenu exact du ticket"),
        ("C5", "droits et jeton revérifiés côté serveur MCP, à chaque appel"),
    ]
    for i, (c, t) in enumerate(legende):
        y = 2.15 - i * 0.46
        pastille(ax, 0.72, y, c)
        ax.text(1.3, y, t, fontsize=7.6, va="center", color=ENCRE)
    # pastilles
    pastille(ax, 14.9, 14.3, "C1")
    pastille(ax, 4.9, 8.5, "C2")
    pastille(ax, 14.9, 11.3, "C3")
    pastille(ax, 14.9, 2.2, "C4")
    pastille(ax, 14.9, 5.1, "C5")
    sauver(fig, "01_architecture.png")


def ingestion():
    fig, ax = figure(7.6, 2.55, 15.2, 5.1)
    boite(ax, 0.2, 3.1, 2.5, 1.7, "Sources", "PDF, images,\ninventaire.csv", fond=GRIS_C, bord=GRIS)
    boite(ax, 3.3, 3.1, 2.5, 1.7, "Extraction", "PyMuPDF,\ntexte et images")
    boite(ax, 6.4, 3.1, 2.5, 1.7, "OCR", "seulement les\n4 PDF scannés")
    boite(ax, 9.5, 3.1, 2.5, 1.7, "Découpage", "passage, tableau,\nfigure, page")
    boite(ax, 12.6, 3.1, 2.4, 1.7, "Embeddings", "BGE-M3,\nencodeur image")
    for x0, x1 in [(2.7, 3.3), (5.8, 6.4), (8.9, 9.5), (12.0, 12.6)]:
        fleche(ax, (x0, 3.95), (x1, 3.95))
    boite(ax, 12.6, 0.3, 2.4, 1.6, "Qdrant", "vecteurs +\nfiltres de droits", fond=GRIS_C, bord=GRIS)
    boite(ax, 6.4, 0.3, 2.5, 1.6, "PostgreSQL", "métadonnées\nde chaque élément", fond=GRIS_C, bord=GRIS)
    boite(ax, 0.2, 0.3, 2.5, 1.6, "MinIO", "fichiers et images\nd'origine", fond=GRIS_C, bord=GRIS)
    fleche(ax, (13.8, 3.1), (13.8, 1.9), "vecteurs", dx=-0.12, ha="right")
    fleche(ax, (10.7, 3.1), (8.1, 1.9), "éléments et droits", dx=0.95, dy=-0.1)
    fleche(ax, (1.45, 3.1), (1.45, 1.9), "copie intacte", dx=0.12, ha="left")
    sauver(fig, "02_flux_ingestion.png")


def requete():
    fig, ax = figure(7.6, 3.75, 15.2, 7.5)
    h = 1.5
    boite(ax, 0.2, 5.7, 2.7, h, "1. Demande", "question\n+ photo", fond=GRIS_C, bord=GRIS)
    boite(ax, 3.45, 5.7, 2.7, h, "2. Accès", "identité,\ngroupes")
    boite(ax, 6.7, 5.7, 2.7, h, "3. Analyse", "VLM : observation,\néquipement ?")
    boite(ax, 9.95, 5.7, 2.2, h, "4. Recherche", "corpus\nautorisé")
    boite(ax, 12.7, 5.7, 2.3, h, "5. Fusion", "RRF puis\nreranker")
    for a, b in [(2.9, 3.45), (6.15, 6.7), (9.4, 9.95), (12.15, 12.7)]:
        fleche(ax, (a, 6.45), (b, 6.45))
    boite(ax, 12.7, 3.1, 2.3, h, "6. Historique", "MCP si utile\n(3 appels max)")
    boite(ax, 9.25, 3.1, 2.9, h, "7. Rédaction", "VLM, extraits traités\ncomme des données")
    boite(ax, 5.8, 3.1, 2.9, h, "8. Vérification", "citations, soutien,\ncontradictions")
    fleche(ax, (13.85, 5.7), (13.85, 4.6))
    fleche(ax, (12.7, 3.85), (12.15, 3.85))
    fleche(ax, (9.25, 3.85), (8.7, 3.85))
    boite(ax, 0.2, 3.1, 3.4, h, "Refus", "accès interdit,\névénement journalisé", fond=ROUGE_C, bord=ROUGE)
    fleche(ax, (4.3, 5.7), (2.6, 4.6), "pas de droit", dx=-0.85, dy=0.1)
    boite(ax, 5.25, 0.4, 3.45, h, "Clarification", "photo floue, sources\nabsentes, contradiction", fond=ROUGE_C, bord=ROUGE)
    boite(ax, 9.95, 0.4, 3.4, h, "Réponse sourcée", "document, page, figure", fond=VERT_C, bord=VERT)
    fleche(ax, (7.0, 3.1), (7.0, 1.9), "preuves\ninsuffisantes", dx=-0.12, ha="right")
    fleche(ax, (8.4, 3.1), (10.6, 1.9), "preuves suffisantes", dx=1.35, dy=0.15)
    pastille(ax, 6.15, 7.2, "C1")
    pastille(ax, 12.15, 7.2, "C2")
    pastille(ax, 8.7, 4.6, "C3")
    pastille(ax, 15.0, 4.6, "C5")
    sauver(fig, "03_flux_requete.png")


def ticket():
    fig, ax = figure(7.6, 2.9, 15.2, 5.8)
    h = 1.6
    boite(ax, 0.2, 3.8, 2.7, h, "1. Préparer", "brouillon du\nticket par le VLM")
    boite(ax, 3.45, 3.8, 2.7, h, "2. Montrer", "contenu exact\nà l'utilisateur")
    boite(ax, 6.7, 3.8, 2.7, h, "3. Décider", "approuver, modifier\nou refuser", fond=ROUGE_C, bord=ROUGE)
    boite(ax, 9.95, 3.8, 2.3, h, "4. Jeton", "lié à l'utilisateur\net au contenu")
    boite(ax, 12.8, 3.8, 2.2, h, "5. Appel MCP", "create_ticket", ts=9.2)
    for a, b in [(2.9, 3.45), (6.15, 6.7), (9.4, 9.95), (12.25, 12.8)]:
        fleche(ax, (a, 4.6), (b, 4.6))
    fleche(ax, (7.3, 3.8), (4.8, 3.8), "modifié : on remontre,\nancien jeton invalide", dy=-1.05, rad=-0.45, couleur=ROUGE)
    boite(ax, 6.7, 0.25, 2.7, 1.4, "Abandon", "aucun appel,\névénement journalisé", fond=GRIS_C, bord=GRIS)
    fleche(ax, (8.6, 3.8), (8.6, 1.65), "refusé", dx=0.12, ha="left", couleur=ROUGE)
    boite(ax, 12.8, 0.25, 2.2, 1.4, "Serveur MCP", "droits, jeton,\nidempotence", fond=GRIS_C, bord=GRIS, ts=9.2)
    fleche(ax, (13.9, 3.8), (13.9, 1.65))
    boite(ax, 9.75, 0.25, 2.5, 1.4, "Ticket créé", "ou ticket déjà créé\nsi même clé", fond=VERT_C, bord=VERT)
    fleche(ax, (12.8, 0.95), (12.25, 0.95))
    pastille(ax, 9.4, 5.4, "C4")
    pastille(ax, 15.0, 1.65, "C5")
    sauver(fig, "04_flux_ticket.png")


if __name__ == "__main__":
    architecture()
    ingestion()
    requete()
    ticket()
