import json
import subprocess
from hex.investigation.domain import (
    InvestigationAgentPort, ClassifyResult, ExtractResult, NewClue, RateLimitError,
)

_HARDCODED_BLACKLIST = [
    "Sala Apolo", "Heliogàbal", "Primavera Sound", "Sónar", "Razzmatazz",
    "BARTS", "Bikini", "Luz de Gas", "Jamboree", "Palau Sant Jordi",
    "FIB", "Viña Rock", "Mad Cool", "BBK Live",
]

_CLASSIFY_SYSTEM = """Ets un agent de recerca per a una banda de rock alternatiu en CATALÀ que acaba de començar.
Tenim 0 seguidors, 0 actuacions, cap segell ni booking. Busquem contactes per fer els PRIMERS concerts.

Classifica la pista donada i extreu informació útil.

TIPUS possibles:
- scout: artista/banda del circuit indie/alternatiu català que pot revelar venues i festivals on toca
- entity: venue, festival, booking, media, associació, cicle municipal, etc. (alguna cosa a contactar)
- unknown: no classificable o irrelevant

Si és "entity": extreu nom (SENSE prefix "Sala"/"Festival"/"Teatre"), mail, web, telefon, persona_contacte, notes, idioma de contacte.
Si és "scout": busca el seu historial de concerts (Songkick, Instagram, Bandcamp) dels últims 2 anys.

A "new_clues": noms de venues/festivals/bookings trobats. Prioritza llocs PETITS i EMERGENTS.
IMPORTANT - mai suggereixis: """ + ", ".join(_HARDCODED_BLACKLIST) + """

NOM: mai ussis prefixos com "Sala", "Festival", "Teatre". Exemple: "Paupaterres" no "Festival Paupaterres".

SCORING new_clues (0-10):
+5 si acull bandes emergents sense historial (cicles municipals, espais joves)
+4 si Catalunya/Illes Balears/País Valencià
+3 si rock, indie, alternatiu, punk, post-rock, folk
+2 si aforament <300 o gratuït/popular
-4 si aforament >1000 o festival famós nacional
-3 si fora d'Espanya
-2 si clàssica, flamenc, reggaeton, electrònica

IMPORTANT: Respon ÚNICAMENT amb JSON vàlid. Zero text addicional."""

_CLASSIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["scout", "entity", "unknown"]},
        "nom": {"type": ["string", "null"]},
        "mail": {"type": ["string", "null"]},
        "web": {"type": ["string", "null"]},
        "persona_contacte": {"type": ["string", "null"]},
        "telefon": {"type": ["string", "null"]},
        "notes": {"type": ["string", "null"]},
        "idioma": {"type": ["string", "null"]},
        "new_clues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "clue": {"type": "string"},
                    "score": {"type": "integer", "minimum": 0, "maximum": 10},
                },
                "required": ["clue", "score"],
            },
        },
    },
    "required": ["type", "new_clues"],
}

_EXTRACT_SYSTEM = """Ets un agent de recerca per a una banda de rock alternatiu en CATALÀ que acaba de començar.
Tenim 0 seguidors, 0 actuacions, cap segell ni booking. Busquem el mail/contacte d'aquesta entitat.

Extreu: nom (SENSE prefix), mail de booking/programació (preferent al genèric), web, telefon, persona_contacte, notes, idioma.

IMPORTANT: Respon ÚNICAMENT amb JSON vàlid. Zero text addicional."""

_EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "nom": {"type": "string"},
        "mail": {"type": "string"},
        "web": {"type": ["string", "null"]},
        "persona_contacte": {"type": ["string", "null"]},
        "telefon": {"type": ["string", "null"]},
        "notes": {"type": ["string", "null"]},
        "idioma": {"type": ["string", "null"]},
        "new_clues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "clue": {"type": "string"},
                    "score": {"type": "integer", "minimum": 0, "maximum": 10},
                },
                "required": ["clue", "score"],
            },
        },
    },
    "required": ["nom", "mail"],
}

_RATE_LIMIT_SIGNALS = ["rate limit", "rate_limit", "too many requests", "429"]


class ClaudeCliAgent(InvestigationAgentPort):
    def __init__(self, model="haiku"):
        self.model = model

    def classify(self, clue: str, top_returned: list[str]) -> ClassifyResult:
        avoid = ", ".join(top_returned[:20]) if top_returned else "—"
        prompt = (
            f'Investiga aquesta pista: "{clue}".\n'
            f'Evita suggerir entitats que ja tenim: {avoid}.\n'
            f'Respon ÚNICAMENT amb JSON vàlid.'
        )
        raw = self._run(prompt, _CLASSIFY_SYSTEM, _CLASSIFY_SCHEMA)
        data = self._parse(raw)
        new_clues = [NewClue(c["clue"], int(c.get("score", 5))) for c in data.get("new_clues", [])]
        return ClassifyResult(
            type=data.get("type", "unknown"),
            new_clues=new_clues,
            nom=data.get("nom"),
            mail=data.get("mail"),
            web=data.get("web"),
            persona_contacte=data.get("persona_contacte"),
            telefon=data.get("telefon"),
            notes=data.get("notes"),
            idioma=data.get("idioma"),
        )

    def extract(self, clue: str) -> ExtractResult:
        prompt = f'Extreu informació de contacte per a: "{clue}". Respon ÚNICAMENT amb JSON vàlid.'
        raw = self._run(prompt, _EXTRACT_SYSTEM, _EXTRACT_SCHEMA)
        data = self._parse(raw)
        new_clues = [NewClue(c["clue"], int(c.get("score", 5))) for c in data.get("new_clues", [])]
        return ExtractResult(
            nom=data.get("nom", clue),
            mail=data.get("mail", ""),
            web=data.get("web") or "",
            persona_contacte=data.get("persona_contacte") or "",
            telefon=data.get("telefon") or "",
            notes=data.get("notes") or "",
            idioma=data.get("idioma") or "",
            new_clues=new_clues,
        )

    def _run(self, prompt: str, system: str, schema: dict) -> str:
        cmd = [
            "claude", "-p", prompt,
            "--model", self.model,
            "--output-format", "json",
            "--json-schema", json.dumps(schema),
            "--allowedTools", "WebSearch",
            "--system-prompt", system,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        combined = (result.stdout + result.stderr).lower()
        if any(sig in combined for sig in _RATE_LIMIT_SIGNALS):
            raise RateLimitError("Claude CLI rate limited")
        if result.returncode != 0:
            raise RuntimeError(f"claude CLI error (rc={result.returncode}): {result.stderr[:300]}")
        return result.stdout

    def _parse(self, raw: str) -> dict:
        import ast
        raw = raw.strip()
        for key in ("structured_output", "result"):
            try:
                outer = json.loads(raw)
                inner = outer.get(key)
                if isinstance(inner, dict):
                    return inner
                if isinstance(inner, str):
                    try:
                        return json.loads(inner)
                    except Exception:
                        return ast.literal_eval(inner)
            except Exception:
                pass
        try:
            return json.loads(raw)
        except Exception:
            pass
        raise RuntimeError(f"unparseable agent output: {raw[:200]}")
