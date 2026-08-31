# -*- coding: utf-8 -*-
"""
Generador del catalogo de fichas de Mundo Aprendizaje.

Produce, a partir de un curriculo declarado por curso:
  data/fichas/<tema>-<curso>.js   contenido completo de las 20 fichas
  data/catalogo.js               indice ligero (sin ejercicios) para navegar

Las operaciones y sus resultados se CALCULAN aqui, nunca se escriben a mano:
asi es imposible publicar una ficha con una suma mal.

Uso:  python tools/generar_fichas.py
"""

import io
import json
import os
import random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Un tramo por curso escolar. El aula de 2 anos es opcional en muchos centros,
# pero aqui se incluye como primer tramo.
CURSOS = {
    2: {"etiqueta": "2 años", "etapa": "Aula de 2 años"},
    3: {"etiqueta": "3 años", "etapa": "Infantil 1º"},
    4: {"etiqueta": "4 años", "etapa": "Infantil 2º"},
    5: {"etiqueta": "5 años", "etapa": "Infantil 3º"},
    6: {"etiqueta": "6 años", "etapa": "1º Primaria"},
    7: {"etiqueta": "7 años", "etapa": "2º Primaria"},
}

TEMAS = {
    "matematicas": {"nombre": "Matemáticas", "icono": "🔢", "color": "peach"},
    "lenguaje":    {"nombre": "Lenguaje",    "icono": "🔤", "color": "sky"},
    "historia":    {"nombre": "Historia",    "icono": "🦕", "color": "mint"},
    "idiomas":     {"nombre": "Idiomas",     "icono": "🌍", "color": "lavender"},
}

FRUTAS   = ["🍎", "🍌", "🍓", "🍐", "🍇", "🍊", "🍉", "🍋"]
ANIMALES = ["🐶", "🐱", "🐰", "🐸", "🐥", "🐢", "🐝", "🐞"]
OBJETOS  = ["⭐", "🌸", "🍀", "🎈", "🚗", "⚽", "🎁", "🌙"]
TODOS    = FRUTAS + ANIMALES + OBJETOS


# ---------------------------------------------------------------- utilidades
def rng(fid):
    """Aleatoriedad reproducible: la misma ficha da siempre el mismo contenido."""
    return random.Random("mundo-aprendizaje::" + fid)


def muestra(r, pool, n):
    return r.sample(pool, n)


# ------------------------------------------------------------ tipos de bloque
def b_contar(r, cuantos=3, maximo=5, pool=None):
    pool = pool or TODOS
    emojis = muestra(r, pool, cuantos)
    return {
        "tipo": "contar",
        "enunciado": "Cuenta y escribe cuántos hay en cada fila.",
        "items": [{"emoji": e, "n": r.randint(1, maximo)} for e in emojis],
    }


def b_trazo(r, glifos, repeticiones=4, enunciado=None):
    return {
        "tipo": "trazo",
        "enunciado": enunciado or "Repasa con tu lápiz siguiendo las flechas.",
        "items": [{"glifo": g, "repeticiones": repeticiones} for g in glifos],
    }


def b_operaciones(r, op, cuantas, maximo, formato="horizontal", llevando=None, enunciado=None):
    items = []
    intentos = 0
    while len(items) < cuantas and intentos < 400:
        intentos += 1
        if op == "+":
            a = r.randint(1, maximo)
            b = r.randint(1, maximo)
            if a + b > maximo:
                continue
            if llevando is True and (a % 10) + (b % 10) < 10:
                continue
            if llevando is False and (a % 10) + (b % 10) >= 10:
                continue
            items.append({"a": a, "op": "+", "b": b, "r": a + b})
        elif op == "-":
            a = r.randint(2, maximo)
            b = r.randint(1, a)
            if llevando is True and (a % 10) >= (b % 10):
                continue
            if llevando is False and (a % 10) < (b % 10):
                continue
            items.append({"a": a, "op": "-", "b": b, "r": a - b})
        elif op == "x":
            a = r.randint(1, maximo)
            b = r.randint(1, 10)
            items.append({"a": a, "op": "×", "b": b, "r": a * b})
    signo = {"+": "sumas", "-": "restas", "x": "multiplicaciones"}[op]
    return {
        "tipo": "operaciones",
        "enunciado": enunciado or f"Resuelve estas {signo}.",
        "formato": formato,
        "items": items,
    }


