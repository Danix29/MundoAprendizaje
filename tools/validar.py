# -*- coding: utf-8 -*-
"""
Validador del contenido generado.

Comprueba que todo lo que se va a imprimir es correcto: operaciones, series,
comparaciones, descomposiciones y tablas. Tambien verifica que la dificultad
progresa de curso en curso y que no hay fichas vacias.

Uso:  python tools/validar.py
"""

import glob
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errores = []
avisos = []


def cargar(ruta):
    """Extrae el objeto JSON del archivo .js generado."""
    txt = io.open(ruta, encoding="utf-8").read()
    inicio = txt.index("] = ") + 4
    return json.loads(txt[inicio:txt.rindex(";")])


def err(fid, msg):
    errores.append("%s: %s" % (fid, msg))


def validar_bloque(fid, b):
    t = b["tipo"]
    items = b.get("items", [])

    if t == "operaciones":
        for it in items:
            a, op, bb, res = it["a"], it["op"], it["b"], it["r"]
            esperado = {"+": a + bb, "-": a - bb, "×": a * bb}[op]
            if res != esperado:
                err(fid, "operacion mal: %d %s %d = %d (deberia ser %d)" % (a, op, bb, res, esperado))
            if op == "-" and res < 0:
                err(fid, "resta con resultado negativo: %d - %d" % (a, bb))

    elif t == "comparar":
        for it in items:
            a, bb, res = it["a"], it["b"], it["r"]
            esperado = "=" if a == bb else ("<" if a < bb else ">")
            if res != esperado:
                err(fid, "comparacion mal: %d %s %d" % (a, res, bb))

    elif t == "serie":
        for it in items:
            v, paso = it["valores"], it["paso"]
            for i in range(1, len(v)):
                if v[i] - v[i - 1] != paso:
                    err(fid, "serie no aritmetica: %s (paso %d)" % (v, paso))
                    break
            if any(x < 0 for x in v):
                err(fid, "serie con negativos: %s" % v)
            if not it["huecos"] or max(it["huecos"]) >= len(v):
                err(fid, "hueco de serie fuera de rango: %s" % it["huecos"])

    elif t == "descomponer":
        total = b["total"]
        for it in items:
            if it["parte"] + it["r"] != total:
                err(fid, "descomposicion mal: %d + %d != %d" % (it["parte"], it["r"], total))
            if it["parte"] <= 0 or it["r"] <= 0:
                err(fid, "descomposicion con parte no positiva: %s" % it)

    elif t == "tabla":
        n = b["n"]
        for it in items:
            if it["r"] != n * it["b"]:
                err(fid, "tabla del %d mal: %d x %d = %d" % (n, n, it["b"], it["r"]))
        if len(items) != 10:
            err(fid, "tabla del %d con %d filas (deberian ser 10)" % (n, len(items)))

    elif t == "problema":
        for it in items:
            if it["r"] < 0:
                err(fid, "problema con resultado negativo: %s" % it["texto"])
            nums = [int(x) for x in re.findall(r"\d+", it["texto"])]
            if len(nums) >= 2:
                a, bb = nums[0], nums[1]
                if it["r"] not in (a + bb, a - bb):
                    err(fid, "problema sin operacion coherente: '%s' -> %d" % (it["texto"], it["r"]))
            if not it["texto"].strip().endswith("?"):
                avisos.append("%s: problema sin pregunta final: %s" % (fid, it["texto"]))

    elif t == "unir":
        if len(b["izq"]) != len(b["der"]):
            err(fid, "unir con columnas de distinta longitud")
        if sorted(b["solucion"]) != list(range(len(b["izq"]))):
            err(fid, "unir con solucion invalida: %s" % b["solucion"])

    elif t == "emparejar":
        for it in items:
            if it["opciones"][it["correcta"]] != it["modelo"]:
                err(fid, "emparejar: la opcion correcta no coincide con el modelo")
            if len(set(it["opciones"])) != len(it["opciones"]):
                err(fid, "emparejar con opciones repetidas: %s" % it["opciones"])

    elif t == "rodear":
        for it in items:
            ops = it["opciones"]
            marcada = ops[it["correcta"]]
            if marcada not in (max(ops), min(ops)):
                err(fid, "rodear: la marcada no es ni el mayor ni el menor: %s" % ops)

    elif t == "vecinos":
        for it in items:
            if it["anterior"] != it["n"] - 1 or it["posterior"] != it["n"] + 1:
                err(fid, "vecinos mal para %d" % it["n"])
            if it["anterior"] < 0:
                err(fid, "vecino anterior negativo para %d" % it["n"])

    elif t == "monedas":
        for it in items:
            if it["un_euro"] + it["dos_euros"] * 2 != it["r"]:
                err(fid, "monedas mal: %s" % it)

    elif t == "colorear":
        for it in items:
            if it["colorear"] > it["total"]:
                err(fid, "colorear mas de los que hay: %d de %d" % (it["colorear"], it["total"]))

    elif t == "reloj":
        for it in items:
            if not (1 <= it["h"] <= 12) or not (0 <= it["m"] < 60):
                err(fid, "hora invalida: %s" % it)

    # ---------------- bloques de Lenguaje, Historia e Idiomas ----------------
    elif t == "silabas":
        for it in items:
            unido = "".join(it["silabas"])
            if unido != it["palabra"]:
                err(fid, "silabas no reconstruyen la palabra: %s -> %s"
                    % (it["palabra"], "-".join(it["silabas"])))
            if not it["silabas"]:
                err(fid, "palabra sin silabas: %s" % it["palabra"])

    elif t == "completar":
        for it in items:
            if it["antes"] + it["falta"] + it["despues"] != it["palabra"]:
                err(fid, "hueco mal recortado en %s" % it["palabra"])
            if len(it["falta"]) != 1:
                err(fid, "el hueco debe ser de una letra en %s" % it["palabra"])

    elif t == "clasificar":
        ncols = len(b["columnas"])
        if ncols < 2:
            err(fid, "clasificar con menos de dos columnas")
        for it in items:
            if not 0 <= it["columna"] < ncols:
                err(fid, "elemento en columna inexistente: %s" % it["contenido"])
        usadas = {it["columna"] for it in items}
        if len(usadas) < ncols:
            avisos.append("%s: alguna columna de clasificar queda vacia" % fid)

    elif t == "ordenar":
        ordenes = sorted(it["orden"] for it in items)
        if ordenes != list(range(1, len(items) + 1)):
            err(fid, "ordenar sin secuencia 1..n: %s" % ordenes)

    elif t == "lectura":
        if len(b.get("texto", "")) < 20:
            err(fid, "texto de lectura demasiado corto")
        for it in items:
            if not it["pregunta"].strip().endswith("?"):
                err(fid, "pregunta de lectura sin interrogante: %s" % it["pregunta"])
            if not str(it["r"]).strip():
                err(fid, "pregunta sin respuesta: %s" % it["pregunta"])

    elif t == "verdadero-falso":
        if not any(it["r"] for it in items) or all(it["r"] for it in items):
            avisos.append("%s: verdadero/falso con todas las respuestas iguales" % fid)
        for it in items:
            if not isinstance(it["r"], bool):
                err(fid, "verdadero/falso sin respuesta booleana")

    elif t == "frase":
        for it in items:
            if not str(it["r"]).strip():
                err(fid, "frase con hueco vacio")

    elif t == "vocabulario":
        for it in items:
            if not it["en"].strip() or not it["es"].strip():
                err(fid, "vocabulario incompleto: %s" % it)

    elif t == "colorear-ingles":
        for it in items:
            if not it["en"].strip():
                err(fid, "colorear-ingles sin palabra")

    elif t == "escritura":
        for it in items:
            if not it["palabra"].strip():
                err(fid, "escritura sin palabra")

    # 'unir' guarda las columnas en izq/der, 'tabla' su rejilla y 'dibujar' es
    # una zona en blanco; el resto sí debe traer items.
    SIN_ITEMS_OK = ("trazo", "formas", "concepto", "unir", "dibujar")
    if t not in SIN_ITEMS_OK and not items:
        err(fid, "bloque '%s' sin items" % t)


