/* ============================================================================
   Mundo Aprendizaje — presentación breve de bienvenida
   Cuatro pantallas deslizables la primera vez que alguien entra. Nunca bloquea:
   se puede saltar, cerrar con Escape o pulsar fuera, y no vuelve a salir.
   ========================================================================== */

window.MA_ONBOARDING = (() => {
  'use strict';

  const { el, icono, reduceMotion } = window.MA;
  const CLAVE = 'ma-onboarding-visto';

  const PANTALLAS = [
    { emoji: '🦉', titulo: '¡Hola! Esto es Mundo Aprendizaje',
      texto: 'Un rincón para peques de 2 a 7 años con juegos, vídeos y fichas para imprimir. Te lo enseñamos en veinte segundos.' },
    { emoji: '🎮', titulo: 'Juegos que hablan',
      texto: 'Cuatro minijuegos con voz: animales y números, letras, la línea del tiempo y un memory en inglés. Se adaptan al curso y son gratis.' },
    { emoji: '🖨️', titulo: 'Fichas para imprimir',
      texto: 'Cuadernos de 20 fichas por tema y curso, de la más sencilla a la más completa. Cada curso tiene una ficha de muestra gratuita.' },
    { emoji: '🌙', titulo: 'A tu manera',
      texto: 'Puedes cambiar entre modo claro y oscuro con el botón de la cabecera, y apagar la voz de los juegos cuando lo necesites.' },
  ];

  function yaVisto(){
    try{ return localStorage.getItem(CLAVE) === '1'; }catch(e){ return true; }
  }
  function marcarVisto(){
    try{ localStorage.setItem(CLAVE, '1'); }catch(e){ /* modo privado */ }
  }

  function montar(){
    if(yaVisto()) return;

    let indice = 0;
    const pista = el('div', { className: 'onboarding-pista' },
      PANTALLAS.map((p, i) => el('section', {
        className: 'onboarding-slide',
        attrs: { 'aria-label': `Paso ${i + 1} de ${PANTALLAS.length}` },
      },
        el('span', { className: 'onboarding-emoji', text: p.emoji, attrs: { 'aria-hidden': 'true' } }),
        el('h2', { text: p.titulo }),
        el('p', { text: p.texto }))));

    const puntos = el('div', { className: 'onboarding-puntos' },
      PANTALLAS.map((_, i) => {
        const b = el('button', { className: 'onboarding-punto',
          attrs: { type: 'button', 'aria-label': `Ir al paso ${i + 1}` } });
        b.addEventListener('click', () => irA(i));
        return b;
      }));

    const saltar = el('button', { className: 'btn btn-ghost', text: 'Saltar',
      attrs: { type: 'button' } });
    const siguiente = el('button', { className: 'btn btn-primary',
      attrs: { type: 'button' } });

    const caja = el('div', { className: 'onboarding-caja',
      attrs: { role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'onbTitulo' } },
      pista,
      el('div', { className: 'onboarding-pie' }, saltar, puntos, siguiente));
    caja.querySelector('h2').id = 'onbTitulo';

    const capa = el('div', { className: 'onboarding' }, caja);

    function irA(i){
      indice = Math.max(0, Math.min(i, PANTALLAS.length - 1));
      const destino = pista.children[indice];
      pista.scrollTo({ left: destino.offsetLeft, behavior: reduceMotion() ? 'auto' : 'smooth' });
      sincronizar();
    }

    function sincronizar(){
      puntos.querySelectorAll('.onboarding-punto').forEach((b, k) => {
        b.classList.toggle('activo', k === indice);
        b.setAttribute('aria-current', String(k === indice));
      });
      const ultimo = indice === PANTALLAS.length - 1;
      siguiente.replaceChildren(ultimo ? '¡Vamos allá!' : 'Siguiente', icono(ultimo ? '🎈' : '→'));
    }

    function cerrar(){
      marcarVisto();
      capa.remove();
      document.removeEventListener('keydown', alPulsarTecla);
      if(foco) foco.focus();
    }

    function alPulsarTecla(ev){
      if(ev.key === 'Escape') return cerrar();
      if(ev.key === 'ArrowRight') irA(indice + 1);
      if(ev.key === 'ArrowLeft') irA(indice - 1);
      // Encierra el tabulador dentro del diálogo mientras esté abierto
      if(ev.key === 'Tab'){
        const focos = caja.querySelectorAll('button');
        const primero = focos[0], ultimo = focos[focos.length - 1];
        if(ev.shiftKey && document.activeElement === primero){ ev.preventDefault(); ultimo.focus(); }
        else if(!ev.shiftKey && document.activeElement === ultimo){ ev.preventDefault(); primero.focus(); }
      }
    }

    saltar.addEventListener('click', cerrar);
    siguiente.addEventListener('click', () =>
      indice === PANTALLAS.length - 1 ? cerrar() : irA(indice + 1));
    capa.addEventListener('click', ev => { if(ev.target === capa) cerrar(); });
    pista.addEventListener('scroll', () => {
      const i = Math.round(pista.scrollLeft / pista.clientWidth);
      if(i !== indice){ indice = i; sincronizar(); }
    });
    document.addEventListener('keydown', alPulsarTecla);

    const foco = document.activeElement;
    document.body.appendChild(capa);
    sincronizar();
    siguiente.focus();
  }

  /** Permite volver a verlo desde el pie, sin borrar localStorage a mano. */
  function reiniciar(){
    try{ localStorage.removeItem(CLAVE); }catch(e){ /* ignorado */ }
    montar();
  }

  return { montar, reiniciar };
})();