def b_comparar(r, cuantas=6, maximo=10, con_dibujo=False):
    items = []
    for _ in range(cuantas):
        a = r.randint(1, maximo)
        b = r.randint(1, maximo)
        items.append({"a": a, "b": b, "r": "=" if a == b else ("<" if a < b else ">")})
    return {
        "tipo": "comparar",
        "enunciado": "Escribe el signo que falta: mayor (>), menor (<) o igual (=).",
        "conDibujo": con_dibujo,
        "items": items,
    }


def b_serie(r, cuantas=3, paso=1, inicio_max=10, longitud=6):
    items = []
    for _ in range(cuantas):
        ini = r.randrange(0, inicio_max + 1, max(1, paso)) or paso
        valores = [ini + paso * i for i in range(longitud)]
        huecos = sorted(r.sample(range(1, longitud), 2))
        items.append({"valores": valores, "huecos": huecos, "paso": paso})
    return {
        "tipo": "serie",
        "enunciado": f"Completa la serie contando de {paso} en {paso}.",
        "items": items,
    }


def b_unir(r, pares, enunciado=None):
    """pares: lista de (izquierda, derecha). La columna derecha se baraja."""
    der = [p[1] for p in pares]
    orden = list(range(len(pares)))
    r.shuffle(orden)
    return {
        "tipo": "unir",
        "enunciado": enunciado or "Une con una línea cada pareja.",
        "izq": [p[0] for p in pares],
        "der": [der[i] for i in orden],
        "solucion": orden,
    }


def b_colorear(r, cuantas=3, maximo=8, pool=None):
    pool = pool or OBJETOS
    emojis = muestra(r, pool, cuantas)
    items = []
    for e in emojis:
        total = r.randint(4, maximo)
        items.append({"emoji": e, "total": total, "colorear": r.randint(1, total)})
    return {
        "tipo": "colorear",
        "enunciado": "Colorea solo la cantidad que se indica en cada fila.",
        "items": items,
    }


PROBLEMAS_SUMA = [
    ("En el parque hay {a} patos y llegan {b} más. ¿Cuántos patos hay ahora?", "patos"),
    ("Tengo {a} cromos y mi hermana me regala {b}. ¿Cuántos cromos tengo?", "cromos"),
    ("En un árbol hay {a} manzanas rojas y {b} verdes. ¿Cuántas manzanas hay?", "manzanas"),
    ("Ana lee {a} páginas por la mañana y {b} por la tarde. ¿Cuántas lee en total?", "páginas"),
    ("Hay {a} niños jugando y llegan {b} más. ¿Cuántos niños juegan ahora?", "niños"),
]

PROBLEMAS_RESTA = [
    ("Tenía {a} globos y se me han volado {b}. ¿Cuántos globos me quedan?", "globos"),
    ("En la caja había {a} lápices y he cogido {b}. ¿Cuántos quedan en la caja?", "lápices"),
    ("Hay {a} pájaros en la rama y se van {b}. ¿Cuántos pájaros quedan?", "pájaros"),
    ("Compré {a} caramelos y me he comido {b}. ¿Cuántos me quedan?", "caramelos"),
    ("En el plato había {a} galletas y nos hemos comido {b}. ¿Cuántas quedan?", "galletas"),
]


