# 🦉 Mundo Aprendizaje

Plataforma educativa para niñas y niños de **2 a 7 años**: juegos con voz en el navegador, vídeos explicativos y **480 fichas imprimibles** organizadas por tema y curso.

Sitio estático, sin frameworks ni compilación de front-end. Se abre con doble clic en `index.html`.

---

## ⚠️ Antes de publicar

Tres cosas sin resolver. Ninguna impide desarrollar, pero **las tres bloquean la publicación**.

| Bloqueo | Dónde | Qué hay que hacer |
| --- | --- | --- |
| **Testimonios inventados** | `data/testimonios.js` | Las seis reseñas son ficticias, escritas para poder diseñar la sección. Publicarlas como opiniones reales sería publicidad engañosa. Sustitúyelas por testimonios reales con permiso por escrito, o borra la sección de `index.html`. Mientras `simulados: true`, la web muestra un aviso visible. |
| **Pasarela de pago sin conectar** | `data/packs.js` | Faltan el usuario y los IDs de producto de Payhip. Mientras valgan `PENDIENTE-…`, los botones de compra salen desactivados a propósito: es preferible un botón inerte a un enlace de compra roto. Al rellenarlos, descomenta el `<script>` de Payhip al final de `tienda.html`. |
| **Aviso legal sin revisar** | `tienda.html#legal` | «Condiciones de compra» es un borrador de trabajo, no un texto validado. Debe revisarlo un profesional, y hay que añadir los datos fiscales de contacto (nombre o razón social, NIF, domicilio, correo). |

---

## 🚀 Puesta en marcha

**Opción rápida.** Doble clic en `index.html`. Funciona todo, fichas incluidas.

**Opción recomendada**, que reproduce cómo se sirve en GitHub Pages:

```bash
python -m http.server 5180
```

Y abrir <http://localhost:5180>. Vale cualquier servidor estático (`npx serve`, `php -S localhost:5180`, la extensión Live Server de VS Code). No hay dependencias que instalar; Python solo hace falta para regenerar el contenido de las fichas.

---

## 📚 Qué incluye

| Página | Qué es | Acceso |
| --- | --- | --- |
| `index.html` | Landing, rincones, juego destacado, carrusel de packs y testimonios | Gratis |
| `juegos.html` | Los cuatro minijuegos con voz | Gratis |
| `videos.html` | Catálogo de vídeos por tema y curso | En preparación |
| `descargas.html` | Catálogo de fichas con filtros y paginación | Gratis |
| `fichas.html` | Visor e impresión de cualquier cuaderno | Muestras gratis |
| `tienda.html` | Venta de packs y condiciones de compra | 1,99 € |
| `fichas_matematicas.html` · `fichas_imprimibles.html` | Los diez cuadernos originales del proyecto, escritos a mano | Gratis |

### Rincones y cursos

Cuatro rincones — 🔢 **Matemáticas**, 🔤 **Lenguaje**, 🦕 **Historia**, 🌍 **Idiomas** — por seis tramos, uno por curso escolar:

| 2 años | 3 años | 4 años | 5 años | 6 años | 7 años |
| --- | --- | --- | --- | --- | --- |
| Aula de 2 | Infantil 1º | Infantil 2º | Infantil 3º | 1º Primaria | 2º Primaria |

### Minijuegos

| Juego | Rincón | Qué se practica |
| --- | --- | --- |
| Toca y Descubre | Matemáticas | Animales y números, con voz en `es-ES` |
| La Letra Perdida | Lenguaje | Asociar la letra inicial con el dibujo |
| Línea del Tiempo | Historia | Ordenar sucesos del más antiguo al más nuevo |
| Memory in English | Idiomas | Parejas de dibujo y palabra, con voz en `en-GB` |

Los cuatro escalan con el curso: el tablero de *Toca y Descubre* va de 6 casillas (2 años) a 18 (7 años), el memory de 3 a 6 parejas y las opciones de La Letra Perdida de 2 a 4.

La Línea del Tiempo se reordena con botones ◀ ▶, no arrastrando: arrastrar sería inaccesible por teclado y difícil para un peque de tres años.

---

## 🗂️ El catálogo de fichas

**480 fichas** — 4 temas × 6 cursos × 20 —, con 603 bloques de ejercicio, 1.838 ítems y 29 tipos de ejercicio distintos.

| Tema | 2 años | 3 años | 4 años | 5 años | 6 años | 7 años | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Matemáticas | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Lenguaje | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Historia | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| Idiomas | 20 | 20 | 20 | 20 | 20 | 20 | 120 |
| **Total** | **80** | **80** | **80** | **80** | **80** | **80** | **480** |

Dentro de cada tema y curso las fichas van de menos a más: la 1 es la más sencilla y la 20 la más completa. Entre cursos también: Matemáticas pasa de «grande y pequeño» (2 años) a las tablas de multiplicar y las sumas llevando (7 años); Lenguaje, del trazo vertical a la comprensión lectora y las tildes.

