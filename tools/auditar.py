# -*- coding: utf-8 -*-
"""Informe de completitud del catalogo: tema x curso x numero de fichas."""
import glob, io, json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import generar_fichas as G

MIN = 20      # fichas por celda
MIN_EJ = 5    # ejercicios por ficha

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

    print("INFORME DE COMPLETITUD")
    print("Minimos exigidos: %d fichas por celda, %d ejercicios por ficha" % (MIN, MIN_EJ))
    print("Fuente: %s/\n" % carpeta)
    print("Cada celda: FICHAS (ejercicios minimos-maximos por ficha)\n")
    print("%-14s" % "TEMA" + "".join("%14s" % ("%d anos" % c) for c in cursos) + "%9s" % "TOTAL")
    print("-" * (14 + 14 * len(cursos) + 9))

    faltan = []
    pobres = []
    total_global = 0
    for tema in temas:
        fila = "%-14s" % G.TEMAS[tema]["nombre"]
        total_tema = 0
        for curso in cursos:
            fichas = datos.get((tema, curso), [])
            n = len(fichas)
            total_tema += n
            ejercicios = [len(f["bloques"]) for f in fichas] or [0]
            lo, hi = min(ejercicios), max(ejercicios)
            marca = "" if n >= MIN and lo >= MIN_EJ else " !"
            fila += "%14s" % ("%d (%d-%d)%s" % (n, lo, hi, marca))
            if n < MIN:
                faltan.append((tema, curso, n, MIN - n))
            if lo < MIN_EJ:
                pobres.append((tema, curso, lo))
        fila += "%9d" % total_tema
        total_global += total_tema
        print(fila)

    print("-" * (14 + 14 * len(cursos) + 9))
    print("%-14s" % "TOTAL" + "".join(
        "%14d" % sum(len(datos.get((t, c), [])) for t in temas) for c in cursos)
        + "%9d" % total_global)

    todos_ej = [len(f["bloques"]) for fs in datos.values() for f in fs]
    if todos_ej:
        print()
        print("Ejercicios por ficha: minimo %d, media %.2f, maximo %d"
              % (min(todos_ej), sum(todos_ej) / float(len(todos_ej)), max(todos_ej)))
        print("Ejercicios totales  : %d" % sum(todos_ej))
        print("Fichas por debajo de %d ejercicios: %d" % (MIN_EJ, sum(1 for e in todos_ej if e < MIN_EJ)))

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
