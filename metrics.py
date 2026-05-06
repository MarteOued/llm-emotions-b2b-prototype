"""
Métriques exploratoires sur les réponses générées.
"""

import re

# Marqueurs de reconnaissance / empathie
RECO_MARKERS = [
    "nous comprenons",
    "nous reconnaissons",
    "excuses",
    "désolé",
    "désolés",
    "navrés",
    "regrettons",
    "présentons nos excuses",
    "on comprend",
]

# Marqueurs orientés solution
ACTION_MARKERS = [
    "plan d'action",
    "prochaines étapes",
    "prise en charge",
    "mise en place",
    "diagnostic",
    "résolution",
    "engagement",
    "compte-rendu",
    "remédiation",
]

# Marqueurs de formalité
FORMALITY_MARKERS = [
    "madame",
    "monsieur",
    "veuillez",
    "agréer",
    "salutations distinguées",
    "respectueusement",
]


def count_words(text: str) -> int:
    """Nombre de mots."""
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


def count_markers(text: str, markers: list) -> int:
    """Compte le nombre de marqueurs présents (case-insensitive)."""
    text_lower = text.lower()
    return sum(1 for m in markers if m in text_lower)


def has_vouvoiement(text: str) -> bool:
    """Détecte si le texte vouvoie."""
    text_lower = text.lower()
    vou_markers = [" vous ", " votre ", " vos "]
    return any(m in text_lower for m in vou_markers)


def has_tutoiement(text: str) -> bool:
    """Détecte si le texte tutoie."""
    text_lower = text.lower()
    tu_markers = [" tu ", " ton ", " ta ", " tes ", " toi "]
    return any(m in text_lower for m in tu_markers)


def compute_metrics(text: str) -> dict:
    """Calcule l'ensemble des métriques."""
    return {
        "nb_mots": count_words(text),
        "nb_marqueurs_reconnaissance": count_markers(text, RECO_MARKERS),
        "nb_marqueurs_action": count_markers(text, ACTION_MARKERS),
        "nb_marqueurs_formalite": count_markers(text, FORMALITY_MARKERS),
        "vouvoiement": has_vouvoiement(text),
        "tutoiement": has_tutoiement(text),
    }
