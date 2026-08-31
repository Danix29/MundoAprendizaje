/* ============================================================================
   Mundo Aprendizaje — minijuegos
   Cuatro juegos, uno por rincón. Sin dependencias externas.
   Cada juego expone montar(contenedor, nivel) y se adapta al curso elegido.
   ========================================================================== */

window.MA_JUEGOS = (() => {
  'use strict';

  const { el, icono, hablar, reduceMotion } = window.MA;

  /* Cuántos elementos mostrar según el curso: los mayores reciben más. */
  const NIVEL = {
    2: { tablero: 6,  opciones: 2, parejas: 3, sucesos: 3 },
    3: { tablero: 8,  opciones: 2, parejas: 3, sucesos: 3 },
    4: { tablero: 10, opciones: 3, parejas: 4, sucesos: 4 },
    5: { tablero: 12, opciones: 3, parejas: 4, sucesos: 4 },
    6: { tablero: 15, opciones: 4, parejas: 6, sucesos: 5 },
    7: { tablero: 18, opciones: 4, parejas: 6, sucesos: 6 },
  };
  const nivel = curso => NIVEL[curso] || NIVEL[5];

  const barajar = arr => {
    const a = arr.slice();
    for(let i = a.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  function rebotar(nodo){
    if(reduceMotion()) return;
    nodo.classList.remove('rebota');
    void nodo.offsetWidth;
    nodo.classList.add('rebota');
  }

  function marcador(contenedor){
    const texto = el('span', { className: 'marcador-texto', text: '' });
    const caja = el('div', { className: 'marcador', attrs: { role: 'status' } }, texto);
    contenedor.append(caja);
    return {
      decir(msg, emoji){ texto.textContent = (emoji ? emoji + ' ' : '') + msg; },
      nodo: caja,
    };
  }

  /* ======================================================================
     1. TOCA Y DESCUBRE — animales y números (Matemáticas / general)
     ====================================================================== */
  const ANIMALES = [
    { emoji: '🐶', name: 'Perro',    sound: 'Perro. ¡Guau, guau!' },
    { emoji: '🐱', name: 'Gato',     sound: 'Gato. ¡Miau, miau!' },
    { emoji: '🐮', name: 'Vaca',     sound: 'Vaca. ¡Muu!' },
    { emoji: '🦁', name: 'León',     sound: 'León. ¡Grrr!' },
    { emoji: '🐘', name: 'Elefante', sound: 'Elefante.' },
    { emoji: '🐥', name: 'Pollito',  sound: 'Pollito. ¡Pío, pío!' },
    { emoji: '🐸', name: 'Rana',     sound: 'Rana. ¡Croac, croac!' },
    { emoji: '🐴', name: 'Caballo',  sound: 'Caballo.' },
    { emoji: '🐷', name: 'Cerdito',  sound: 'Cerdito. ¡Oink, oink!' },
    { emoji: '🦆', name: 'Pato',     sound: 'Pato. ¡Cuac, cuac!' },
    { emoji: '🐰', name: 'Conejo',   sound: 'Conejo.' },
    { emoji: '🐢', name: 'Tortuga',  sound: 'Tortuga.' },
    { emoji: '🐝', name: 'Abeja',    sound: 'Abeja. ¡Bzzz!' },
    { emoji: '🦉', name: 'Búho',     sound: 'Búho. ¡Uh, uh!' },
    { emoji: '🐬', name: 'Delfín',   sound: 'Delfín.' },
    { emoji: '🦋', name: 'Mariposa', sound: 'Mariposa.' },
    { emoji: '🐟', name: 'Pez',      sound: 'Pez.' },
    { emoji: '🐑', name: 'Oveja',    sound: 'Oveja. ¡Beee!' },
  ];
  const PALABRAS_NUM = ['cero','uno','dos','tres','cuatro','cinco','seis','siete','ocho',
                        'nueve','diez','once','doce','trece','catorce','quince','dieciséis',
                        'diecisiete','dieciocho'];

  function tocaYDescubre(raiz, curso){
    const n = nivel(curso).tablero;
    const escena = el('div', { className: 'escena', attrs: { role: 'status' } },
      el('span', { className: 'escena-emoji', text: '👋', attrs: { 'aria-hidden': 'true' } }),
      el('div', {}, el('div', { className: 'escena-nombre', text: '¡Elige algo para empezar!' }),
        el('div', { className: 'escena-pista', text: 'Toca cualquier casilla del tablero.' })));
    const emoji = escena.querySelector('.escena-emoji');
    const nombre = escena.querySelector('.escena-nombre');
    const pista = escena.querySelector('.escena-pista');

    const tabAnimales = el('button', { className: 'tab-btn', text: '🐾 Animales',
      attrs: { type: 'button', role: 'tab', 'aria-selected': 'true', 'aria-controls': 'jgAnimales' } });
    const tabNumeros = el('button', { className: 'tab-btn', text: '🔢 Números',
      attrs: { type: 'button', role: 'tab', 'aria-selected': 'false', 'aria-controls': 'jgNumeros', tabindex: '-1' } });
    const tabs = el('div', { className: 'tabs', attrs: { role: 'tablist', 'aria-label': 'Elegir actividad' } },
      tabAnimales, tabNumeros);

    const boardA = el('div', { className: 'tablero', attrs: { id: 'jgAnimales', role: 'tabpanel', 'aria-labelledby': 'jgTabAnimales' } });
    const boardN = el('div', { className: 'tablero', attrs: { id: 'jgNumeros', role: 'tabpanel', hidden: true } });

    barajar(ANIMALES).slice(0, n).forEach(a => {
      const b = el('button', { className: 'casilla', text: a.emoji,
                               attrs: { type: 'button', 'aria-label': a.name } });
      b.addEventListener('click', () => {
        rebotar(b);
        emoji.textContent = a.emoji;
        nombre.textContent = a.name;
        pista.textContent = '¡Muy bien! Sigue explorando el tablero.';
        hablar(a.sound);
      });
      boardA.append(b);
    });

    for(let i = 1; i <= n; i++){
      const b = el('button', { className: 'casilla', text: String(i),
                               attrs: { type: 'button', 'aria-label': 'Número ' + i } });
      b.addEventListener('click', () => {
        rebotar(b);
        const fila = el('span', { className: 'estrellas' });
        for(let k = 0; k < i; k++){
          const s = el('span', { className: 'estrella', text: '⭐' });
          s.style.animationDelay = (k * 0.04) + 's';
          fila.append(s);
        }
        emoji.replaceChildren(fila);
        nombre.textContent = 'Número ' + i;
        pista.textContent = '¡Cuenta las estrellitas conmigo!';
        hablar('Número ' + (PALABRAS_NUM[i] || i));
      });
      boardN.append(b);
    }

    const lista = [tabAnimales, tabNumeros];
    const paneles = [boardA, boardN];
    const elegir = (i, foco) => {
      lista.forEach((t, k) => {
        t.setAttribute('aria-selected', String(k === i));
        t.tabIndex = k === i ? 0 : -1;
        paneles[k].hidden = k !== i;
      });
      if(foco) lista[i].focus();
    };
    lista.forEach((t, i) => {
      t.addEventListener('click', () => elegir(i, false));
      t.addEventListener('keydown', ev => {
        const paso = { ArrowRight: 1, ArrowLeft: -1 }[ev.key];
        if(!paso) return;
        ev.preventDefault();
        elegir((i + paso + lista.length) % lista.length, true);
      });
    });

    raiz.append(escena, tabs, boardA, boardN);
  }

  /* ======================================================================
     2. LA LETRA PERDIDA — asociar letra e imagen (Lenguaje)
     ====================================================================== */
  const PALABRAS = [
    { letra: 'A', emoji: '🌳', palabra: 'Árbol' },
    { letra: 'B', emoji: '🚌', palabra: 'Bus' },
    { letra: 'C', emoji: '🏠', palabra: 'Casa' },
    { letra: 'D', emoji: '🦕', palabra: 'Dinosaurio' },
    { letra: 'E', emoji: '🐘', palabra: 'Elefante' },
    { letra: 'F', emoji: '🌻', palabra: 'Flor' },
    { letra: 'G', emoji: '🐱', palabra: 'Gato' },
    { letra: 'H', emoji: '🍦', palabra: 'Helado' },
    { letra: 'I', emoji: '🏝️', palabra: 'Isla' },
    { letra: 'L', emoji: '🌙', palabra: 'Luna' },
    { letra: 'M', emoji: '🐵', palabra: 'Mono' },
    { letra: 'N', emoji: '☁️', palabra: 'Nube' },
    { letra: 'O', emoji: '🐻', palabra: 'Oso' },
    { letra: 'P', emoji: '🐶', palabra: 'Perro' },
    { letra: 'R', emoji: '🐸', palabra: 'Rana' },
    { letra: 'S', emoji: '☀️', palabra: 'Sol' },
    { letra: 'T', emoji: '🐢', palabra: 'Tortuga' },
    { letra: 'U', emoji: '🍇', palabra: 'Uvas' },
    { letra: 'V', emoji: '🐮', palabra: 'Vaca' },
    { letra: 'Z', emoji: '🦊', palabra: 'Zorro' },
  ];

  /* Cada palabra debe empezar de verdad por su letra. Se comprueba al cargar
     porque un desajuste aquí enseñaría algo incorrecto sin dar ningún error. */
  const sinAcento = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase();
  PALABRAS.forEach(p => {
    if(sinAcento(p.palabra)[0] !== sinAcento(p.letra)){
      console.error(`[juegos] "${p.palabra}" no empieza por ${p.letra}`);
    }
  });

  function laLetraPerdida(raiz, curso){
    const nOpciones = nivel(curso).opciones;
    let aciertos = 0, rondas = 0, actual = null;

    const letraGrande = el('div', { className: 'letra-grande' });
    const opciones = el('div', { className: 'opciones' });
    const m = marcador(raiz);

    const btnRepetir = el('button', { className: 'btn btn-secondary', attrs: { type: 'button' } },
      icono('🔊'), 'Escuchar otra vez');
    btnRepetir.addEventListener('click', () => actual && hablar(`La letra ${actual.letra}`));

    function ronda(){
      rondas++;
      const elegidas = barajar(PALABRAS).slice(0, nOpciones);
      actual = elegidas[0];
      letraGrande.textContent = actual.letra;
      letraGrande.setAttribute('aria-label', `Letra ${actual.letra}`);
      m.decir(`¿Qué dibujo empieza por la letra ${actual.letra}?`, '🔤');
      hablar(`Busca la letra ${actual.letra}`);

      opciones.replaceChildren(...barajar(elegidas).map(op => {
        const b = el('button', { className: 'casilla casilla-grande', text: op.emoji,
                                 attrs: { type: 'button', 'aria-label': op.palabra } });
        b.addEventListener('click', () => {
          if(op.letra === actual.letra){
            aciertos++;
            rebotar(b);
            b.classList.add('acierto');
            m.decir(`¡Muy bien! ${op.palabra} empieza por ${actual.letra}. Llevas ${aciertos} de ${rondas}.`, '🎉');
            hablar(`¡Muy bien! ${op.palabra} empieza por ${actual.letra}`);
            setTimeout(ronda, reduceMotion() ? 300 : 1400);
          }else{
            b.classList.add('fallo');
            m.decir(`Eso es ${op.palabra}. Empieza por ${op.letra}. ¡Prueba otra vez!`, '🤔');
            hablar(`Eso es ${op.palabra}. Inténtalo otra vez.`);
            setTimeout(() => b.classList.remove('fallo'), 700);
          }
        });
        return b;
      }));
    }

    raiz.append(letraGrande, opciones, el('div', { className: 'juego-acciones' }, btnRepetir));
    ronda();
  }

  /* ======================================================================
     3. LÍNEA DEL TIEMPO — ordenar sucesos (Historia)
     ====================================================================== */
  const SUCESOS = [
    { emoji: '🦕', nombre: 'Los dinosaurios', orden: 1 },
    { emoji: '🦣', nombre: 'Los mamuts',      orden: 2 },
    { emoji: '🔥', nombre: 'La prehistoria',  orden: 3 },
    { emoji: '🏜️', nombre: 'Antiguo Egipto',  orden: 4 },
    { emoji: '🏛️', nombre: 'Antigua Roma',    orden: 5 },
    { emoji: '🏰', nombre: 'Los castillos',   orden: 6 },
    { emoji: '🚂', nombre: 'El primer tren',  orden: 7 },
    { emoji: '🚀', nombre: 'Viajar al espacio', orden: 8 },
  ];

  function lineaDelTiempo(raiz, curso){
    const n = nivel(curso).sucesos;
    const elegidos = barajar(SUCESOS).slice(0, n).sort((a, b) => a.orden - b.orden);
    let actual = barajar(elegidos);
    const m = marcador(raiz);
    const pista = el('div', { className: 'linea-pista' },
      icono('⬅️'), el('span', { text: 'Antes' }),
      el('span', { className: 'linea-flecha', attrs: { 'aria-hidden': 'true' } }),
      el('span', { text: 'Después' }), icono('➡️'));
    const fila = el('ol', { className: 'linea-tiempo' });

    function comprobar(){
      const ok = actual.every((s, i) => i === 0 || actual[i - 1].orden < s.orden);
      if(ok){
        m.decir('¡Perfecto! Están todos en orden, del más antiguo al más nuevo.', '🏆');
        hablar('¡Perfecto! Todos en orden.');
        fila.classList.add('resuelta');
      }else{
        m.decir('Coloca los sucesos del más antiguo al más nuevo usando las flechas.', '🕰️');
        fila.classList.remove('resuelta');
      }
    }

    function mover(i, delta){
      const j = i + delta;
      if(j < 0 || j >= actual.length) return;
      [actual[i], actual[j]] = [actual[j], actual[i]];
      pintar();
      // El foco sigue a la tarjeta movida, si no se pierde al repintar.
      const btn = fila.children[j].querySelector(delta < 0 ? '.mover-izq' : '.mover-der');
      btn && btn.focus();
      comprobar();
    }

    function pintar(){
      fila.replaceChildren(...actual.map((s, i) => {
        const izq = el('button', { className: 'mover mover-izq', text: '◀',
          attrs: { type: 'button', 'aria-label': `Mover ${s.nombre} hacia antes`, disabled: i === 0 || null } });
        const der = el('button', { className: 'mover mover-der', text: '▶',
          attrs: { type: 'button', 'aria-label': `Mover ${s.nombre} hacia después`, disabled: i === actual.length - 1 || null } });
        izq.addEventListener('click', () => mover(i, -1));
        der.addEventListener('click', () => mover(i, 1));

        const card = el('li', { className: 'suceso' },
          el('span', { className: 'suceso-emoji', text: s.emoji, attrs: { 'aria-hidden': 'true' } }),
          el('span', { className: 'suceso-nombre', text: s.nombre }),
          el('div', { className: 'suceso-controles' }, izq, der));
        card.addEventListener('click', ev => {
          if(!ev.target.closest('.mover')) hablar(s.nombre);
        });
        return card;
      }));
    }

    raiz.append(pista, fila);
    pintar();
    comprobar();
  }

  /* ======================================================================
     4. MEMORY IN ENGLISH — parejas de vocabulario (Idiomas)
     ====================================================================== */
  const VOCABULARIO = [
    { emoji: '🐶', en: 'DOG',    es: 'Perro' },
    { emoji: '🐱', en: 'CAT',    es: 'Gato' },
    { emoji: '🐷', en: 'PIG',    es: 'Cerdo' },
    { emoji: '🐦', en: 'BIRD',   es: 'Pájaro' },
    { emoji: '🐟', en: 'FISH',   es: 'Pez' },
    { emoji: '🐴', en: 'HORSE',  es: 'Caballo' },
    { emoji: '🔴', en: 'RED',    es: 'Rojo' },
    { emoji: '🔵', en: 'BLUE',   es: 'Azul' },
    { emoji: '🟢', en: 'GREEN',  es: 'Verde' },
    { emoji: '🟡', en: 'YELLOW', es: 'Amarillo' },
    { emoji: '☀️', en: 'SUN',    es: 'Sol' },
    { emoji: '🏠', en: 'HOUSE',  es: 'Casa' },
  ];

  function memoryInEnglish(raiz, curso){
    const nParejas = nivel(curso).parejas;
    const m = marcador(raiz);
    const tablero = el('div', { className: 'tablero tablero-memory' });
    let primera = null, bloqueado = false, encontradas = 0, intentos = 0;

    function nuevaPartida(){
      encontradas = 0; intentos = 0; primera = null; bloqueado = false;
      const elegidas = barajar(VOCABULARIO).slice(0, nParejas);
      const cartas = barajar(elegidas.flatMap(v => [
        { ...v, cara: 'emoji' }, { ...v, cara: 'texto' },
      ]));
      m.decir(`Encuentra las ${nParejas} parejas: dibujo y palabra en inglés.`, '🌍');

      tablero.replaceChildren(...cartas.map(c => {
        const btn = el('button', { className: 'carta',
          attrs: { type: 'button', 'aria-label': 'Carta boca abajo' } });
        btn.dataset.en = c.en;
        btn.dataset.cara = c.cara;
        btn.append(el('span', { className: 'carta-dorso', text: '❓', attrs: { 'aria-hidden': 'true' } }),
                   el('span', { className: 'carta-frente', text: c.cara === 'emoji' ? c.emoji : c.en }));
        btn.addEventListener('click', () => voltear(btn, c));
        return btn;
      }));
    }

    function voltear(btn, carta){
      if(bloqueado || btn.classList.contains('descubierta') || btn === primera) return;
      btn.classList.add('descubierta');
      btn.setAttribute('aria-label', carta.cara === 'emoji' ? carta.es : carta.en);
      hablar(carta.en, 'en-GB');

      if(!primera){ primera = btn; return; }

      intentos++;
      if(primera.dataset.en === btn.dataset.en){
        encontradas++;
        [primera, btn].forEach(b => { b.classList.add('emparejada'); b.disabled = true; });
        primera = null;
        if(encontradas === nParejas){
          m.decir(`¡Enhorabuena! Has encontrado las ${nParejas} parejas en ${intentos} intentos.`, '🏆');
          hablar('¡Enhorabuena! Lo has conseguido.');
        }else{
          m.decir(`¡Bien! ${carta.en} es ${carta.es}. Llevas ${encontradas} de ${nParejas}.`, '🎉');
        }
      }else{
        bloqueado = true;
        const anterior = primera;
        primera = null;
        m.decir('Esas dos no van juntas. ¡Vuelve a intentarlo!', '🤔');
        setTimeout(() => {
          [anterior, btn].forEach(b => {
            b.classList.remove('descubierta');
            b.setAttribute('aria-label', 'Carta boca abajo');
          });
          bloqueado = false;
        }, reduceMotion() ? 400 : 1100);
      }
    }

    const btnNueva = el('button', { className: 'btn btn-secondary', attrs: { type: 'button' } },
      icono('🔄'), 'Partida nueva');
    btnNueva.addEventListener('click', nuevaPartida);

    raiz.append(tablero, el('div', { className: 'juego-acciones' }, btnNueva));
    nuevaPartida();
  }

  return {
    catalogo: [
      { id: 'toca',    tema: 'matematicas', titulo: 'Toca y Descubre', icono: '🐾',
        descripcion: 'Pulsa un animal o un número: se mueve y te dice su nombre en voz alta.',
        montar: tocaYDescubre },
      { id: 'letra',   tema: 'lenguaje', titulo: 'La Letra Perdida', icono: '🔤',
        descripcion: 'Escucha la letra y elige el dibujo que empieza por ella.',
        montar: laLetraPerdida },
      { id: 'tiempo',  tema: 'historia', titulo: 'Línea del Tiempo', icono: '🕰️',
        descripcion: 'Ordena los sucesos del más antiguo al más nuevo.',
        montar: lineaDelTiempo },
      { id: 'memory',  tema: 'idiomas', titulo: 'Memory in English', icono: '🃏',
        descripcion: 'Encuentra las parejas de dibujo y palabra en inglés.',
        montar: memoryInEnglish },
    ],
  };
})();