La primera ficha de **cada tema y cada curso** es una muestra gratuita: 24 en total. Así una familia ve el nivel exacto del curso de su hija o hijo antes de pagar, y no el de otro.

### Cómo está construido

No hay 480 archivos escritos a mano. El contenido se declara y se genera:

1. **El currículo** (`tools/curriculo_<tema>.py`) declara las 20 fichas de cada curso: título, objetivo pedagógico y los bloques de ejercicio que la componen.
2. **El generador** (`tools/generar_fichas.py` y `tools/bloques_texto.py`) construye cada bloque. **Las operaciones y sus resultados se calculan en Python**, nunca se escriben a mano, así que es imposible publicar una ficha con una suma mal. Lo mismo con las sílabas, que se separan con un algoritmo.
3. **Los datos** (`data/fichas/<tema>-<curso>.js`) se cargan solo al abrir ese cuaderno, unos 4 KB cada uno.
4. **El renderizador** (`assets/render-ficha.js`) pinta cualquier ficha a partir de sus datos, con 29 tipos de bloque: contar, trazo, operaciones, comparar, series, unir, problemas, formas, reloj, descomposición, tablas de multiplicar, sílabas, lectura comprensiva, verdadero/falso, clasificar, ordenar, completar, vocabulario en inglés, zonas de dibujo…

El generador es **determinista**: la misma ficha produce siempre el mismo contenido, así que dos ejecuciones dan archivos idénticos y los diffs quedan limpios.

---

## 🛠️ Desarrollo

### Regenerar y comprobar el contenido

```bash
python tools/build.py && python tools/extras.py && python tools/validar.py && python tools/auditar.py
```

| Script | Qué hace |
| --- | --- |
| `build.py` | Genera `data/catalogo.js`, `data/fichas/*.js` y `dist/fichas/*.js` |
| `extras.py` | Genera `data/packs.js` y `data/videos.js` |
| `validar.py` | Comprueba que el contenido es correcto |
| `auditar.py` | Informe de completitud tema × curso y detección de fichas vacías |

`validar.py` no es decorativo: comprueba que cada operación cuadra, que las sílabas reconstruyen la palabra, que ningún ejercicio de ordenar se salta un número y que los verdadero/falso no tienen todas las respuestas iguales.

### Qué se genera y qué se edita a mano

```text
data/
├── catalogo.js       GENERADO   build.py
├── fichas/*.js       GENERADO   build.py
├── packs.js          GENERADO   extras.py
├── videos.js         GENERADO   extras.py
└── testimonios.js    A MANO     ningún script lo toca
```

Cuidado con `packs.js` y `videos.js`: **`extras.py` los sobrescribe**. Si rellenas ahí los IDs de Payhip o las URL de los vídeos y luego regeneras, los pierdes. Para que sean permanentes, ponlos en `tools/extras.py`.

### Añadir un tema, un curso o un tipo de ejercicio

* **Tema nuevo:** crea `tools/curriculo_<tema>.py` con `CURRICULO = {curso: [...20 entradas...]}`, añádelo a `TEMAS` en `generar_fichas.py` y a `CURRICULOS` en `build.py`. Ni el sitio ni el renderizador cambian.
* **Curso nuevo:** añádelo a `CURSOS` en `generar_fichas.py` y da sus 20 entradas en cada currículo.
* **Tipo de ejercicio nuevo:** una función `b_<tipo>` en `generar_fichas.py` o `bloques_texto.py`, su entrada en `RENDER` de `assets/render-ficha.js`, sus estilos en `assets/fichas.css` y su comprobación en `validar.py`.

---

## 🧩 Decisiones de diseño

### Datos en `.js` y no en `.json`

`fetch()` de un archivo local está bloqueado por CORS en `file://`. Con los datos en `.json`, el sitio dejaría de funcionar al abrirlo con doble clic. Sirviéndolos como `.js` que asignan a una variable global y cargándolos con un `<script>` inyectado, funciona igual en `file://` y en un servidor.

### Lo público y lo vendible, separados

`data/fichas/*.js` lleva **solo los ejercicios de las 24 fichas gratuitas**. Las 456 de pago viajan con su título, su objetivo y los tipos de ejercicio que contienen, pero sin contenido.

El motivo es que un bloqueo en el navegador no es un bloqueo: cualquiera abre las herramientas de desarrollo y lo lee. Publicar los ejercicios de pago sería regalarlos. El contenido completo se genera en `dist/`, que está en `.gitignore` y sirve para producir los PDF que se venden.

### Modo claro y oscuro

El interruptor sol/luna lo inyecta `assets/site.js` en la cabecera de todas las páginas. La preferencia se guarda en `localStorage`; si no hay ninguna se sigue `prefers-color-scheme`, y los cambios del sistema se aplican en caliente mientras nadie haya elegido a mano. Un script en línea en el `<head>` aplica el tema antes de pintar, para que no haya fogonazo blanco.

