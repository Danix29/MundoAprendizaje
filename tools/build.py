# -*- coding: utf-8 -*-
"""
Ensambla el catalogo y escribe los datos que consume el sitio.

Salida:
  data/catalogo.js            indice ligero (sin ejercicios) -> navegacion rapida
  data/fichas/<tema>-<n>.js   contenido completo de las 20 fichas de ese curso

Se emite JavaScript, no JSON, a proposito: fetch() de un .json local esta
bloqueado por CORS en file://, asi que el sitio dejaria de funcionar al abrirlo
con doble clic. Un <script> inyectado funciona en file:// y en servidor.

Uso:  python tools/build.py
"""

import io
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

import generar_fichas as G           # noqa: E402
import curriculo_matematicas         # noqa: E402
import curriculo_lenguaje            # noqa: E402
import curriculo_historia            # noqa: E402
import curriculo_idiomas             # noqa: E402

# Para anadir un tema basta con crear su modulo de curriculo e incluirlo aqui:
# el resto del sitio (catalogo, tienda, visor) se adapta solo.
CURRICULOS = {
    "matematicas": curriculo_matematicas.CURRICULO,
    "lenguaje": curriculo_lenguaje.CURRICULO,
    "historia": curriculo_historia.CURRICULO,
    "idiomas": curriculo_idiomas.CURRICULO,
}


def construir_ficha(tema, curso, orden, titulo, objetivo, constructor):
    fid = "%s-c%d-%02d" % (tema[:3], curso, orden)
    r = G.rng(fid)
    return {
        "id": fid,
        "tema": tema,
        "curso": curso,
        "orden": orden,
        "titulo": titulo,
        "objetivo": objetivo,
        # La primera ficha de cada curso es la muestra gratuita: asi una familia
        # ve el nivel exacto del curso de su hija o hijo, no el de otro.
        "gratis": orden == 1,
        "bloques": constructor(r),
    }


def js(nombre_global, clave, datos):
    cuerpo = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    if clave is None:
        return "window.%s = %s;\n" % (nombre_global, cuerpo)
    return ("window.%s = window.%s || {};\n"
            "window.%s[%s] = %s;\n" % (nombre_global, nombre_global,
                                       nombre_global, json.dumps(clave), cuerpo))


def escribir(ruta_rel, contenido):
    ruta = os.path.join(RAIZ, ruta_rel)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with io.open(ruta, "w", encoding="utf-8") as fh:
        fh.write(contenido)
    return os.path.getsize(ruta)


def publico(ficha):
    """
    Version que se sirve al navegador.

    El contenido completo solo viaja si la ficha es gratuita. Publicar los
    ejercicios de las fichas de pago en un .js seria regalarlas: cualquiera
    las lee con las herramientas de desarrollo. Lo que se vende se entrega
    como PDF tras la compra, generado desde dist/.
    """
    if ficha["gratis"]:
        return ficha
    recortada = dict(ficha)
    recortada["bloques"] = []
    recortada["bloqueado"] = True
    # Se conserva de que va la ficha, para poder ensenarla en el catalogo.
    recortada["resumen"] = [b["tipo"] for b in ficha["bloques"]]
    return recortada


def main():
    indice = []
    total_bloques = 0
    total_items = 0

    for tema, por_curso in CURRICULOS.items():
        for curso, entradas in sorted(por_curso.items()):
            if len(entradas) != 20:
                raise SystemExit(
                    "%s curso %d tiene %d fichas, se esperaban 20"
                    % (tema, curso, len(entradas))
                )
            fichas = []
            for i, (titulo, objetivo, constructor) in enumerate(entradas, start=1):
                f = construir_ficha(tema, curso, i, titulo, objetivo, constructor)
                fichas.append(f)
                total_bloques += len(f["bloques"])
                total_items += sum(len(b.get("items", [])) for b in f["bloques"])
                indice.append({
                    "id": f["id"], "tema": tema, "curso": curso, "orden": i,
                    "titulo": titulo, "objetivo": objetivo, "gratis": f["gratis"],
                    "nBloques": len(f["bloques"]),
                    "tipos": sorted({b["tipo"] for b in f["bloques"]}),
                })
            clave = "%s-%d" % (tema, curso)

            # Publico: solo las gratuitas llevan ejercicios.
            tam = escribir("data/fichas/%s.js" % clave,
                           js("MA_FICHAS", clave, [publico(f) for f in fichas]))
            # Privado: todo, para generar los PDF que se venden. No se publica.
            escribir("dist/fichas/%s.js" % clave, js("MA_FICHAS", clave, fichas))

            print("  %-22s %2d fichas (%d gratis)  publico %5.1f KB"
                  % (clave + ".js", len(fichas),
                     sum(1 for f in fichas if f["gratis"]), tam / 1024))

    catalogo = {
        "temas": G.TEMAS,
        "cursos": {str(k): v for k, v in G.CURSOS.items()},
        "temasGenerados": sorted(CURRICULOS.keys()),
        "fichas": indice,
    }
    tam = escribir("data/catalogo.js", js("MA_CATALOGO", None, catalogo))

    print()
    print("  data/catalogo.js   %d fichas indexadas  %.1f KB" % (len(indice), tam / 1024))
    print("  %d bloques de ejercicio, %d items en total" % (total_bloques, total_items))
    print("  gratuitas: %d   premium: %d"
          % (sum(1 for f in indice if f["gratis"]), sum(1 for f in indice if not f["gratis"])))


if __name__ == "__main__":
    main()
