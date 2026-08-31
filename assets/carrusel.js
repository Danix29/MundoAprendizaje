/* ============================================================================
   Mundo Aprendizaje — carrusel accesible
   Sin librerías: el desplazamiento es scroll nativo con scroll-snap, así el
   swipe táctil y el trackpad funcionan solos y sin código. El JS solo añade
   flechas, puntos indicadores y teclado.
   ========================================================================== */

window.MA_CARRUSEL = (() => {
  'use strict';

  const { el, reduceMotion } = window.MA;

  /**
   * @param {HTMLElement} raiz  contenedor con .carrusel-pista dentro
   * @param {object} opciones   { etiqueta: string }
   */
  function montar(raiz, opciones = {}){
    const pista = raiz.querySelector('.carrusel-pista');
    if(!pista || raiz.dataset.montado) return;
    raiz.dataset.montado = '1';

    const items = Array.from(pista.children);
    if(!items.length) return;

    pista.setAttribute('role', 'group');
    pista.setAttribute('aria-roledescription', 'carrusel');
    pista.setAttribute('aria-label', opciones.etiqueta || 'Contenido deslizable');
    pista.tabIndex = 0;
    items.forEach((it, i) => {
      it.setAttribute('role', 'group');
      it.setAttribute('aria-roledescription', 'diapositiva');
      it.setAttribute('aria-label', `${i + 1} de ${items.length}`);
    });

    const comportamiento = () => (reduceMotion() ? 'auto' : 'smooth');

    /** Cuántos items caben a la vez, para no pasar de uno en uno de más. */
    const porPagina = () => {
      const anchoItem = items[0].getBoundingClientRect().width;
      return Math.max(1, Math.round(pista.clientWidth / (anchoItem + 22)));
    };

    const indiceActual = () => {
      const anchoItem = items[0].getBoundingClientRect().width + 22;
      return Math.round(pista.scrollLeft / anchoItem);
    };

    function irA(indice){
      const i = Math.max(0, Math.min(indice, items.length - 1));
      // Posición relativa al primer item: offsetLeft se mide contra el
      // offsetParent (el .carrusel, que es position:relative), así que
      // restar el del primero da la distancia correcta dentro del carril.
      const left = items[i].offsetLeft - items[0].offsetLeft;
      pista.scrollTo({ left, behavior: comportamiento() });
    }

    /* ---------------------------------------------------------- flechas */
    const anterior = el('button', {
      className: 'carrusel-flecha carrusel-prev', text: '◀',
      attrs: { type: 'button', 'aria-label': 'Ver anterior' },
    });
    const siguiente = el('button', {
      className: 'carrusel-flecha carrusel-next', text: '▶',
      attrs: { type: 'button', 'aria-label': 'Ver siguiente' },
    });
    anterior.addEventListener('click', () => irA(indiceActual() - porPagina()));
    siguiente.addEventListener('click', () => irA(indiceActual() + porPagina()));

    /* ------------------------------------------------------------ puntos
       Un punto por PÁGINA, no por item: con 24 cuadernos y tres visibles,
       veinticuatro puntos serían ruido en vez de una ayuda. Como el número
       de páginas depende del ancho, se reconstruyen al redimensionar. */
    const MAX_PUNTOS = 8;
    const puntos = el('div', { className: 'carrusel-puntos', attrs: { role: 'tablist', 'aria-label': 'Ir a una página' } });
    const contador = el('p', { className: 'carrusel-contador', attrs: { role: 'status' } });
    let botonesPunto = [];
    let paginasActuales = -1;

    function construirPuntos(){
      const paginas = Math.ceil(items.length / porPagina());
      if(paginas === paginasActuales) return;
      paginasActuales = paginas;
      puntos.replaceChildren();
      botonesPunto = [];

      // En móvil solo cabe una tarjeta: veinticuatro puntos de 12 px serían
      // imposibles de acertar con el dedo. A partir de ocho páginas se cambia
      // por un contador, que ocupa lo mismo y sí se lee.
      const demasiados = paginas > MAX_PUNTOS;
      puntos.hidden = demasiados || paginas <= 1;
      contador.hidden = !demasiados;
      if(demasiados) return;

      botonesPunto = Array.from({ length: paginas }, (_, i) => {
        const b = el('button', {
          className: 'carrusel-punto',
          attrs: { type: 'button', role: 'tab', 'aria-label': `Ir a la página ${i + 1} de ${paginas}` },
        });
        b.addEventListener('click', () => irA(i * porPagina()));
        puntos.append(b);
        return b;
      });
    }

    /* ----------------------------------------------------------- teclado */
    pista.addEventListener('keydown', ev => {
      const salto = { ArrowRight: 1, ArrowLeft: -1, Home: 'inicio', End: 'fin' }[ev.key];
      if(salto === undefined) return;
      ev.preventDefault();
      if(salto === 'inicio') return irA(0);
      if(salto === 'fin') return irA(items.length - 1);
      irA(indiceActual() + salto);
    });

    /* --------------------------------------- estado de puntos y flechas */
    let pendiente = null;
    function sincronizar(){
      construirPuntos();
      const pagina = Math.round(indiceActual() / porPagina());
      botonesPunto.forEach((b, k) => {
        const activo = k === pagina;
        b.setAttribute('aria-selected', String(activo));
        b.classList.toggle('activo', activo);
      });
      // El estado se mide por índice, no por píxeles: con scroll-snap
      // "mandatory" el carril nunca llega al píxel final, así que comparar
      // scrollLeft con scrollWidth dejaba la flecha activa para siempre.
      const i = indiceActual();
      anterior.disabled = i <= 0;
      siguiente.disabled = i >= items.length - porPagina();
      if(!contador.hidden){
        contador.textContent = `${Math.min(i + 1, items.length)} de ${items.length}`;
      }
    }
    pista.addEventListener('scroll', () => {
      if(pendiente) cancelAnimationFrame(pendiente);
      pendiente = requestAnimationFrame(sincronizar);
    });
    window.addEventListener('resize', sincronizar);

    raiz.append(anterior, siguiente, puntos, contador);
    sincronizar();
    return { irA, sincronizar };
  }

  /** Monta todos los carruseles marcados con data-carrusel. */
  function montarTodos(){
    document.querySelectorAll('[data-carrusel]').forEach(c =>
      montar(c, { etiqueta: c.dataset.carrusel }));
  }

  return { montar, montarTodos };
})();