El tema oscuro **no es una inversión de colores**: es una paleta propia de marrón carbón cálido (`#211B17`) con versiones nocturnas de cada pastel, para que siga pareciendo un cuento y no un panel de control. Todos los pares de texto y fondo superan el contraste AA en ambos temas; el mínimo medido es 5,87:1.

### Al imprimir, siempre papel blanco

El bloque `@media print` de `assets/fichas.css` repone la paleta clara con el selector `:root, :root[data-theme="dark"]`, que gana en especificidad al tema oscuro. Esté como esté la pantalla, **por la impresora sale fondo blanco y tinta oscura**: imprimir fondos carbón gastaría un cartucho por cuaderno y dejaría las fichas ilegibles a lápiz.

### Animación con intención

En vez de mover todo, se animan tres momentos: la entrada del hero, la aparición de las tarjetas al cambiar de filtro y la transición entre temas. Las micro-interacciones que ya existían, como el rebote de las casillas, se mantienen. Todo queda anulado por `prefers-reduced-motion`, tanto en CSS como en JavaScript.

---

## 🖨️ Notas de impresión

* Las fichas están maquetadas para **A4 vertical** con márgenes de 12 mm, una ficha por página.
* Activa **«Gráficos de fondo»** en el diálogo de impresión para que salgan los colores pastel.
* Cada ficha tiene un botón **«Imprimir solo esta»** para sacar una sola hoja sin gastar el cuaderno entero.
* El tamaño de letra se adapta al curso: a menor edad, todo más grande.

---

## 📁 Estructura

```text
mundo-aprendizaje/
├── index.html                  Landing, rincones, juego, carruseles y testimonios
├── juegos.html                 Los cuatro minijuegos
├── videos.html                 Catálogo de vídeos
├── descargas.html              Catálogo de fichas con filtros y paginación
├── fichas.html                 Visor e impresión de cualquier cuaderno
├── tienda.html                 Venta de packs y condiciones de compra
├── fichas_matematicas.html     Cuaderno original de Matemáticas (3 fichas)
├── fichas_imprimibles.html     Cuaderno original de Lenguaje, Historia e Idiomas (7 fichas)
│
├── assets/
│   ├── base.css                Tokens de ambos temas, navegación, animaciones, carrusel
│   ├── fichas.css              Estilos de ficha y @media print (A4)
│   ├── site.js                 Carga perezosa, utilidades, voz y modo oscuro
│   ├── render-ficha.js         Convierte los datos de una ficha en HTML imprimible
│   ├── juegos.js               Motor de los cuatro minijuegos
│   ├── carrusel.js             Carrusel accesible: scroll-snap, teclado y swipe
│   └── onboarding.js           Presentación de bienvenida, una sola vez
│
├── data/                       Ver «Qué se genera y qué se edita a mano»
│   ├── catalogo.js             Índice ligero de las 480 fichas
│   ├── packs.js                Packs y precios
│   ├── videos.js               Catálogo de vídeos
│   ├── testimonios.js          ⚠️ Testimonios de ejemplo, no reales
│   └── fichas/
│       └── <tema>-<curso>.js   24 archivos, uno por tema y curso
│
├── tools/
│   ├── generar_fichas.py       Tipos de ejercicio numéricos y utilidades
│   ├── bloques_texto.py        Tipos de ejercicio de texto: sílabas, lectura, ordenar…
│   ├── curriculo_matematicas.py
│   ├── curriculo_lenguaje.py
│   ├── curriculo_historia.py
│   ├── curriculo_idiomas.py
│   ├── build.py                Ensambla data/ y dist/
│   ├── extras.py               Genera packs.js y videos.js
│   ├── validar.py              Comprueba que el contenido es correcto
│   └── auditar.py              Informe de completitud tema × curso
│
├── dist/                       GENERADO, fuera del repositorio (.gitignore)
│   └── fichas/                 Contenido completo, para producir los PDF que se venden
│
└── Cuaderno de {Matemáticas, Lenguaje, Historia, Idiomas} - Mundo Aprendizaje.pdf
```

---

## ⚙️ Tecnologías y accesibilidad

HTML5 semántico, CSS3 con variables nativas y `@media print`, y JavaScript Vanilla ES6+. **Sin frameworks ni dependencias externas.** La única petición a terceros son las tipografías de Google Fonts (Fredoka y Nunito), que degradan a fuentes del sistema si no hay conexión.

En accesibilidad: etiquetas ARIA en los controles icónicos, foco visible, navegación completa por teclado en pestañas, juegos y carruseles, objetivos táctiles de 44 px o más, `prefers-reduced-motion` respetado en CSS y en JS, contraste AA en ambos temas y responsive real sin scroll horizontal.

En rendimiento: el catálogo se recorre con un índice ligero y los ejercicios se cargan solo al abrir un cuaderno, así que navegar las 480 fichas no descarga ni un ejercicio hasta que hace falta.