def b_problema(r, op="+", cuantos=2, maximo=10):
    plantillas = PROBLEMAS_SUMA if op == "+" else PROBLEMAS_RESTA
    elegidas = muestra(r, plantillas, min(cuantos, len(plantillas)))
    items = []
    for texto, unidad in elegidas:
        if op == "+":
            a = r.randint(2, max(2, maximo // 2))
            b = r.randint(1, max(1, maximo - a))
            res = a + b
        else:
            a = r.randint(3, maximo)
            b = r.randint(1, a - 1)
            res = a - b
        items.append({"texto": texto.format(a=a, b=b), "r": res, "unidad": unidad})
    return {
        "tipo": "problema",
        "enunciado": "Lee con atención, haz la operación y escribe la solución.",
        "items": items,
    }


FORMAS = [
    ("circulo", "Círculo"), ("cuadrado", "Cuadrado"),
    ("triangulo", "Triángulo"), ("rectangulo", "Rectángulo"),
    ("ovalo", "Óvalo"), ("rombo", "Rombo"),
]


def b_formas(r, cuales=None, enunciado=None):
    cuales = cuales or ["circulo", "cuadrado", "triangulo", "rectangulo"]
    nombres = dict(FORMAS)
    return {
        "tipo": "formas",
        "enunciado": enunciado or "Repasa las líneas de puntos y lee el nombre de cada forma.",
        "items": [{"forma": f, "nombre": nombres[f]} for f in cuales],
    }


def b_reloj(r, cuantos=4, precision="en punto"):
    minutos = {"en punto": [0], "y media": [0, 30], "y cuarto": [0, 15, 30, 45]}[precision]
    items = []
    for _ in range(cuantos):
        items.append({"h": r.randint(1, 12), "m": r.choice(minutos)})
    return {
        "tipo": "reloj",
        "enunciado": "Observa cada reloj y escribe la hora que marca.",
        "items": items,
    }


def b_descomponer(r, total=10, cuantos=4):
    partes = muestra(r, list(range(1, total)), min(cuantos, total - 1))
    return {
        "tipo": "descomponer",
        "enunciado": f"Completa: ¿cuánto falta para llegar a {total}?",
        "total": total,
        "items": [{"parte": p, "r": total - p} for p in sorted(partes)],
    }


def b_rodear(r, cuantos=4, maximo=20, criterio="mayor"):
    items = []
    for _ in range(cuantos):
        ops = muestra(r, list(range(1, maximo + 1)), 3)
        correcta = ops.index(max(ops) if criterio == "mayor" else min(ops))
        items.append({"opciones": ops, "correcta": correcta})
    return {
        "tipo": "rodear",
        "enunciado": f"Rodea en cada grupo el número {criterio}.",
        "items": items,
    }


def b_emparejar(r, cuantos=3, pool=None):
    pool = pool or TODOS
    items = []
    usados = muestra(r, pool, cuantos * 3)
    for i in range(cuantos):
        modelo = usados[i * 3]
        distractores = usados[i * 3 + 1: i * 3 + 3]
        opciones = [modelo] + distractores
        orden = list(range(3))
        r.shuffle(orden)
        opciones = [opciones[j] for j in orden]
        items.append({"modelo": modelo, "opciones": opciones, "correcta": opciones.index(modelo)})
    return {
        "tipo": "emparejar",
        "enunciado": "Rodea en cada fila el dibujo igual que el del recuadro.",
        "items": items,
    }


def b_vecinos(r, cuantos=5, maximo=20, pide="ambos"):
    ns = muestra(r, list(range(2, maximo)), cuantos)
    return {
        "tipo": "vecinos",
        "enunciado": {
            "ambos": "Escribe el número anterior y el posterior.",
            "anterior": "Escribe el número anterior.",
            "posterior": "Escribe el número posterior.",
        }[pide],
        "pide": pide,
        "items": [{"n": n, "anterior": n - 1, "posterior": n + 1} for n in sorted(ns)],
    }


def b_tabla(r, n):
    huecos = sorted(r.sample(range(1, 11), 5))
    return {
        "tipo": "tabla",
        "enunciado": f"Completa la tabla del {n}.",
        "n": n,
        "huecos": huecos,
        "items": [{"b": i, "r": n * i} for i in range(1, 11)],
    }


def b_concepto(r, pares, enunciado):
    """Conceptos basicos por oposicion: grande/pequeno, lleno/vacio..."""
    return {
        "tipo": "concepto",
        "enunciado": enunciado,
        "items": [{"emoji": e, "criterio": c} for e, c in pares],
    }


def b_tantos_como(r, cuantos=3, maximo=6):
    emojis = muestra(r, TODOS, cuantos)
    return {
        "tipo": "tantos-como",
        "enunciado": "Dibuja en el recuadro tantas cosas como hay en la fila.",
        "items": [{"emoji": e, "n": r.randint(2, maximo)} for e in emojis],
    }


def b_dobles(r, cuantos=5, maximo=10):
    ns = muestra(r, list(range(1, maximo + 1)), cuantos)
    return {
        "tipo": "operaciones",
        "enunciado": "Calcula el doble de cada número.",
        "formato": "horizontal",
        "items": [{"a": n, "op": "+", "b": n, "r": n * 2} for n in sorted(ns)],
    }


def b_monedas(r, cuantos=4):
    combos = []
    for _ in range(cuantos):
        n1 = r.randint(1, 3)   # monedas de 1 €
        n2 = r.randint(1, 3)   # monedas de 2 €
        combos.append({"un_euro": n1, "dos_euros": n2, "r": n1 + n2 * 2})
    return {
        "tipo": "monedas",
        "enunciado": "Cuenta el dinero y escribe cuántos euros hay en total.",
        "items": combos,
    }
