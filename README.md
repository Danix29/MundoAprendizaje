# 🦉 Mundo Aprendizaje

**Mundo Aprendizaje** es una plataforma educativa interactiva para niñas y niños de **2 a 7 años**. Acompaña los primeros pasos lectores, matemáticos y creativos con juegos en el navegador, vídeos explicativos y cuadernos de fichas imprimibles.

## ✨ Qué hay

| Sección | Página | Acceso |
| --- | --- | --- |
| Landing y rincones | `index.html` | Gratis |
| Cuatro minijuegos con voz | `juegos.html` | Gratis |
| Vídeos explicativos por tema y curso | `videos.html` | En preparación |
| Catálogo de fichas | `descargas.html` | Gratis (muestras) |
| Visor e impresión de fichas | `fichas.html` | Muestras gratis |
| Packs de fichas en PDF | `tienda.html` | 1,99 € |

### Rincones de aprendizaje

* 🔢 **Matemáticas:** sumas, formas y números.
* 🔤 **Lenguaje:** abecedario, vocales y primeras palabras.
* 🦕 **Historia:** dinosaurios y Antiguo Egipto.
* 🌍 **Idiomas:** vocabulario básico en inglés (colores, animales).

### Cursos

Un tramo por curso escolar: **2 años** (aula de 2), **3 años** (Infantil 1º), **4 años** (Infantil 2º), **5 años** (Infantil 3º), **6 años** (1º Primaria) y **7 años** (2º Primaria).

### Minijuegos

| Juego | Rincón | Qué se practica |
| --- | --- | --- |
| Toca y Descubre | Matemáticas | Animales y números, con voz en `es-ES` |
| La Letra Perdida | Lenguaje | Asociar la letra inicial con el dibujo |
| Línea del Tiempo | Historia | Ordenar sucesos del más antiguo al más nuevo |
| Memory in English | Idiomas | Parejas de dibujo y palabra, con voz en `en-GB` |

Los cuatro escalan con el curso: el tablero de *Toca y Descubre* va de 6 casillas (2 años) a 18 (7 años), el memory de 3 a 6 parejas, etc.

## 📁 Estructura del proyecto

```text
mundo-aprendizaje/
├── index.html                  # Landing, rincones y juego destacado
├── juegos.html                 # Los cuatro minijuegos
├── videos.html                 # Catálogo de vídeos (placeholders)
├── descargas.html              # Catálogo de fichas, con filtros y paginación
├── fichas.html                 # Visor e impresión de cualquier cuaderno
├── tienda.html                 # Venta de packs + condiciones de compra
│
├── fichas_matematicas.html     # Cuaderno original (3 fichas, gratis)
├── fichas_imprimibles.html     # Cuaderno original (7 fichas, gratis)
│
├── assets/
│   ├── base.css                # Tokens (claro y oscuro), navegación, animaciones
│   ├── fichas.css              # Estilos de ficha + @media print (A4)
│   ├── site.js                 # Carga perezosa, utilidades y modo oscuro
│   ├── render-ficha.js         # Convierte una ficha JSON en HTML imprimible
│   ├── juegos.js               # Motor de los cuatro minijuegos
│   ├── carrusel.js             # Carrusel accesible (scroll-snap + teclado)
│   └── onboarding.js           # Presentación de bienvenida (una sola vez)
│
├── data/                       # GENERADO — no editar a mano
│   ├── catalogo.js             # Índice ligero de todas las fichas
│   ├── packs.js                # Catálogo de packs y precios
│   ├── videos.js               # Catálogo de vídeos
│   ├── testimonios.js          # ⚠️ TESTIMONIOS DE EJEMPLO, no reales
│   └── fichas/
│       └── <tema>-<curso>.js   # 24 archivos: 4 temas × 6 cursos
│
├── tools/                      # Generador del contenido
│   ├── generar_fichas.py       # Tipos de ejercicio y utilidades
│   ├── curriculo_matematicas.py# Las 20 fichas de cada curso
│   ├── build.py                # Ensambla data/ y dist/
│   ├── curriculo_lenguaje.py   # Ídem para Lenguaje
│   ├── curriculo_historia.py   # Ídem para Historia
│   ├── curriculo_idiomas.py    # Ídem para Idiomas
│   ├── bloques_texto.py        # Tipos de ejercicio de texto (sílabas, lectura…)
│   ├── extras.py               # Genera packs.js y videos.js
│   ├── validar.py              # Comprueba que el contenido es correcto
│   └── auditar.py              # Informe de completitud tema × curso
│
├── dist/                       # GENERADO, no se publica (.gitignore)
│   └── fichas/                 # Contenido COMPLETO, para producir los PDF
│
└── Cuadernos en PDF (Matemáticas, Lenguaje, Historia, Idiomas)
```

## 🧱 Cómo funciona el catálogo de fichas

No hay 480 archivos HTML escritos a mano. El sistema es:

1. **Currículo declarado** (`tools/curriculo_<tema>.py`): 20 entradas por curso, cada una con título, objetivo pedagógico y la lista de bloques de ejercicio que la componen.
2. **Generador** (`tools/generar_fichas.py`): construye cada bloque. **Las operaciones y sus resultados se calculan en Python**, nunca se escriben a mano, así que es imposible publicar una ficha con una suma mal.
3. **Datos** (`data/fichas/*.js`): un archivo por tema y curso, cargado solo cuando hace falta.
4. **Renderizador** (`assets/render-ficha.js`): pinta cualquier ficha a partir de sus datos, con **29 tipos de bloque** (contar, trazo, operaciones, comparar, series, unir, problemas, formas, reloj, descomposición, tablas de multiplicar, sílabas, lectura comprensiva, verdadero/falso, clasificar, ordenar, vocabulario en inglés…).

