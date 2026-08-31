/* ============================================================================
   Mundo Aprendizaje — renderizador de fichas
   Convierte un objeto ficha (data/fichas/*.js) en HTML imprimible.
   Requiere assets/site.js y assets/fichas.css.
   ========================================================================== */

window.MA_RENDER = (() => {
  'use strict';

  const { el, icono } = window.MA;
  const SVG_NS = 'http://www.w3.org/2000/svg';

  function svg(viewBox, etiqueta, ...hijos){
    const s = document.createElementNS(SVG_NS, 'svg');
    s.setAttribute('viewBox', viewBox);
    s.setAttribute('role', 'img');
    s.setAttribute('aria-label', etiqueta);
    hijos.flat().forEach(h => s.appendChild(h));
    return s;
  }

  function forma(tag, attrs){
    const n = document.createElementNS(SVG_NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    return n;
  }

  const PUNTEADO = {
    fill: 'none', stroke: 'var(--trace-line)', 'stroke-width': 5,
    'stroke-dasharray': '7 11', 'stroke-linecap': 'round', 'stroke-linejoin': 'round',
  };

  const FIGURAS = {
    circulo:    () => forma('circle',  { cx: 80, cy: 80, r: 62, ...PUNTEADO }),
    cuadrado:   () => forma('rect',    { x: 20, y: 20, width: 120, height: 120, rx: 10, ...PUNTEADO }),
    triangulo:  () => forma('polygon', { points: '80,22 142,138 18,138', ...PUNTEADO }),
    rectangulo: () => forma('rect',    { x: 12, y: 45, width: 136, height: 70, rx: 8, ...PUNTEADO }),
    ovalo:      () => forma('ellipse', { cx: 80, cy: 80, rx: 68, ry: 46, ...PUNTEADO }),
    rombo:      () => forma('polygon', { points: '80,16 144,80 80,144 16,80', ...PUNTEADO }),
  };

  const caja = (clase = '') => el('span', {
    className: `caja ${clase}`.trim(),
    attrs: { role: 'img', 'aria-label': 'Recuadro para escribir la respuesta' },
  });

  /* ------------------------------------------------------ tipos de bloque */
  const RENDER = {

    contar: b => b.items.map(it => el('div', { className: 'fila contar-fila' },
      el('span', { className: 'emoji-serie', attrs: { role: 'img', 'aria-label': `${it.n} veces ${it.emoji}` },
                   text: it.emoji.repeat(it.n) }),
      caja())),

    'tantos-como': b => b.items.map(it => el('div', { className: 'fila contar-fila' },
      el('span', { className: 'emoji-serie', attrs: { role: 'img', 'aria-label': `${it.n} veces ${it.emoji}` },
                   text: it.emoji.repeat(it.n) }),
      caja('caja-grande'))),

    colorear: b => b.items.map(it => el('div', { className: 'fila contar-fila' },
      el('span', { className: 'emoji-serie', attrs: { role: 'img', 'aria-label': `${it.total} veces ${it.emoji}` },
                   text: it.emoji.repeat(it.total) }),
      el('strong', { text: `colorea ${it.colorear}` }))),

    trazo: b => b.items.map(it => el('div', { className: 'trazo-fila' },
      Array.from({ length: it.repeticiones }, (_, i) => el('span', {
        className: i === 0 ? 'glifo' : 'glifo fantasma',
        text: it.glifo,
        attrs: i === 0 ? null : { 'aria-hidden': 'true' },
      })))),

    operaciones: b => {
      const grid = el('div', { className: `ops-grid ${b.formato || 'horizontal'}` });
      b.items.forEach(it => {
        if(b.formato === 'vertical'){
          grid.append(el('div', { className: 'op-v' },
            el('div', { text: String(it.a) }),
            el('div', {}, el('span', { className: 'signo', text: it.op }), String(it.b)),
            el('div', { className: 'linea' }),
            el('div', { className: 'hueco' })));
        }else{
          grid.append(el('div', { className: 'op-h' },
            `${it.a} ${it.op} ${it.b} =`, caja()));
        }
      });
      return [grid];
    },

    comparar: b => [el('div', { className: 'comparar-grid' },
      b.items.map(it => el('div', { className: 'comparar-item' },
        String(it.a), caja(), String(it.b))))],

    serie: b => b.items.map(it => {
      const fila = el('div', { className: 'serie-fila' });
      it.valores.forEach((v, i) => {
        if(i) fila.append(icono('→'));
        fila.append(it.huecos.includes(i)
          ? caja('caja-ancha')
          : el('span', { className: 'serie-valor', text: String(v) }));
      });
      return fila;
    }),

    unir: b => [el('div', { className: 'unir' },
      el('ul', { className: 'col-izq' }, b.izq.map(v => el('li', {},
        el('span', { className: 'contenido', text: v }),
        el('span', { className: 'punto', attrs: { 'aria-hidden': 'true' } })))),
      el('ul', { className: 'col-der' }, b.der.map(v => el('li', {},
        el('span', { className: 'contenido', text: v }),
        el('span', { className: 'punto', attrs: { 'aria-hidden': 'true' } })))))],

    problema: b => b.items.map(it => el('div', { className: 'problema' },
      el('p', { className: 'problema-texto', text: it.texto }),
      el('div', { className: 'problema-pie' },
        el('span', { text: 'Operación:' }),
        el('span', { className: 'problema-operacion', attrs: { role: 'img', 'aria-label': 'Espacio para la operación' } })),
      el('div', { className: 'problema-pie', style: { marginTop: '10px' } },
        el('span', { text: `Solución: ${it.unidad}` }), caja('caja-ancha')))),

    formas: b => [el('div', { className: 'formas-grid' },
      b.items.map(it => el('div', { className: 'forma-celda' },
        svg('0 0 160 160', `${it.nombre} punteado para repasar`, (FIGURAS[it.forma] || FIGURAS.circulo)()),
        el('p', { className: 'forma-nombre', text: it.nombre }))))],

    reloj: b => [el('div', { className: 'relojes' },
      b.items.map(it => {
        const ah = ((it.h % 12) + it.m / 60) * 30 - 90;       // aguja horaria
        const am = it.m * 6 - 90;                              // minutero
        const rad = g => (g * Math.PI) / 180;
        const marcas = Array.from({ length: 12 }, (_, i) => {
          const a = rad(i * 30 - 90);
          return forma('circle', { cx: 60 + 44 * Math.cos(a), cy: 60 + 44 * Math.sin(a), r: 2.4, fill: 'var(--trace-line)' });
        });
        return el('div', { className: 'reloj-celda' },
          svg('0 0 120 120', 'Reloj de agujas',
            forma('circle', { cx: 60, cy: 60, r: 54, fill: 'var(--white)', stroke: 'var(--trace-line)', 'stroke-width': 4 }),
            marcas,
            forma('line', { x1: 60, y1: 60, x2: 60 + 26 * Math.cos(rad(ah)), y2: 60 + 26 * Math.sin(rad(ah)),
                            stroke: 'var(--ink)', 'stroke-width': 5, 'stroke-linecap': 'round' }),
            forma('line', { x1: 60, y1: 60, x2: 60 + 38 * Math.cos(rad(am)), y2: 60 + 38 * Math.sin(rad(am)),
                            stroke: 'var(--ink)', 'stroke-width': 3, 'stroke-linecap': 'round' }),
            forma('circle', { cx: 60, cy: 60, r: 4, fill: 'var(--ink)' })),
          caja());
      }))],

    descomponer: b => [el('div', { className: 'descomp-grid' },
      b.items.map(it => el('div', { className: 'descomp' },
        String(it.parte), '+', caja(), '=', String(b.total))))],

    rodear: b => b.items.map(it => el('div', { className: 'rodear-fila' },
      it.opciones.map(o => el('span', { className: 'rodear-op', text: String(o) })))),

    emparejar: b => b.items.map(it => el('div', { className: 'emparejar-fila' },
      el('span', { className: 'emparejar-modelo', text: it.modelo }),
      icono('→'),
      it.opciones.map(o => el('span', { className: 'emparejar-op', text: o })))),

    vecinos: b => [el('div', { className: 'vecinos-grid' },
      b.items.map(it => {
        const fila = el('div', { className: 'vecino' });
        if(b.pide !== 'posterior') fila.append(caja());
        fila.append(el('span', { className: 'num', text: String(it.n) }));
        if(b.pide !== 'anterior') fila.append(caja());
        return fila;
      }))],

    tabla: b => [el('div', { className: 'tabla-mult' },
      b.items.map(it => el('div', { className: 'tabla-fila' },
        `${b.n} × ${it.b} =`,
        b.huecos.includes(it.b)
          ? caja()
          : el('span', { className: 'resuelto', text: String(it.r) }))))],

    concepto: b => [el('div', { className: 'concepto-grid' },
      b.items.map(it => el('div', { className: 'concepto-celda' },
        el('div', { className: 'concepto-emoji', text: it.emoji, attrs: { role: 'img', 'aria-label': it.criterio } }),
        el('div', { className: 'concepto-etiqueta', text: it.criterio }))))],

    monedas: b => [el('div', { className: 'monedas-grid' },
      b.items.map(it => el('div', { className: 'monedas-fila' },
        el('span', { attrs: { role: 'img', 'aria-label': `${it.un_euro} monedas de un euro y ${it.dos_euros} de dos euros` },
                     text: '🪙'.repeat(it.un_euro) + '💰'.repeat(it.dos_euros) }),
        el('span', { text: `${it.un_euro}×1€  ${it.dos_euros}×2€` }),
        caja())))],

    /* ------------------ Lenguaje, Historia e Idiomas ------------------ */

    silabas: b => b.items.map(it => el('div', { className: 'fila silabas-fila' },
      el('span', { className: 'silabas-pic', text: it.emoji, attrs: { 'aria-hidden': 'true' } }),
      el('span', { className: 'silabas-palabra', text: it.palabra }),
      el('span', { className: 'silabas-cajas' },
        it.silabas.map(() => el('span', { className: 'caja caja-silaba' }))),
      caja())),

    escritura: b => b.items.map(it => el('div', { className: 'escritura-fila' },
      el('span', { className: 'escritura-pic', text: it.emoji, attrs: { 'aria-hidden': 'true' } }),
      el('span', { className: 'glifo escritura-modelo', text: it.palabra }),
      el('span', { className: 'pauta', attrs: { role: 'img', 'aria-label': `Línea para escribir ${it.palabra}` } }))),

    completar: b => [el('div', { className: 'completar-grid' },
      b.items.map(it => el('div', { className: 'completar-item' },
        el('span', { className: 'completar-pic', text: it.emoji, attrs: { 'aria-hidden': 'true' } }),
        el('span', { className: 'completar-palabra' },
          el('span', { text: it.antes }),
          el('span', { className: 'caja caja-letra' }),
          el('span', { text: it.despues })))))],

    clasificar: b => {
      const banco = el('div', { className: 'clasificar-banco' },
        b.items.map(it => el('span', { className: 'clasificar-pieza', text: it.contenido })));
      const cols = el('div', { className: 'clasificar-cols' },
        b.columnas.map(nombre => el('div', { className: 'clasificar-col' },
          el('h4', { text: nombre }),
          el('div', { className: 'clasificar-hueco', attrs: { role: 'img', 'aria-label': `Espacio para ${nombre}` } }))));
      return [banco, cols];
    },

    lectura: b => {
      const nodos = [el('blockquote', { className: 'lectura-texto', text: b.texto })];
      nodos.push(el('ol', { className: 'lectura-preguntas' },
        b.items.map(it => el('li', {},
          el('p', { className: 'lectura-pregunta', text: it.pregunta }),
          el('span', { className: 'pauta', attrs: { role: 'img', 'aria-label': 'Línea para la respuesta' } })))));
      return nodos;
    },

    'verdadero-falso': b => [el('ul', { className: 'vf-lista' },
      b.items.map(it => el('li', { className: 'vf-fila' },
        el('span', { className: 'vf-texto', text: it.texto }),
        el('span', { className: 'vf-opciones' },
          el('span', { className: 'vf-op', text: 'V' }),
          el('span', { className: 'vf-op', text: 'F' })))))],

    ordenar: b => [el('ul', { className: 'ordenar-lista' },
      b.items.map(it => el('li', { className: 'ordenar-fila' },
        el('span', { className: 'caja caja-orden' }),
        el('span', { className: 'ordenar-texto', text: it.contenido }))))],

    dibujar: b => [el('div', { className: `zona-dibujo zona-${b.alto || 'grande'}` },
      el('span', { className: 'zona-pie', text: b.pie }))],

    vocabulario: b => [el('div', { className: 'vocab-grid' },
      b.items.map(it => el('div', { className: 'vocab-celda' },
        el('span', { className: 'vocab-pic', text: it.emoji, attrs: { role: 'img', 'aria-label': it.es } }),
        el('span', { className: 'glifo vocab-en', text: it.en }),
        el('span', { className: 'vocab-es', text: it.es }))))],

    frase: b => b.items.map(it => el('div', { className: 'frase-fila' },
      el('span', { text: it.antes }),
      caja('caja-ancha'),
      el('span', { text: it.despues }))),

    'colorear-ingles': b => [el('div', { className: 'formas-grid' },
      b.items.map(it => el('div', { className: 'forma-celda' },
        svg('0 0 160 160', `${it.en} para colorear`, (FIGURAS[it.forma] || FIGURAS.circulo)()),
        el('p', { className: 'forma-nombre', text: it.en }))))],
  };

  /** Renderiza un bloque; si el tipo fuese desconocido no rompe la ficha. */
  function renderBloque(b, indice){
    const cuerpo = RENDER[b.tipo];
    return el('section', { className: 'bloque' },
      el('div', { className: 'bloque-enunciado' },
        el('span', { className: 'bloque-num', text: String(indice), attrs: { 'aria-hidden': 'true' } }),
        el('span', { text: b.enunciado })),
      cuerpo ? cuerpo(b) : el('p', { text: '(Este ejercicio se verá al imprimir.)' }));
  }

  /**
   * Renderiza una ficha completa.
   * @param {object} f ficha del catálogo
   * @param {object} opciones { conBotonImprimir: boolean }
   */
  function renderFicha(f, opciones = {}){
    const cat = window.MA.catalogo();
    const tema = cat.temas[f.tema] || {};
    const curso = cat.cursos[String(f.curso)] || {};

    const art = el('article', {
      className: `ficha t-${tema.color || 'peach'}`,
      attrs: { id: f.id, 'data-curso': f.curso, 'data-tema': f.tema },
    });

    art.append(
      el('header', { className: 'ficha-head' },
        el('div', { className: 'ficha-head-title' },
          el('span', { className: 'ficha-emoji', text: tema.icono, attrs: { 'aria-hidden': 'true' } }),
          el('div', {},
            el('h2', { text: f.titulo }),
            el('div', { className: 'ficha-meta', text: `${tema.nombre} · ${curso.etiqueta} (${curso.etapa}) · Ficha ${f.orden} de 20` }))),
        el('div', { className: 'ficha-fields' },
          el('span', { className: 'field' }, 'Nombre: ', el('span', { className: 'field-line', attrs: { 'aria-hidden': 'true' } })),
          el('span', { className: 'field' }, 'Fecha: ', el('span', { className: 'field-line', attrs: { 'aria-hidden': 'true' } })))),
      el('p', { className: 'ficha-objetivo', text: `Objetivo: ${f.objetivo}` }),
    );

    f.bloques.forEach((b, i) => art.append(renderBloque(b, i + 1)));

    const pie = el('footer', { className: 'ficha-foot' },
      el('span', { text: `Mundo Aprendizaje · ${tema.nombre} · ${curso.etiqueta} · Ficha ${f.orden}` }));
    if(opciones.conBotonImprimir !== false){
      const btn = el('button', { className: 'btn-print-one no-print', text: '🖨️ Imprimir solo esta', attrs: { type: 'button' } });
      btn.addEventListener('click', () => imprimirSolo(art));
      pie.append(btn);
    }
    art.append(pie);
    return art;
  }

  /* Imprime una sola ficha ocultando el resto mientras dura el diálogo. */
  function restaurar(){
    document.body.classList.remove('printing-one');
    document.querySelectorAll('.print-target').forEach(n => n.classList.remove('print-target'));
  }
  window.addEventListener('afterprint', restaurar);

  function imprimirSolo(art){
    restaurar();
    art.classList.add('print-target');
    document.body.classList.add('printing-one');
    window.print();
    setTimeout(restaurar, 2000);   // red de seguridad si no llega afterprint
  }

  return { renderFicha, renderBloque, imprimirSolo };
})();
