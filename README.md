<h1 align="center">🧠 LLM Émotions B2B — Prototype</h1>

<p align="center">
  <i>Prototype d'étude des <b>variations linguistiques contrôlées</b> d'un Large Language Model
  sur des scénarios d'échec en relation client B2B.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Prompt%20Engineering-Advanced-success?style=flat" />
  <img src="https://img.shields.io/badge/Mode-Mock%20%2B%20Real-blueviolet?style=flat" />
  <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=flat" />
</p>

<p align="center">
  <a href="#-quick-start">🚀 Quick Start</a> ·
  <a href="#-méthodologie">📐 Méthodologie</a> ·
  <a href="https://portfoliomarte.vercel.app">🌐 Portfolio</a>
</p>

---

## 🎯 Aperçu

Ce projet est un **prototype de recherche en prompt engineering** qui étudie comment
des paramètres linguistiques explicites (registre émotionnel, niveau de familiarité)
modifient les réponses d'un LLM sur des scénarios concrets d'**échec en relation client B2B**
(retard de livraison, panne SaaS, erreur de facturation, non-respect SLA, ticket sans réponse).

> ⚠️ **L'IA n'éprouve pas d'émotions.** On étudie uniquement des **variations linguistiques**
> contrôlées par paramètres explicites.

## ✨ Fonctionnalités

- 🎯 **5 scénarios B2B** réalistes (logistique, SaaS, facturation, support, SLA)
- 🎭 **4 registres émotionnels** (neutre, empathique, rassurant, très professionnel)
- 🤝 **3 niveaux de familiarité** (très formel, semi-formel, familier)
- 🤖 **Mode dual** : OpenAI réel **OU** mode mock paramétrique (gratuit, sans API)
- 📏 **Métriques** automatiques (mots, marqueurs reconnaissance/action/formalité, vouvoiement)
- 🔬 **Comparaison** côte à côte de plusieurs combinaisons
- 📊 **Visualisations** Plotly interactives
- 💾 **Export CSV** de l'historique
- 🛡️ **Contraintes éthiques** explicites dans le méta-prompt

## 📐 Méthodologie

L'architecture suit **4 blocs logiques** :

| Bloc | Contenu |
|------|---------|
| **1. Scénarios B2B** | 5 cas d'échec formulés en **texte neutre et factuel** (pas de mots émotionnels dans l'input) |
| **2. Paramètres linguistiques** | 4 registres × 3 familiarités = **12 combinaisons** par scénario |
| **3. Méta-prompt** | Template paramétrable avec **contraintes éthiques** (pas de manipulation, plan d'action obligatoire) |
| **4. Génération & métriques** | Appel LLM + métriques exploratoires + sauvegarde CSV/JSONL |

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/MarteOued/llm-emotions-b2b-prototype.git
cd llm-emotions-b2b-prototype
pip install -r requirements.txt
```

### Mode mock (recommandé pour tester sans clé API)

```bash
streamlit run app.py
```

Choisis "🎭 Mode Mock" dans la sidebar et c'est parti !

### Mode OpenAI réel (avec clé API)

```bash
# 1. Copie le template
cp .env.example .env

# 2. Édite .env et ajoute ta vraie clé
# OPENAI_API_KEY=sk-XXXXXX

# 3. Lance l'app
streamlit run app.py
```

Sélectionne "🤖 Mode OpenAI" dans la sidebar.

## 🎨 Captures

```
┌────────────────────────────────────────────────────────────────┐
│  🧠 LLM Émotions B2B                                           │
│  Prototype d'étude des variations linguistiques...             │
└────────────────────────────────────────────────────────────────┘

  ┌─ Scénario : 🖥️ Panne logicielle SaaS ──────────────────┐
  │ Le client signale une indisponibilité du service...     │
  └─────────────────────────────────────────────────────────┘

  Paramètres : 💙 Empathique  ·  👔 Semi-formel  ·  🎭 Mock

  [ 🚀 Générer la réponse ]

  📨 Réponse générée
  ┌─────────────────────────────────────────────────────────┐
  │ Bonjour,                                                 │
  │ Nous comprenons parfaitement la gêne occasionnée...     │
  │ Voici notre plan d'action pour vous accompagner...      │
  └─────────────────────────────────────────────────────────┘

  📏 Métriques
  📝 Mots: 142   💙 Reco: 3   ⚡ Action: 4   🎩 Formalité: 1
```

## 📂 Structure

```
llm-emotions-b2b-prototype/
├── app.py              # Interface Streamlit principale
├── prompts.py          # Scénarios, émotions, familiarités, méta-prompt
├── llm_client.py       # Wrapper LLM (mock + OpenAI)
├── metrics.py          # Calcul des métriques exploratoires
├── requirements.txt    # Dépendances
├── .env.example        # Template de config (ne pas committer .env)
├── .gitignore
└── README.md
```

## 🛡️ Contraintes éthiques (intégrées dans le méta-prompt)

Tout LLM appelé par cette app **doit** :
- ✓ Rester professionnel et respectueux
- ✓ Reconnaître l'échec / l'incident sans le minimiser
- ✓ **Ne jamais manipuler émotionnellement** le client
- ✓ Donner un plan d'action concret (étapes, délais, point de contact)
- ✓ Demander les précisions si information manquante

## 🛠️ Stack technique

| Catégorie | Technologie |
|-----------|-------------|
| **Langage** | Python 3.10+ |
| **UI** | Streamlit |
| **LLM** | OpenAI API (gpt-4o-mini) ou mock paramétrique |
| **Visualisation** | Plotly |
| **Data** | Pandas |
| **Sécurité** | python-dotenv pour la gestion des secrets |

## 📊 Métriques exploratoires

L'app calcule pour chaque réponse :

- 📝 **Nombre de mots**
- 💙 **Marqueurs de reconnaissance** ("nous comprenons", "excuses"...)
- ⚡ **Marqueurs d'action** ("plan d'action", "prise en charge"...)
- 🎩 **Marqueurs de formalité** ("Madame", "veuillez"...)
- ✅ **Vouvoiement / Tutoiement** (détection automatique)

## 🎬 Démo

▶️ **[Voir la démo sur YouTube](https://youtu.be/0IhQ_Ob7zjs)**

> Vidéo de démonstration complète (3 min 39) — présentation de l'interface,
> des 5 scénarios B2B, de la génération de réponses et de l'onglet Comparaison.

## 👩‍💻 Auteur

**Martine Ouedraogo** — Master 1 Informatique, spécialisation Data Science & Machine Learning
Université Lumière Lyon 2 · 2026

[LinkedIn](https://www.linkedin.com/in/marte-oued) · [Portfolio](https://portfoliomarte.vercel.app) · [GitHub](https://github.com/MarteOued)

## 📜 Licence

MIT — Projet de recherche réalisé dans le cadre du Master 1 Informatique.
