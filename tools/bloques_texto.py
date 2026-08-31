# -*- coding: utf-8 -*-
"""
Tipos de bloque para Lenguaje, Historia e Idiomas.

Complementan los de generar_fichas.py (que son sobre todo numericos). Igual que
alli, todo lo verificable se calcula: las silabas se parten con un algoritmo, no
a mano, y las respuestas de verdadero/falso viajan con la afirmacion.
"""

import re

VOCALES = "aeiouáéíóúü"


# --------------------------------------------------------------------- silabas
def separar_silabas(palabra):
    """
    Separacion silabica del espanol para palabras sencillas de Infantil y
    primer ciclo: estructuras V, CV, CVC y los digrafos ch, ll, rr, qu, gu.
    No cubre todos los casos del idioma, pero si el vocabulario que usamos,
    y `validar.py` comprueba que la reconstruccion coincide con la palabra.
    """
    p = palabra.lower()
    digrafos = ("ch", "ll", "rr", "qu", "gu")
    grupos_cons = ("bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr",
                   "pl", "pr", "tl", "tr")

    # 1. Trocear en unidades: digrafo o letra suelta
    unidades, i = [], 0
    while i < len(p):
        if p[i:i + 2] in digrafos:
            unidades.append(p[i:i + 2]); i += 2
        else:
            unidades.append(p[i]); i += 1

    # 2. Agrupar consonantes iniciales + vocal, y cerrar con coda si procede
    silabas, actual = [], ""
    j = 0
    while j < len(unidades):
        u = unidades[j]
        if u[0] not in VOCALES:
            # Grupo consonantico inseparable delante de vocal
            if (j + 2 < len(unidades) and u + unidades[j + 1] in grupos_cons
                    and unidades[j + 2][0] in VOCALES):
                actual += u + unidades[j + 1]; j += 2; continue
            if actual and any(c in VOCALES for c in actual):
                # Consonante entre vocales: abre silaba nueva
                siguiente = unidades[j + 1] if j + 1 < len(unidades) else ""
                if siguiente and siguiente[0] in VOCALES:
                    silabas.append(actual); actual = u; j += 1; continue
                # Consonante final o coda
                actual += u; silabas.append(actual); actual = ""; j += 1; continue
            actual += u; j += 1; continue
        # Vocal
        actual += u
        siguiente = unidades[j + 1] if j + 1 < len(unidades) else ""
        if not siguiente:
            silabas.append(actual); actual = ""
        j += 1

    if actual:
        if silabas and not any(c in VOCALES for c in actual):
            silabas[-1] += actual        # coda suelta al final
        else:
            silabas.append(actual)

    # Preservar mayusculas/acentos del original
    salida, k = [], 0
    for s in silabas:
        salida.append(palabra[k:k + len(s)])
        k += len(s)
    return [s for s in salida if s]


def b_silabas(r, palabras, enunciado=None):
    items = []
    for emoji, palabra in palabras:
        items.append({"emoji": emoji, "palabra": palabra,
                      "silabas": separar_silabas(palabra)})
    return {
        "tipo": "silabas",
        "enunciado": enunciado or "Da una palmada por cada sílaba y escribe cuántas tiene.",
        "items": items,
    }


# ------------------------------------------------------------------- escritura
def b_escritura(r, palabras, enunciado=None):
    """Palabra para repasar + linea de pauta para escribirla sola."""
    return {
        "tipo": "escritura",
        "enunciado": enunciado or "Repasa la palabra y después escríbela tú en la línea.",
        "items": [{"emoji": e, "palabra": p} for e, p in palabras],
    }


def b_completar(r, items, enunciado=None):
    """
    items: lista de (emoji, palabra, indice_de_la_letra_que_falta)
    La palabra se parte en el generador para que el hueco siempre encaje.
    """
    salida = []
    for emoji, palabra, i in items:
        salida.append({
            "emoji": emoji,
            "antes": palabra[:i],
            "falta": palabra[i],
            "despues": palabra[i + 1:],
            "palabra": palabra,
        })
    return {
        "tipo": "completar",
        "enunciado": enunciado or "Escribe la letra que falta en cada palabra.",
        "items": salida,
    }


# ------------------------------------------------------------------ clasificar
def b_clasificar(r, columnas, elementos, enunciado=None):
    """
    columnas: lista de nombres de columna
    elementos: lista de (contenido, indice_de_columna_correcta)
    Los elementos se barajan; la solucion viaja aparte.
    """
    mezcla = elementos[:]
    r.shuffle(mezcla)
    return {
        "tipo": "clasificar",
        "enunciado": enunciado or "Escribe cada dibujo en la columna que le corresponde.",
        "columnas": columnas,
        "items": [{"contenido": c, "columna": i} for c, i in mezcla],
    }


# --------------------------------------------------------------------- lectura
def b_lectura(r, texto, preguntas, enunciado=None):
    """preguntas: lista de (pregunta, respuesta_esperada)"""
    return {
        "tipo": "lectura",
        "enunciado": enunciado or "Lee el texto y contesta a las preguntas.",
        "texto": texto,
        "items": [{"pregunta": p, "r": resp} for p, resp in preguntas],
    }


def b_verdadero_falso(r, afirmaciones, enunciado=None):
    """afirmaciones: lista de (texto, True/False)"""
    mezcla = afirmaciones[:]
    r.shuffle(mezcla)
    return {
        "tipo": "verdadero-falso",
        "enunciado": enunciado or "Lee cada frase y marca si es verdadera (V) o falsa (F).",
        "items": [{"texto": t, "r": bool(v)} for t, v in mezcla],
    }


def b_ordenar(r, elementos, enunciado=None):
    """
    elementos: lista de (contenido, posicion_correcta_1_a_n) ya en orden.
    Se presentan barajados para que el alumno los numere.
    """
    indices = list(range(len(elementos)))
    r.shuffle(indices)
    return {
        "tipo": "ordenar",
        "enunciado": enunciado or "Numera del 1 al %d en el orden correcto." % len(elementos),
        "items": [{"contenido": elementos[i][0], "orden": elementos[i][1]} for i in indices],
    }


def b_dibujar(r, consigna, pie=None, alto="grande"):
    return {
        "tipo": "dibujar",
        "enunciado": consigna,
        "pie": pie or "Dibuja aquí dentro",
        "alto": alto,
        "items": [],
    }


# -------------------------------------------------------------------- idiomas
def b_vocabulario(r, palabras, enunciado=None):
    """palabras: lista de (emoji, ingles, espanol). Palabra inglesa para repasar."""
    return {
        "tipo": "vocabulario",
        "enunciado": enunciado or "Repasa la palabra en inglés y dila en voz alta.",
        "items": [{"emoji": e, "en": en, "es": es} for e, en, es in palabras],
    }


def b_frase(r, frases, enunciado=None):
    """frases: lista de (inicio, hueco_esperado, final)"""
    return {
        "tipo": "frase",
        "enunciado": enunciado or "Completa cada frase con la palabra que falta.",
        "items": [{"antes": a, "r": h, "despues": f} for a, h, f in frases],
    }


def b_colorear_ingles(r, items, enunciado=None):
    """items: lista de (forma, palabra_inglesa, color_css_de_referencia)"""
    return {
        "tipo": "colorear-ingles",
        "enunciado": enunciado or "Colorea cada dibujo del color que dice su nombre en inglés.",
        "items": [{"forma": f, "en": en, "pista": p} for f, en, p in items],
    }
