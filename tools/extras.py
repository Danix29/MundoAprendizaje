# -*- coding: utf-8 -*-
"""Genera data/packs.js y data/videos.js a partir del catalogo de temas y cursos."""

import io, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import generar_fichas as G
from build import js, escribir, CURRICULOS

GENERADOS = sorted(CURRICULOS.keys())
PRECIO_TEMA_CURSO = 1.99
PRECIO_CURSO = 5.99
PRECIO_COMPLETO = 19.99

def main():
    packs = []
    for tema, t in G.TEMAS.items():
        for curso, c in sorted(G.CURSOS.items()):
            packs.append({
                "id": "pack-%s-%d" % (tema, curso),
                "tipo": "tema-curso", "tema": tema, "curso": curso,
                "titulo": "%s — %s" % (t["nombre"], c["etiqueta"]),
                "resumen": "Las 20 fichas de %s para %s (%s), en PDF listo para imprimir."
                           % (t["nombre"], c["etiqueta"], c["etapa"]),
                "nFichas": 20, "precio": PRECIO_TEMA_CURSO,
                "disponible": tema in GENERADOS,
                "payhipId": "PENDIENTE-%s-%d" % (tema, curso),
            })
    for curso, c in sorted(G.CURSOS.items()):
        packs.append({
            "id": "pack-curso-%d" % curso, "tipo": "curso", "tema": None, "curso": curso,
            "titulo": "Curso completo — %s" % c["etiqueta"],
            "resumen": "Los cuatro temas del curso de %s (%s): 80 fichas en PDF, uno por rincón."
                       % (c["etiqueta"], c["etapa"]),
            "nFichas": 80, "precio": PRECIO_CURSO,
            "disponible": len(GENERADOS) == len(G.TEMAS),
            "payhipId": "PENDIENTE-curso-%d" % curso,
        })
    packs.append({
        "id": "pack-completo", "tipo": "completo", "tema": None, "curso": None,
        "titulo": "Pack completo Mundo Aprendizaje",
        "resumen": "Los 4 temas y los 6 cursos: 480 fichas en PDF, de 2 a 7 años.",
        "nFichas": 20 * len(G.CURSOS) * len(G.TEMAS), "precio": PRECIO_COMPLETO,
        "disponible": len(GENERADOS) == len(G.TEMAS),
        "payhipId": "PENDIENTE-completo",
    })

    tam = escribir("data/packs.js", js("MA_PACKS", None, {
        "moneda": "EUR",
        # PENDIENTE: sustituir por el usuario real de Payhip al crear la cuenta.
        "payhipUsuario": "PENDIENTE-USUARIO-PAYHIP",
        "packs": packs,
    }))
    print("  data/packs.js    %d packs (%d disponibles)  %.1f KB"
          % (len(packs), sum(1 for p in packs if p["disponible"]), tam / 1024))

    # Videos: un hueco por tema y curso. Al llegar el video real basta con
    # rellenar "url" y "duracion"; el diseno no se toca.
    videos = []
    for tema, t in G.TEMAS.items():
        for curso, c in sorted(G.CURSOS.items()):
            videos.append({
                "id": "vid-%s-%d" % (tema, curso),
                "tema": tema, "curso": curso,
                "titulo": "%s en %s: por dónde empezar" % (t["nombre"], c["etiqueta"]),
                "descripcion": "Cómo acompañar en casa las fichas de %s de %s, paso a paso."
                               % (t["nombre"], c["etiqueta"]),
                "duracion": None,   # p. ej. "4:15"
                "url": None,        # p. ej. "https://www.youtube.com/embed/XXXX"
                "proximamente": True,
            })
    tam = escribir("data/videos.js", js("MA_VIDEOS", None, videos))
    print("  data/videos.js   %d huecos de video  %.1f KB" % (len(videos), tam / 1024))

if __name__ == "__main__":
    main()