### Regenerar el contenido

```bash
python tools/build.py && python tools/extras.py && python tools/validar.py && python tools/auditar.py
```

El generador es **determinista**: la misma ficha produce siempre el mismo contenido, así que dos ejecuciones dan archivos idénticos y los diffs son limpios.

### Por qué `.js` y no `.json`

`fetch()` de un archivo local está bloqueado por CORS en `file://`. Si los datos fuesen `.json`, el sitio dejaría de funcionar al abrirlo con doble clic. Sirviéndolos como `.js` que asignan a una variable global y cargándolos con `<script>`, funciona igual en `file://` y en un servidor.

### Público vs. vendible

`data/fichas/*.js` contiene **solo el contenido de las fichas gratuitas**. Las de pago viajan con su título y objetivo, pero sin ejercicios: publicarlos sería regalarlos, porque cualquiera los lee con las herramientas de desarrollo. El contenido completo vive en `dist/`, que no se publica y sirve para generar los PDF que se venden.

## 💻 Cómo previsualizarlo en local

**Opción rápida:** doble clic en `index.html`. Funciona todo, incluida la carga de fichas.

**Opción recomendada** (reproduce cómo se sirve en GitHub Pages):

```bash
python -m http.server 5180
```

Después abre <http://localhost:5180>. No hay proceso de compilación de front-end ni dependencias que instalar; Python solo hace falta para regenerar el contenido.

## 🌙 Modo claro y oscuro

El interruptor sol/luna vive en la cabecera de todas las páginas y lo inyecta `assets/site.js`. La preferencia se guarda en `localStorage`; si no hay ninguna guardada se sigue a `prefers-color-scheme`, y los cambios del sistema se aplican en caliente mientras el usuario no haya elegido a mano.

El tema oscuro **no es una inversión**: es una paleta propia de marrón carbón cálido con versiones nocturnas de cada pastel, para que siga sintiéndose de cuento y no de panel de control. Todos los pares de texto y fondo superan el contraste AA (mínimo medido: 5,87:1).

**Al imprimir se fuerza siempre papel blanco y tinta oscura**, esté como esté la pantalla: el bloque `@media print` de `assets/fichas.css` redefine la paleta con `:root, :root[data-theme="dark"]`, que gana en especificidad al tema oscuro. Imprimir fondos carbón gastaría un cartucho por cuaderno.

## 🖨️ Notas de impresión

* Las fichas están maquetadas para **A4 vertical** con márgenes de 12 mm, una ficha por página.
* Activa **«Gráficos de fondo»** en el diálogo de impresión para que salgan los colores pastel.
* Cada ficha tiene un botón **«Imprimir solo esta»** para sacar una sola hoja.
* El tamaño de letra se adapta al curso: los más pequeños reciben todo más grande.

## 🚀 Tecnologías

HTML5 semántico, CSS3 con variables nativas y `@media print`, y JavaScript Vanilla ES6+. **Sin frameworks ni dependencias externas**; la única petición a terceros son las tipografías de Google Fonts, que degradan a fuentes del sistema si no hay conexión.

Accesibilidad: etiquetas ARIA, foco visible, navegación por teclado en pestañas y juegos, objetivos táctiles de 44 px o más, `prefers-reduced-motion` y responsive real.

## ⏳ Estado y pendientes

**Catálogo completo: 480 fichas** — 4 temas × 6 cursos × 20, con 603 bloques de ejercicio, 1.834 ítems y 29 tipos de ejercicio distintos. Todo validado por `tools/validar.py`.

| Tema | 2 años | 3 años | 4 años | 5 años | 6 años | 7 años | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Matemáticas | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Lenguaje | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Historia | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Idiomas | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| **Total** | **80** | **80** | **80** | **80** | **80** | **80** | **480** |

Comprueba la tabla en cualquier momento con `python tools/auditar.py`.

**⚠️ Los testimonios de `data/testimonios.js` son inventados.** Están ahí para diseñar la sección; publicarlos como reseñas reales sería publicidad engañosa. Sustitúyelos por testimonios reales con permiso escrito, o borra la sección de `index.html`.

**Pendiente de configuración:**

* **Pasarela de pago.** Crear la cuenta de Payhip, dar de alta los productos y sustituir `payhipUsuario` y cada `payhipId` en `data/packs.js`. Mientras pongan `PENDIENTE`, los botones de compra salen desactivados a propósito. Después, descomentar el `<script>` de Payhip al final de `tienda.html`.
* **Revisión legal.** El apartado «Condiciones de compra» de `tienda.html` es un **borrador** y debe revisarlo un profesional antes de publicar, además de añadir los datos fiscales de contacto.
* **Vídeos.** Rellenar `url` y `duracion` en `data/videos.js` (`tools/extras.py` para regenerarlo). El diseño no se toca: si hay URL se monta el reproductor, y si no, el placeholder.
* **Testimonios.** Sustituir `data/testimonios.js` por reseñas reales con permiso, o eliminar la sección.
