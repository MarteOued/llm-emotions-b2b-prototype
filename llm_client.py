"""
Client LLM avec deux modes :
- mock : génération paramétrique sans appel API (gratuit, déterministe)
- openai : appel réel à l'API OpenAI (nécessite OPENAI_API_KEY)

Le mode mock construit une réponse plausible en fonction des paramètres
(scénario × émotion × familiarité) à partir de templates structurés.
"""

import os
from typing import Optional
from prompts import SCENARIOS, EMOTIONS, FAMILIARITES, build_prompt


# =====================================================================
# TEMPLATES MOCK — varient selon les paramètres
# =====================================================================
GREETINGS = {
    "tres_formel": [
        "Madame, Monsieur,",
        "Madame, Monsieur,",
    ],
    "semi_formel": [
        "Bonjour,",
        "Bonjour,",
    ],
    "familier": [
        "Salut,",
        "Hello,",
    ],
}

OPENINGS = {
    "neutre": {
        "S1_retard_livraison": "Nous accusons réception de votre signalement concernant la livraison du 10 du mois.",
        "S2_panne_logicielle": "Nous prenons note de l'indisponibilité du service depuis 09:15.",
        "S3_erreur_facturation": "Nous accusons réception de votre demande relative à la facture émise.",
        "S4_non_respect_SLA": "Nous prenons note du non-respect des délais SLA observés.",
        "S5_ticket_sans_reponse": "Nous prenons note de l'absence de réponse sur les tickets ouverts.",
    },
    "empathique": {
        "S1_retard_livraison": "Nous comprenons l'impact que ce retard peut avoir sur la mise en production de votre site et la mobilisation de vos équipes. Nous vous présentons nos excuses pour cette situation.",
        "S2_panne_logicielle": "Nous comprenons parfaitement la gêne occasionnée par cette indisponibilité et nous vous présentons nos excuses sincères pour l'impact sur vos équipes.",
        "S3_erreur_facturation": "Nous comprenons votre questionnement et nous vous présentons nos excuses pour la confusion générée par cette facture.",
        "S4_non_respect_SLA": "Nous comprenons l'irritation que peut provoquer un dépassement de SLA et nous reconnaissons l'impact opérationnel.",
        "S5_ticket_sans_reponse": "Nous comprenons votre frustration et nous vous présentons nos excuses pour ce délai inacceptable.",
    },
    "rassurant": {
        "S1_retard_livraison": "Nous prenons en charge la situation et mettons en place un plan de rattrapage immédiat.",
        "S2_panne_logicielle": "Notre équipe technique est immédiatement mobilisée et nous mettons en place une solution de mitigation.",
        "S3_erreur_facturation": "Nous prenons en charge la vérification de votre facture et garantissons une correction si nécessaire.",
        "S4_non_respect_SLA": "Nous prenons en charge l'analyse des écarts et établissons un plan de retour au niveau de service.",
        "S5_ticket_sans_reponse": "Nous mobilisons immédiatement un point de contact unique pour traiter vos tickets bloquants.",
    },
    "tres_professionnel": {
        "S1_retard_livraison": "Nous accusons réception de votre signalement et nous engageons à respecter notre obligation contractuelle de livraison.",
        "S2_panne_logicielle": "Nous accusons réception de votre signalement d'incident et appliquons notre procédure de gestion d'incident conformément à notre SLA.",
        "S3_erreur_facturation": "Nous accusons réception de votre demande de vérification et appliquons notre procédure de revue contractuelle.",
        "S4_non_respect_SLA": "Nous accusons réception de votre signalement et reconnaissons le non-respect de nos engagements contractuels.",
        "S5_ticket_sans_reponse": "Nous accusons réception de votre escalade et appliquons notre procédure de remédiation conformément aux engagements contractuels.",
    },
}

