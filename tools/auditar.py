# -*- coding: utf-8 -*-
"""Informe de completitud del catalogo: tema x curso x numero de fichas."""
import glob, io, json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import generar_fichas as G

MIN = 20

def cargar(ruta):
    t = io.open(ruta, encoding="utf-8").read()
    return json.loads(t[t.index("] = ") + 4:t.rindex(";")])

def main(carpeta="dist/fichas"):
    datos = {}
    for ruta in glob.glob(os.path.join(RAIZ, carpeta, "*.js")):
        clave = os.path.basename(ruta)[:-3]
        tema, curso = clave.rsplit("-", 1)
        datos[(tema, int(curso))] = cargar(ruta)

    cursos = sorted(G.CURSOS)
    temas = list(G.TEMAS)
    ancho = 14

    print("INFORME DE COMPLETITUD  (minimo exigido: %d fichas por celda)" % MIN)
    print("Fuente: %s/\n" % carpeta)
    print("%-14s" % "TEMA" + "".join("%9s" % ("%d anos" % c) for c in cursos) + "%9s" % "TOTAL")
    print("-" * (14 + 9 * (len(cursos) + 1)))

    faltan = []
    total_global = 0
    for tema in temas:
        fila = "%-14s" % G.TEMAS[tema]["nombre"]
        total_tema = 0
        for curso in cursos:
            fichas = datos.get((tema, curso), [])
            n = len(fichas)
            total_tema += n
            marca = "" if n >= MIN else " !"
            fila += "%9s" % ("%d%s" % (n, marca))
            if n < MIN:
                faltan.append((tema, curso, n, MIN - n))
        fila += "%9d" % total_tema
        total_global += total_tema
        print(fila)

    print("-" * (14 + 9 * (len(cursos) + 1)))
    print("%-14s" % "TOTAL" + "".join(
        "%9d" % sum(len(datos.get((t, c), [])) for t in temas) for c in cursos)
        + "%9d" % total_global)

    objetivo = len(temas) * len(cursos) * MIN
    print("\nObjetivo: %d fichas (%d temas x %d cursos x %d)" % (objetivo, len(temas), len(cursos), MIN))
    print("Actual  : %d fichas  (%.0f%%)" % (total_global, 100.0 * total_global / objetivo))

    # Fichas vacias o sin ejercicios reales
    sospechosas = []
    for (tema, curso), fichas in sorted(datos.items()):
        for f in fichas:
            if not f.get("bloques"):
                sospechosas.append("%s: sin bloques" % f["id"])
            # Estos tipos no llevan `items` por diseño: son zonas en blanco
            # (dibujar), columnas (unir) o series de glifos (trazo).
            elif all(not b.get("items")
                     and b["tipo"] not in ("trazo", "formas", "concepto", "unir", "dibujar")
                     for b in f["bloques"]):
                sospechosas.append("%s: bloques sin contenido" % f["id"])
    print("\nFichas vacias o placeholder: %d" % len(sospechosas))
    for s in sospechosas[:10]:
        print("   - %s" % s)

    return faltan

if __name__ == "__main__":
    faltan = main(sys.argv[1] if len(sys.argv) > 1 else "dist/fichas")
    if faltan:
        print("\nCELDAS INCOMPLETAS (%d de %d):" % (len(faltan), len(G.TEMAS) * len(G.CURSOS)))
        for tema, curso, n, deficit in faltan:
            print("   %-12s %d anos -> %2d fichas (faltan %2d)"
                  % (G.TEMAS[tema]["nombre"], curso, n, deficit))
