"""Controle de coherence du corpus MaintiDoc.

Usage : python scripts/controle_corpus.py [dossier_corpus]
Dependance : pymupdf.
Limite : ce script detecte des incoherences entre documents, pas une erreur
recopiee partout a l'identique. Il ne remplace pas la relecture humaine.
"""
import collections
import csv
import re
import sys
from pathlib import Path

import fitz

COLONNES = ("document_id,fichier,titre,famille_equipement,equipement_id,type_document,version,nb_pages,langue,format,"
            "elements_visuels,provenance,licence,genere_par_ia,outil_ia,verifie_par,corrections,groupe_acces,usage_test,remarques").split(",")
VALEURS = {
    "famille_equipement": {"pompes", "compresseurs"},
    "type_document": {"manuel", "procedure", "fiche_securite", "schema", "codes_alarme", "photo", "historique"},
    "langue": {"fr", "en"},
    "format": {"pdf_texte", "pdf_scanne", "image"},
    "genere_par_ia": {"oui", "non"},
    "usage_test": {"normal", "contradictoire", "injection", "ambigu"},
}
VOYANTS = {
    "P-ALM-01": "Orange fixe", "P-ALM-02": "Orange clignotant", "P-ALM-03": "Rouge fixe", "P-ALM-04": "Jaune fixe",
    "P-ALM-05": "Jaune clignotant", "P-ALM-06": "Rouge clignotant", "P-ALM-07": "Rouge + jaune",
    "C-ALM-01": "Orange clignotant", "C-ALM-02": "Jaune fixe", "C-ALM-03": "Jaune clignotant", "C-ALM-04": "Rouge clignotant",
    "C-ALM-05": "Rouge fixe", "C-ALM-06": "Rouge + jaune", "C-ALM-07": "Écran seul", "C-ALM-08": "Jaune fixe", "C-ALM-09": "Orange fixe",
}
# Valeurs qui ne doivent pas apparaitre dans les documents d'un autre equipement.
INTERDITS = {
    "pompe_b": r"\b95 °C|\b105 °C|2,5 bar|\b28 A\b|DN 65",
    "pompe_a": r"\b100 °C|\b110 °C|3,5 bar|\b40 A\b|DN 100",
    "comp_a": r"\b115 °C|\b105 °C|8,0 bar|\b95 A\b|25 L",
    "comp_b": r"\b100 °C|6,0 bar|\b65 A\b|18 L",
}


def main(racine):
    erreurs = []
    with open(racine / "inventaire.csv", encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != COLONNES:
            erreurs.append("colonnes de l'inventaire incorrectes")
        lignes = list(lecteur)

    ids = collections.Counter(l["document_id"] for l in lignes)
    erreurs += [f"identifiant en double : {k}" for k, n in ids.items() if n > 1]
    for l in lignes:
        for col, permis in VALEURS.items():
            if l[col] not in permis:
                erreurs.append(f"{l['document_id']} : valeur '{l[col]}' interdite pour {col}")
        if Path(l["fichier"]).stem != l["document_id"]:
            erreurs.append(f"{l['document_id']} : nom de fichier different de l'identifiant")

    inventaire = {l["fichier"] for l in lignes}
    disque = {p.relative_to(racine).as_posix() for d in ("documents", "images") for p in (racine / d).rglob("*") if p.is_file()}
    erreurs += [f"absent de l'inventaire : {x}" for x in sorted(disque - inventaire)]
    erreurs += [f"absent du disque : {x}" for x in sorted(inventaire - disque)]

    paires = 0
    for l in lignes:
        chemin = racine / l["fichier"]
        if chemin.suffix != ".pdf" or not chemin.exists():
            continue
        doc = fitz.open(chemin)
        if str(len(doc)) != l["nb_pages"]:
            erreurs.append(f"{l['document_id']} : {len(doc)} pages, inventaire {l['nb_pages']}")
        texte = re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))
        if l["format"] == "pdf_scanne":
            if len(texte) > 50:
                erreurs.append(f"{l['document_id']} : declare scanne mais contient du texte")
            continue
        for code in re.findall(r"\b[PC]-ALM-\d+\b", texte):
            if code not in VOYANTS:
                erreurs.append(f"{l['document_id']} : code inconnu {code}")
        for m in re.finditer(r"([PC]-ALM-0\d) ((?:Orange|Jaune|Rouge|Écran)[^ ]* ?(?:fixe|clignotant|seul|\+ jaune)?)", texte):
            paires += 1
            if m[1] in VOYANTS and not m[2].startswith(VOYANTS[m[1]]):
                erreurs.append(f"{l['document_id']} : {m[0]} (attendu {VOYANTS[m[1]]})")
        for tag, motif in INTERDITS.items():
            if tag in l["document_id"]:
                for m in re.finditer(motif, texte):
                    erreurs.append(f"{l['document_id']} : valeur d'un autre equipement : {m[0]}")
        if "vidange_a" not in l["document_id"] and re.search(r"\d+\s*N\s*·\s*m", texte):
            erreurs.append(f"{l['document_id']} : couple de serrage hors procedure de vidange")

    print(f"{len(lignes)} documents, {len(disque)} fichiers, {paires} couples code et voyant verifies")
    for e in erreurs:
        print("ERREUR :", e)
    print("Controle termine :", "aucune erreur" if not erreurs else f"{len(erreurs)} erreur(s)")
    return 1 if erreurs else 0


if __name__ == "__main__":
    dossier = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "corpus"
    sys.exit(main(dossier))