ACTION_PLANS = {
    "neutre": "Voici les prochaines étapes : (1) diagnostic en cours, (2) communication d'une estimation sous 60 minutes, (3) point d'avancement régulier.",
    "empathique": "Voici notre plan d'action pour vous accompagner : (1) prise en charge immédiate par un référent dédié, (2) communication transparente toutes les 30 minutes, (3) compte-rendu détaillé une fois la situation résolue.",
    "rassurant": "Voici concrètement ce que nous allons faire : (1) mobilisation de notre équipe d'intervention, (2) mise en place d'une solution de contournement sous 1 heure, (3) résolution définitive sous 24 heures.",
    "tres_professionnel": "Engagements de remédiation : (1) ouverture d'un compte-rendu d'incident formel, (2) plan d'action transmis sous 24 heures avec jalons mesurables, (3) reporting hebdomadaire jusqu'à clôture, (4) revue de gouvernance contractuelle.",
}

CONTACT_INFOS = {
    "tres_formel": "Pour toute information complémentaire, je vous prie de bien vouloir contacter votre responsable de compte ou de répondre directement à cet email.",
    "semi_formel": "N'hésitez pas à me contacter directement pour toute question — je reste à votre disposition.",
    "familier": "Si tu as la moindre question, contacte-moi directement, je suis là pour t'aider.",
}

CLOSINGS = {
    "tres_formel": "Nous vous prions d'agréer, Madame, Monsieur, l'expression de nos salutations distinguées.",
    "semi_formel": "Cordialement,",
    "familier": "À très vite,",
}

SIGNATURE = "L'équipe Relation Client B2B"


def call_llm_mock(scenario_id: str, emotion_id: str, familiarite_id: str) -> str:
    """Génère une réponse paramétrique sans appel API."""
    greeting = GREETINGS[familiarite_id][0]
    opening = OPENINGS[emotion_id][scenario_id]
    action_plan = ACTION_PLANS[emotion_id]
    contact = CONTACT_INFOS[familiarite_id]
    closing = CLOSINGS[familiarite_id]

    # Adapter le tutoiement pour familier
    if familiarite_id == "familier":
        opening = (
            opening.replace("Nous comprenons", "On comprend")
                   .replace("Nous prenons", "On prend")
                   .replace("Nous accusons", "Bien reçu")
                   .replace("Nous mobilisons", "On mobilise")
                   .replace("votre", "ton")
                   .replace("vos", "tes")
                   .replace("vous", "te")
        )
        action_plan = (
            action_plan.replace("Nous", "On")
                       .replace("vous", "te")
                       .replace("votre", "ton")
        )

    response = f"""{greeting}

{opening}

{action_plan}

{contact}

{closing}

{SIGNATURE}"""

    return response


def call_llm_openai(scenario_id: str, emotion_id: str, familiarite_id: str, model: str = "gpt-4o-mini") -> str:
    """Appel réel à l'API OpenAI."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("La bibliothèque 'openai' n'est pas installée. Lance `pip install openai`.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY non définie. Configure ton fichier .env.")

    client = OpenAI(api_key=api_key)
    prompt = build_prompt(scenario_id, emotion_id, familiarite_id)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Tu es un assistant B2B fiable, transparent et professionnel."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    return response.choices[0].message.content


def call_llm(scenario_id: str, emotion_id: str, familiarite_id: str, mode: str = "mock") -> dict:
    """Point d'entrée unique. Renvoie un dict avec metadata."""
    if mode == "openai":
        try:
            response = call_llm_openai(scenario_id, emotion_id, familiarite_id)
            return {"response": response, "mode": "openai", "error": None}
        except Exception as e:
            # Fallback sur mock en cas d'erreur API
            return {
                "response": call_llm_mock(scenario_id, emotion_id, familiarite_id),
                "mode": "mock (fallback)",
                "error": str(e),
            }
    else:
        return {
            "response": call_llm_mock(scenario_id, emotion_id, familiarite_id),
            "mode": "mock",
            "error": None,
        }
