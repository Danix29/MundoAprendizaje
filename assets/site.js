/* ============================================================================
   Mundo Aprendizaje — utilidades compartidas
   Carga perezosa de datos, helpers de DOM y formato.
   ========================================================================== */

window.MA = (() => {
  'use strict';

  const cache = new Map();

  /**
   * Carga bajo demanda las fichas de un tema y curso.
   *
   * Se inyecta un <script> en vez de usar fetch() a proposito: fetch() sobre
   * un archivo local esta bloqueado por CORS en file://, asi que el sitio
   * dejaria de funcionar al abrirlo con doble clic. Un <script> no lo esta.
   *
   * @param {string} tema
   * @param {number|string} curso
   * @returns {Promise<Array>} fichas de ese tema y curso
   */
  function cargarFichas(tema, curso){
    const clave = `${tema}-${curso}`;
    if(cache.has(clave)) return cache.get(clave);

    const promesa = new Promise((resolve, reject) => {
      const yaCargado = window.MA_FICHAS && window.MA_FICHAS[clave];
      if(yaCargado) return resolve(yaCargado);

      const script = document.createElement('script');
      script.src = `data/fichas/${clave}.js`;
      script.onload = () => {
        const datos = window.MA_FICHAS && window.MA_FICHAS[clave];
        datos ? resolve(datos) : reject(new Error(`Sin datos para ${clave}`));
      };
      script.onerror = () => reject(new Error(`No se pudo cargar ${clave}`));
      document.head.appendChild(script);
    });

    cache.set(clave, promesa);
    return promesa;
  }

  /** Crea un elemento con clase, texto, atributos e hijos en una sola llamada. */
  function el(tag, opciones = {}, ...hijos){
    const { className, text, attrs, style } = opciones;
    const nodo = document.createElement(tag);
    if(className) nodo.className = className;
    if(text != null) nodo.textContent = text;
    if(attrs) Object.entries(attrs).forEach(([k, v]) => {
      if(v != null && v !== false) nodo.setAttribute(k, v === true ? '' : v);
    });
    if(style) Object.assign(nodo.style, style);
    hijos.flat().forEach(h => h != null && nodo.append(h));
    return nodo;
  }

  /** Icono decorativo: siempre oculto para lectores de pantalla. */
  const icono = txt => el('span', { text: txt, attrs: { 'aria-hidden': 'true' } });

  const catalogo = () => window.MA_CATALOGO || { fichas: [], temas: {}, cursos: {} };

  /** Fichas del indice filtradas por tema, curso y acceso. */
  function filtrar({ tema, curso, soloGratis } = {}){
    return catalogo().fichas.filter(f =>
      (!tema || f.tema === tema) &&
      (!curso || String(f.curso) === String(curso)) &&
      (!soloGratis || f.gratis)
    );
  }

  const etiquetaCurso = curso => {
    const c = catalogo().cursos[String(curso)];
    return c ? `${c.etiqueta} · ${c.etapa}` : `${curso} años`;
  };

  const precio = n => n.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });

  const reduceMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --------------------------------------------------------------- voz es-ES */
  const vozDisponible = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  let vozActiva = vozDisponible;

  /**
   * @param {string} texto
   * @param {string} [lang] 'es-ES' por defecto; 'en-GB' para el vocabulario
   *                        en inglés, donde leerlo en español sonaría mal.
   */
  function hablar(texto, lang = 'es-ES'){
    if(!vozActiva || !vozDisponible) return;
    try{
      speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(texto);
      u.lang = lang;
      u.rate = lang.startsWith('en') ? 0.85 : 0.95;
      u.pitch = 1.15;
      speechSynthesis.speak(u);
    }catch(e){ /* silencioso si el navegador no lo soporta */ }
  }

  function alternarVoz(){
    vozActiva = !vozActiva;
    if(!vozActiva && vozDisponible) speechSynthesis.cancel();
    return vozActiva;
  }

  /* ------------------------------------------------------------------ tema
     El tema se aplica en un script en línea del <head> para que no haya
     parpadeo; aquí solo se monta el interruptor y se guarda la elección. */
  const CLAVE_TEMA = 'ma-tema';

  const temaDelSistema = () =>
    window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

  const temaActual = () => document.documentElement.dataset.theme || temaDelSistema();

  function aplicarTema(tema, guardar){
    document.documentElement.dataset.theme = tema;
    const meta = document.querySelector('meta[name="theme-color"]');
    if(meta) meta.setAttribute('content', tema === 'dark' ? '#211B17' : '#FFFBF3');
    if(guardar){
      try{ localStorage.setItem(CLAVE_TEMA, tema); }catch(e){ /* modo privado */ }
    }
    document.querySelectorAll('.tema-btn').forEach(b => sincronizarBoton(b, tema));
  }

  function sincronizarBoton(btn, tema){
    const oscuro = tema === 'dark';
    btn.setAttribute('aria-pressed', String(oscuro));
    btn.setAttribute('aria-label', oscuro ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
    btn.title = oscuro ? 'Modo claro' : 'Modo oscuro';
    btn.textContent = oscuro ? '☀️' : '🌙';
  }

  /** Inserta el interruptor de tema en la cabecera de cualquier página. */
  function montarTema(){
    const barra = document.querySelector('.topbar-inner');
    if(!barra || barra.querySelector('.tema-btn')) return;

    const btn = el('button', {
      className: 'tema-btn',
      attrs: { type: 'button', 'aria-pressed': 'false' },
    });
    sincronizarBoton(btn, temaActual());
    btn.addEventListener('click', () =>
      aplicarTema(temaActual() === 'dark' ? 'light' : 'dark', true));
    barra.appendChild(btn);

    // Si no hay preferencia guardada, seguimos al sistema en caliente.
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', ev => {
      let guardado = null;
      try{ guardado = localStorage.getItem(CLAVE_TEMA); }catch(e){ /* ignorado */ }
      if(!guardado) aplicarTema(ev.matches ? 'dark' : 'light', false);
    });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', montarTema);
  }else{
    montarTema();
  }

  return {
    cargarFichas, el, icono, catalogo, filtrar, etiquetaCurso, precio,
    reduceMotion, hablar, alternarVoz, aplicarTema, temaActual,
    get vozDisponible(){ return vozDisponible; },
    get vozActiva(){ return vozActiva; },
  };
})();
