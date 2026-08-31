# -*- coding: utf-8 -*-
"""
Genera los PDF que se venden, uno por tema y curso.

Imprime cada cuaderno con Chrome en modo headless desde
`fichas.html?fuente=dist`, que es la unica vista que renderiza las 20 fichas
completas. Requiere que el servidor local este levantado.

    python -m http.server 5180        (en otra terminal, desde la raiz)
    python tools/generar_pdf.py

Salida en dist/pdf/. Como dist/ esta en .gitignore, los PDF no se publican:
son el producto que se entrega tras la compra.
"""

import io
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import generar_fichas as G  # noqa: E402

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SERVIDOR = "http://localhost:5180"
SALIDA = os.path.join(RAIZ, "dist", "pdf")


def nombre_archivo(tema, curso):
    return "Mundo Aprendizaje - %s - %s.pdf" % (
        G.TEMAS[tema]["nombre"], G.CURSOS[curso]["etiqueta"])


def imprimir(tema, curso, destino, presupuesto):
    url = "%s/fichas.html?fuente=dist#/%s/%d" % (SERVIDOR, tema, curso)
    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        "--virtual-time-budget=%d" % presupuesto,
        "--print-to-pdf=" + destino,
        url,
    ], capture_output=True, timeout=240)


def revisar(ruta):
    """
    Devuelve None si el PDF esta bien, o el motivo del fallo.

    Chrome a veces imprime antes de que la pagina termine de pintar y produce
    un PDF con el numero correcto de paginas pero completamente en blanco.
    Pesa unos pocos KB y no tiene texto: se detectan las dos cosas, porque un
    cuaderno vacio vendido a un cliente seria el peor fallo posible.
    """
    from pypdf import PdfReader
    if not os.path.exists(ruta):
        return "no se creo el archivo"
    kb = os.path.getsize(ruta) / 1024.0
    if kb < 200:
        return "pesa solo %.0f KB (parece vacio)" % kb
    r = PdfReader(ruta)
    if len(r.pages) < 20:
        return "solo %d paginas" % len(r.pages)
    texto = (r.pages[0].extract_text() or "").strip()
    if len(texto) < 40:
        return "la primera pagina no tiene texto"
    return None


def generar(tema, curso, intentos=3):
    destino = os.path.join(SALIDA, nombre_archivo(tema, curso))
    presupuesto = 15000
    for intento in range(1, intentos + 1):
        imprimir(tema, curso, destino, presupuesto)
        fallo = revisar(destino)
        if not fallo:
            return destino, None
        # Si fallo por prisa, se le da mas tiempo a la pagina en el reintento.
        presupuesto += 10000
    return destino, fallo


def main():
    os.makedirs(SALIDA, exist_ok=True)
    if not os.path.exists(CHROME):
        raise SystemExit("No encuentro Chrome en %s" % CHROME)

    from pypdf import PdfReader
    total_paginas = 0
    filas = []
    for tema in G.TEMAS:
        for curso in sorted(G.CURSOS):
            t0 = time.time()
            ruta, fallo = generar(tema, curso)
            if fallo:
                print("  FALLO  %-12s %d anos -> %s" % (tema, curso, fallo))
                sys.stdout.flush()
                continue
            paginas = len(PdfReader(ruta).pages)
            kb = os.path.getsize(ruta) / 1024.0
            total_paginas += paginas
            filas.append((tema, curso, paginas, kb))
            print("  %-12s %d anos -> %3d pag  %6.0f KB  (%.0fs)"
                  % (tema, curso, paginas, kb, time.time() - t0))
            sys.stdout.flush()

    print()
    print("  %d PDF generados, %d paginas en total" % (len(filas), total_paginas))
    print("  peso total: %.1f MB" % (sum(f[3] for f in filas) / 1024.0))


if __name__ == "__main__":
    main()