def main():
    archivos = sorted(glob.glob(os.path.join(RAIZ, "data", "fichas", "*.js")))
    if not archivos:
        raise SystemExit("No hay datos generados. Ejecuta antes: python tools/build.py")

    total = 0
    por_curso_max = {}

    for ruta in archivos:
        fichas = cargar(ruta)
        for f in fichas:
            total += 1
            if not f["bloques"]:
                err(f["id"], "ficha sin bloques")
            if len(f["titulo"]) < 3:
                err(f["id"], "titulo demasiado corto")
            for b in f["bloques"]:
                validar_bloque(f["id"], b)
                # Mayor operando visto en el curso, para comprobar la progresion
                for it in b.get("items", []):
                    for k in ("a", "b", "n", "total"):
                        v = it.get(k)
                        if isinstance(v, int):
                            por_curso_max[f["curso"]] = max(por_curso_max.get(f["curso"], 0), v)

    print("Fichas validadas: %d" % total)
    print()
    print("Progresion (mayor numero que aparece en cada curso):")
    anterior = 0
    for curso in sorted(por_curso_max):
        maximo = por_curso_max[curso]
        flecha = "OK" if maximo >= anterior else "!! RETROCEDE"
        print("  %d anos -> %4d   %s" % (curso, maximo, flecha))
        if maximo < anterior:
            errores.append("La dificultad retrocede en el curso de %d anos" % curso)
        anterior = maximo

    print()
    if avisos:
        print("Avisos (%d):" % len(avisos))
        for a in avisos[:10]:
            print("  - %s" % a)
        print()
    if errores:
        print("ERRORES (%d):" % len(errores))
        for e in errores[:40]:
            print("  - %s" % e)
        sys.exit(1)
    print("Sin errores. Todo el contenido es correcto.")


if __name__ == "__main__":
    main()
