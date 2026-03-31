#!/usr/bin/env bash
SCHEMA='{"type":"object","properties":{"type":{"type":"string","enum":["scout","entity","unknown"]},"summary":{"type":["string","null"]},"nom":{"type":["string","null"]},"mail":{"type":["string","null"]},"web":{"type":["string","null"]},"persona_contacte":{"type":["string","null"]},"telefon":{"type":["string","null"]},"notes":{"type":["string","null"]},"idioma":{"type":["string","null"]},"new_clues":{"type":"array","items":{"type":"object","properties":{"clue":{"type":"string"},"score":{"type":"integer","minimum":0,"maximum":10}},"required":["clue","score"]}}},"required":["type","new_clues","summary"]}'

PROMPT='Investiga aquesta pista: "Ítaca Sant Joan".
Evita suggerir entitats que ja tenim: La Clota (Vic), Cafè de l'"'"'Orfeó, inconexia festival, Osona Music.
Respon ÚNICAMENT amb JSON vàlid.'

SYSTEM='Ets un agent de recerca per a una banda de rock alternatiu en CATALÀ que acaba de començar.
Tenim 0 seguidors, 0 actuacions, cap segell ni booking. Busquem contactes per fer els PRIMERS concerts.

Classifica la pista donada i extreu informació útil.

TIPUS possibles:
- scout: artista/banda del circuit indie/alternatiu català que pot revelar venues i festivals on toca
- entity: venue, festival, booking, media, associació, cicle municipal, etc. (alguna cosa a contactar)
- unknown: no classificable o irrelevant

Si és "entity": extreu nom (SENSE prefix "Sala"/"Festival"/"Teatre"), mail, web, telefon, persona_contacte, notes, idioma de contacte.
Si és "scout": busca el seu historial de concerts (Songkick, Instagram, Bandcamp, pàgina web) dels últims 2 anys.

A "new_clues": noms de venues/festivals/bookings trobats. Prioritza llocs PETITS i EMERGENTS.
IMPORTANT - mai suggereixis: Sala Apolo, Heliogàbal, Primavera Sound, Sónar, Razzmatazz, BARTS, Bikini, Luz de Gas, Jamboree, Palau Sant Jordi, FIB, Viña Rock, Mad Cool, BBK Live

NOM: mai ussis prefixos com "Sala", "Festival", "Teatre".

SCORING new_clues (0-10):
+5 si acull bandes emergents sense historial
+4 si Catalunya/Illes Balears/País Valencià
+3 si rock, indie, alternatiu, punk, post-rock, folk
+2 si aforament <300 o gratuït/popular
-4 si aforament >1000 o festival famós nacional
-3 si fora d'"'"'Espanya
-2 si clàssica, flamenc, reggaeton, electrònica

IMPORTANT: Respon ÚNICAMENT amb JSON vàlid. Zero text addicional.'

time claude \
  -p "$PROMPT" \
  --model haiku \
  --output-format json \
  --max-turns 5 \
  --verbose \
  --json-schema "$SCHEMA" \
  --allowedTools WebSearch \
  --system-prompt "$SYSTEM"
