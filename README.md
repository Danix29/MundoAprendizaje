# 🦉 Mundo Aprendizaje

![Mundo Aprendizaje Banner](https://via.placeholder.com/1000x300/FFFBF3/3E3427?text=Mundo+Aprendizaje+-+Aprender+jugando)

**Mundo Aprendizaje** es una plataforma educativa interactiva diseñada especialmente para niños y niñas de 3 a 7 años. Su objetivo es acompañar los primeros pasos lectores, matemáticos y creativos a través de juegos interactivos en el navegador y materiales descargables para imprimir.

## ✨ Características Principales

*   **Rincones de Aprendizaje:** Cuatro áreas temáticas principales:
    *   🔢 **Matemáticas:** Sumas, formas y números.
    *   🔤 **Lenguaje:** Abecedario, vocales y primeras palabras.
    *   🦕 **Historia:** Dinosaurios y Antiguo Egipto.
    *   🌍 **Idiomas:** Vocabulario básico en inglés (colores, animales).
*   **Juegos Interactivos:** Tableros táctiles con soporte de voz (usando la *SpeechSynthesis API*) para que los niños escuchen los nombres de los números y los animales al interactuar con ellos.
*   **Zona de Descargas (SPA):** Una página ágil desarrollada con JavaScript Vanilla (ES6+) que permite navegar entre las distintas categorías de fichas sin recargar la página, ofreciendo una experiencia fluida.
*   **Fichas Imprimibles:** Archivos HTML estructurados para impresión (CSS Print Media Queries) que actúan como cuadernos de ejercicios en PDF listos para usar en casa o en el aula.
*   **Diseño Inclusivo y Accesible:** Colores pastel amigables, tipografías legibles (Nunito y Fredoka) y soporte básico de accesibilidad (ARIA tags) para lectores de pantalla.

## 🚀 Tecnologías Utilizadas

Este proyecto está construido con tecnologías web estándar, sin dependencias pesadas ni frameworks, lo que garantiza tiempos de carga ultrarrápidos y un mantenimiento sencillo.

*   **HTML5:** Semántica web pura.
*   **CSS3:** Variables nativas (`:root`), Grid, Flexbox y animaciones suaves.
*   **JavaScript (Vanilla ES6+):** Lógica de la Single Page Application (SPA) para descargas y control del reproductor de voz.
*   **Web Speech API:** Para la síntesis de voz en los juegos interactivos.

## 📁 Estructura del Proyecto

```text
mundo-aprendizaje/
├── index.html                  # Landing page principal y minijuegos interactivos
├── descargas.html              # Zona SPA para explorar y descargar fichas
├── fichas_matematicas.html     # Cuaderno de fichas listo para imprimir (Matemáticas)
├── fichas_imprimibles.html     # Cuaderno de fichas generales para imprimir
└── README.md                   # Documentación del proyecto