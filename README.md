# MaintiDoc

Assistant documentaire multimodal et agentique pour la maintenance.
Projet du module IA générative multimodale, EMSI 2026. Livrable 1 : cadrage, corpus et architecture.

## Équipe

Équipe `ELADRAOUI`, travail individuel : Abderrahmane EL ADRAOUI.

## Objectif

Aider un technicien de maintenance à partir d'une question et d'une photo. MaintiDoc répond en citant la page et la figure du document source, consulte l'historique de l'équipement via un outil MCP et prépare un ticket, qui n'est créé qu'après une approbation humaine. Il ne pilote aucune machine et ne garantit aucun diagnostic.

## Contenu du ZIP du livrable 1

```text
L1_MaintiDoc_ELADRAOUI/
├── L1_MaintiDoc_ELADRAOUI_Rapport.pdf      rapport complet
├── L1_MaintiDoc_ELADRAOUI_LienGitHub.txt   URL du dépôt
├── README.md                               ce fichier
└── L1_MaintiDoc_ELADRAOUI_Corpus/          40 documents, inventaire.csv, prompts_corpus.md
```

## Structure du dépôt

```text
maintidoc/
├── README.md
├── .gitignore                exclut les secrets et les fichiers .env
├── docs/
│   ├── reference_coherence.md  table de valeurs de référence du corpus
│   └── diagrammes/             source Python et images des schémas du rapport
├── scripts/
│   └── controle_corpus.py      contrôle de cohérence du corpus
└── corpus/
    ├── inventaire.csv          registre des 40 documents
    ├── prompts_corpus.md       prompts, journal et analyse critique
    ├── documents/famille_1/    pompes centrifuges
    ├── documents/famille_2/    compresseurs à vis
    └── images/                 photos synthétiques
```

## Corpus

Tous les documents sont synthétiques et générés avec Claude : équipements, fabricants et valeurs sont fictifs. Ils ne contiennent aucune donnée personnelle réelle. Pour relancer le contrôle :

```bash
pip install pymupdf
python scripts/controle_corpus.py
```
