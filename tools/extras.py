# -*- coding: utf-8 -*-
"""Genera data/packs.js y data/videos.js a partir del catalogo de temas y cursos."""

import io, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import generar_fichas as G
from build import js, escribir, CURRICULOS


# ============================================================================
# IDs REALES DE PAYHIP
# Se guardan aqui, y no directamente en data/packs.js, porque extras.py
# sobrescribe ese archivo: si se editaran alli se perderian al regenerar.
# No son secretos: son los identificadores publicos de cada producto, los
# mismos que aparecen en la URL de compra payhip.com/b/<id>.
# ============================================================================
PAYHIP_USUARIO = "MundoAprendizaje"

PAYHIP_TEMA_CURSO = {
    ("matematicas", 2): "7jdDy", ("matematicas", 3): "HEmyW",
    ("matematicas", 4): "JzDXt", ("matematicas", 5): "Tbr3W",
    ("matematicas", 6): "ebk9X", ("matematicas", 7): "j9WfG",
    ("lenguaje", 2): "6ofCL", ("lenguaje", 3): "x4PV9",
    ("lenguaje", 4): "Z8q6Q", ("lenguaje", 5): "aN5IB",
    ("lenguaje", 6): "Ij6lQ", ("lenguaje", 7): "U7cJv",
    ("historia", 2): "PyEKX", ("historia", 3): "jDOfP",
    ("historia", 4): "Dj7MN", ("historia", 5): "pYUQA",
    ("historia", 6): "dOgnk", ("historia", 7): "cy8PQ",
    ("idiomas", 2): "ySmDl", ("idiomas", 3): "TWPps",
    ("idiomas", 4): "GMov7", ("idiomas", 5): "BbJjp",
    ("idiomas", 6): "mPr6T", ("idiomas", 7): "Q3roq",
}

# Los packs de curso y el completo son "bundles" de Payhip: agrupan los
# productos ya creados en vez de repetir los PDF. Asi el pack completo no
# tiene que subir 71 MB de archivos.
PAYHIP_CURSO = {2: "8zJx1", 3: "kbVeW", 4: "0Ljqa",
                5: "siNpx", 6: "zhaUA", 7: "09MTq"}
PAYHIP_COMPLETO = "Q0esT"

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
                "payhipId": PAYHIP_TEMA_CURSO.get((tema, curso)),
            })
    for curso, c in sorted(G.CURSOS.items()):
        packs.append({
            "id": "pack-curso-%d" % curso, "tipo": "curso", "tema": None, "curso": curso,
            "titulo": "Curso completo — %s" % c["etiqueta"],
            "resumen": "Los cuatro temas del curso de %s (%s): 80 fichas en PDF, uno por rincón."
                       % (c["etiqueta"], c["etapa"]),
            "nFichas": 80, "precio": PRECIO_CURSO,
            "disponible": True,
            "payhipId": PAYHIP_CURSO.get(curso),
        })
    packs.append({
        "id": "pack-completo", "tipo": "completo", "tema": None, "curso": None,
        "titulo": "Pack completo Mundo Aprendizaje",
        "resumen": "Los 4 temas y los 6 cursos: 480 fichas en PDF, de 2 a 7 años.",
        "nFichas": 20 * len(G.CURSOS) * len(G.TEMAS), "precio": PRECIO_COMPLETO,
        "disponible": True,
        "payhipId": PAYHIP_COMPLETO,
    })

    tam = escribir("data/packs.js", js("MA_PACKS", None, {
        "moneda": "EUR",
        # PENDIENTE: sustituir por el usuario real de Payhip al crear la cuenta.
        "payhipUsuario": PAYHIP_USUARIO,
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
