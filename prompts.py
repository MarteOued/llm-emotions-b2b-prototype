"""
Scénarios B2B + paramètres émotionnels et de familiarité.
Tiré du notebook de recherche, structuré en module Python réutilisable.
"""

# =====================================================================
# SCÉNARIOS B2B (textes neutres, factuels)
# =====================================================================
SCENARIOS = {
    "S1_retard_livraison": {
        "titre": "Retard de livraison",
        "contexte": "Chaîne logistique / livraison de matériel",
        "probleme": "Retard de livraison d'un matériel critique",
        "enjeu_client": "Blocage de mise en production et mobilisation des équipes",
        "emotion_probable_client": "Frustration / inquiétude",
        "icone": "📦",
        "texte_neutre": (
            "Le client attend une livraison de matériel indispensable au démarrage d'un site. "
            "La livraison prévue le 10 du mois n'a pas eu lieu. "
            "Le client indique que cela bloque la mise en production et mobilise ses équipes. "
            "Le client demande une date fiable, un plan de rattrapage et une explication."
        ),
    },
    "S2_panne_logicielle": {
        "titre": "Panne logicielle SaaS",
        "contexte": "SaaS / application métier",
        "probleme": "Indisponibilité d'un service",
        "enjeu_client": "Interruption d'activité et dépassement de SLA",
        "emotion_probable_client": "Stress / urgence",
        "icone": "🖥️",
        "texte_neutre": (
            "Le client signale une indisponibilité du service depuis 09:15. "
            "Plusieurs équipes ne peuvent plus accéder aux fonctionnalités critiques. "
            "Le client demande un diagnostic, une estimation de reprise et une mesure de mitigation."
        ),
    },
    "S3_erreur_facturation": {
        "titre": "Erreur de facturation",
        "contexte": "Facturation / abonnement",
        "probleme": "Montant facturé non conforme au contrat",
        "enjeu_client": "Risque de litige et blocage du paiement",
        "emotion_probable_client": "Mécontentement",
        "icone": "💳",
        "texte_neutre": (
            "Le client indique qu'une facture inclut des lignes non prévues au contrat. "
            "Le client demande la justification des montants, une correction et une confirmation écrite."
        ),
    },
    "S4_non_respect_SLA": {
        "titre": "Non-respect du SLA",
        "contexte": "Support / centre de services",
        "probleme": "Délais de réponse non conformes au SLA",
        "enjeu_client": "Risque opérationnel et escalade interne",
        "emotion_probable_client": "Irritation",
        "icone": "⏱️",
        "texte_neutre": (
            "Le client constate que les délais de réponse observés dépassent les engagements SLA. "
            "Le client demande les causes, un plan de retour au niveau de service et un reporting."
        ),
    },
    "S5_ticket_sans_reponse": {
        "titre": "Ticket sans réponse",
        "contexte": "Support / suivi de tickets",
        "probleme": "Tickets bloquants sans réponse depuis 72h",
        "enjeu_client": "Ralentissement projet et risque de churn",
        "emotion_probable_client": "Frustration",
        "icone": "🎫",
        "texte_neutre": (
            "Le client indique que plusieurs tickets ouverts restent sans réponse depuis 72 heures. "
            "Il précise que ces demandes concernent des anomalies bloquantes. "
            "Il demande une prise en charge immédiate et un point de contact unique."
        ),
    },
}

# =====================================================================
# REGISTRES ÉMOTIONNELS
# =====================================================================
EMOTIONS = {
    "neutre": {
        "label": "Neutre",
        "icone": "📋",
        "description": "Factuel, informatif, sans marque émotionnelle.",
        "marqueurs": ["information", "constat", "étapes"],
        "couleur": "#94A3B8",
    },
    "empathique": {
        "label": "Empathique",
        "icone": "💙",
        "description": "Reconnaissance explicite de l'impact côté client, ton respectueux et humain.",
        "marqueurs": ["nous comprenons", "impact", "excuses"],
        "couleur": "#60A5FA",
    },
    "rassurant": {
        "label": "Rassurant",
        "icone": "🛡️",
        "description": "Calme et orienté solution, réduit l'incertitude, donne un plan clair.",
        "marqueurs": ["prise en charge", "plan", "prochaines étapes", "délai"],
        "couleur": "#34D399",
    },
    "tres_professionnel": {
        "label": "Très professionnel",
        "icone": "🎓",
        "description": "Très formel, orienté gouvernance, conformité et engagement écrit.",
        "marqueurs": ["conformité", "SLA", "engagement", "compte-rendu"],
        "couleur": "#F472B6",
    },
}

# =====================================================================
# NIVEAUX DE FAMILIARITÉ
# =====================================================================
FAMILIARITES = {
    "tres_formel": {
        "label": "Très formel",
        "icone": "🎩",
        "description": "Vouvoiement strict, formules de politesse complètes, style institutionnel.",
        "regles": ["vouvoiement", "Madame/Monsieur", "phrases longues et structurées"],
    },
    "semi_formel": {
        "label": "Semi-formel",
        "icone": "👔",
        "description": "Vouvoiement, ton cordial et direct, structure claire.",
        "regles": ["vouvoiement", "formules courtes", "style pragmatique"],
    },
    "familier": {
        "label": "Familier",
        "icone": "👋",
        "description": "Tutoiement et proximité (à utiliser seulement si la relation le permet).",
        "regles": ["tutoiement", "phrases plus courtes", "chaleur et proximité"],
    },
}


def build_prompt(scenario_id: str, emotion_id: str, familiarite_id: str) -> str:
    """Construit le méta-prompt à envoyer au LLM."""
    scenario = SCENARIOS[scenario_id]
    emo = EMOTIONS[emotion_id]
    fam = FAMILIARITES[familiarite_id]

    return f"""Tu es un agent de relation client B2B représentant une entreprise de services.

Contexte du scénario (neutre, faits uniquement) :
{scenario["texte_neutre"]}

Registre émotionnel attendu :
- {emotion_id} : {emo["description"]}
Marqueurs conseillés : {", ".join(emo["marqueurs"])}

Niveau de familiarité attendu :
- {familiarite_id} : {fam["description"]}
Règles : {", ".join(fam["regles"])}

Contraintes (obligatoires) :
- rester professionnel et respectueux
- reconnaître l'échec / l'incident
- ne pas manipuler émotionnellement
- donner un plan d'action (prochaines étapes, délais, point de contact)
- si information manquante : demander les précisions nécessaires

Rédige une réponse email courte (150 à 220 mots), structurée en 3 à 5 paragraphes."""
