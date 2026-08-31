# -*- coding: utf-8 -*-
"""
Complementos: lleva cada ficha al minimo de 5 ejercicios.

El curriculo declara el NUCLEO de cada ficha (lo que le da su objetivo). Aqui se
anaden ejercicios alrededor, con una estructura pedagogica real y no de relleno:

    calentamiento  ->  NUCLEO declarado  ->  consolidacion

El calentamiento repasa algo ya sabido para entrar en calor; la consolidacion
aplica o extiende lo del nucleo. Cada entrada del banco lleva un rango de
dificultad de 1 a 5, y la ficha se ordena por ese rango, asi que dentro de una
misma ficha los primeros ejercicios son mas sencillos que los ultimos.

Cada celda (tema, curso) tiene su propio banco: un complemento de 7 anos no
puede aparecer en una ficha de 3 anos.
"""

from generar_fichas import (
    b_colorear, b_comparar, b_concepto, b_contar, b_descomponer, b_dobles,
    b_emparejar, b_formas, b_monedas, b_operaciones, b_problema, b_reloj,
    b_rodear, b_serie, b_tabla, b_tantos_como, b_trazo, b_unir, b_vecinos,
)
from bloques_texto import (
    b_clasificar, b_completar, b_dibujar, b_escritura, b_frase, b_lectura,
    b_ordenar, b_silabas, b_verdadero_falso, b_vocabulario,
)

MINIMO = 5


# ============================================================================
# BANCOS POR TEMA Y CURSO
# Cada entrada: (rango 1-5, constructor). Rango 1-2 sirve de calentamiento,
# 3-5 de consolidacion.
# ============================================================================

BANCO = {}

# ---------------------------------------------------------------- MATEMATICAS
BANCO[("matematicas", 2)] = [
    (1, lambda r: b_contar(r, 3, 3)),
    (1, lambda r: b_colorear(r, 3, 4)),
    (2, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_concepto(r, [("🐘", "grande"), ("🐭", "pequeño"), ("🦒", "grande")],
                             "Rodea lo que es GRANDE.")),
    (3, lambda r: b_formas(r, ["circulo", "cuadrado"])),
    (3, lambda r: b_trazo(r, ["1", "2", "3"], 4)),
    (4, lambda r: b_tantos_como(r, 3, 3)),
    (4, lambda r: b_concepto(r, [("🪣", "lleno"), ("🥛", "vacío"), ("🧺", "lleno")],
                             "Colorea lo que está LLENO.")),
]
BANCO[("matematicas", 3)] = [
    (1, lambda r: b_contar(r, 3, 5)),
    (1, lambda r: b_colorear(r, 3, 5)),
    (2, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_trazo(r, ["1", "2", "3", "4", "5"], 3)),
    (3, lambda r: b_comparar(r, 4, 5, True)),
    (3, lambda r: b_tantos_como(r, 3, 5)),
    (4, lambda r: b_formas(r, ["circulo", "cuadrado", "triangulo"])),
    (5, lambda r: b_unir(r, [("🍎🍎", "2"), ("⭐⭐⭐", "3"), ("🐸", "1"), ("🎈🎈🎈🎈", "4")],
                         "Une cada grupo con su número.")),
]
BANCO[("matematicas", 4)] = [
    (1, lambda r: b_contar(r, 3, 10)),
    (1, lambda r: b_trazo(r, ["6", "7", "8", "9", "10"], 3)),
    (2, lambda r: b_colorear(r, 3, 8)),
    (2, lambda r: b_comparar(r, 5, 9)),
    (3, lambda r: b_vecinos(r, 4, 10)),
    (3, lambda r: b_operaciones(r, "+", 6, 8)),
    (4, lambda r: b_rodear(r, 4, 10, "mayor")),
    (5, lambda r: b_descomponer(r, 5, 4)),
]
BANCO[("matematicas", 5)] = [
    (1, lambda r: b_contar(r, 3, 10)),
    (1, lambda r: b_vecinos(r, 5, 15)),
    (2, lambda r: b_comparar(r, 6, 15)),
    (2, lambda r: b_operaciones(r, "+", 6, 12)),
    (3, lambda r: b_operaciones(r, "-", 6, 12)),
    (3, lambda r: b_serie(r, 2, 2, 10, 6)),
    (4, lambda r: b_descomponer(r, 10, 5)),
    (5, lambda r: b_problema(r, "+", 2, 15)),
]
BANCO[("matematicas", 6)] = [
    (1, lambda r: b_vecinos(r, 6, 50)),
    (1, lambda r: b_comparar(r, 8, 50)),
    (2, lambda r: b_serie(r, 3, 5, 20, 6)),
    (2, lambda r: b_operaciones(r, "+", 8, 40, "vertical", llevando=False)),
    (3, lambda r: b_operaciones(r, "-", 8, 40, "vertical", llevando=False)),
    (3, lambda r: b_dobles(r, 6, 20)),
    (4, lambda r: b_monedas(r, 4)),
    (5, lambda r: b_problema(r, "-", 2, 40)),
]
BANCO[("matematicas", 7)] = [
    (1, lambda r: b_vecinos(r, 6, 200)),
    (1, lambda r: b_comparar(r, 8, 300)),
    (2, lambda r: b_operaciones(r, "+", 8, 99, "vertical", llevando=True)),
    (2, lambda r: b_serie(r, 3, 10, 100, 6)),
    (3, lambda r: b_operaciones(r, "-", 8, 99, "vertical")),
    (3, lambda r: b_operaciones(r, "x", 8, 5)),
    (4, lambda r: b_reloj(r, 4, "y media")),
    (5, lambda r: b_problema(r, "+", 2, 100)),
]

# ------------------------------------------------------------------ LENGUAJE
BANCO[("lenguaje", 2)] = [
    (1, lambda r: b_trazo(r, ["|", "—", "∿"], 5, "Repasa cada trazo sin levantar la cera.")),
    (1, lambda r: b_colorear(r, 3, 4)),
    (2, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_concepto(r, [("🐘", "grande"), ("🐭", "pequeño"), ("🌳", "grande")],
                             "Di en voz alta si es GRANDE o PEQUEÑO.")),
    (3, lambda r: b_trazo(r, ["A", "E", "I"], 4)),
    (3, lambda r: b_contar(r, 3, 3)),
    (4, lambda r: b_trazo(r, ["O", "U"], 5)),
    (5, lambda r: b_dibujar(r, "Dibuja algo que empiece por la letra que has repasado.",
                            "Mi dibujo", "mediano")),
]
BANCO[("lenguaje", 3)] = [
    (1, lambda r: b_trazo(r, ["A", "E", "I", "O", "U"], 3)),
    (1, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_unir(r, [("A", "a"), ("E", "e"), ("I", "i"), ("O", "o"), ("U", "u")],
                         "Une cada letra grande con su letra pequeña.")),
    (2, lambda r: b_colorear(r, 3, 5)),
    (3, lambda r: b_clasificar(r, ["Empieza por A", "No empieza por A"],
                               [("🕷️ Araña", 0), ("🌳 Árbol", 0), ("🐶 Perro", 1),
                                ("🌊 Agua", 0), ("🐱 Gato", 1), ("🌙 Luna", 1)])),
    (3, lambda r: b_silabas(r, [("☀️", "SOL"), ("🐱", "GATO")])),
    (4, lambda r: b_escritura(r, [("👩", "MAMÁ"), ("🌙", "LUNA")])),
    (5, lambda r: b_dibujar(r, "Dibuja algo que empiece por la letra de esta ficha.",
                            "Mi dibujo", "mediano")),
]
BANCO[("lenguaje", 4)] = [
    (1, lambda r: b_trazo(r, ["A", "E", "I", "O", "U"], 3)),
    (1, lambda r: b_unir(r, [("☀️", "SOL"), ("🌙", "LUNA"), ("🏠", "CASA"), ("🐱", "GATO")],
                         "Une cada dibujo con su palabra.")),
    (2, lambda r: b_silabas(r, [("🐱", "GATO"), ("🏠", "CASA"), ("🌸", "FLOR")])),
    (2, lambda r: b_clasificar(r, ["Animales", "Comida"],
                               [("🐶", 0), ("🍎", 1), ("🐱", 0), ("🍌", 1), ("🐰", 0), ("🍇", 1)])),
    (3, lambda r: b_escritura(r, [("☀️", "SOL"), ("🐱", "GATO")])),
    (3, lambda r: b_completar(r, [("☀️", "SOL", 1), ("🌙", "LUNA", 2), ("🏠", "CASA", 3)])),
    (4, lambda r: b_clasificar(r, ["1 sílaba", "2 sílabas", "3 sílabas"],
                               [("SOL", 0), ("GATO", 1), ("PELOTA", 2),
                                ("PAN", 0), ("CASA", 1), ("CAMISETA", 2)])),
    (5, lambda r: b_ordenar(r, [("EL", 1), ("GATO", 2), ("DUERME", 3)])),
]
BANCO[("lenguaje", 5)] = [
    (1, lambda r: b_silabas(r, [("🏠", "CASA"), ("🌙", "LUNA"), ("🐱", "GATO")])),
    (1, lambda r: b_unir(r, [("GATO", "GATOS"), ("FLOR", "FLORES"),
                             ("CASA", "CASAS"), ("PAN", "PANES")],
                         "Une cada palabra con su plural.")),
    (2, lambda r: b_completar(r, [("🦋", "MARIPOSA", 3), ("🍅", "TOMATE", 2), ("🚗", "COCHE", 1)])),
    (2, lambda r: b_escritura(r, [("🌸", "FLOR"), ("🐦", "PÁJARO")])),
    (3, lambda r: b_clasificar(r, ["Personas", "Animales", "Cosas"],
                               [("MAMÁ", 0), ("PERRO", 1), ("SILLA", 2),
                                ("NIÑO", 0), ("GATO", 1), ("MESA", 2)])),
    (3, lambda r: b_ordenar(r, [("MI", 1), ("PERRO", 2), ("COME", 3), ("PAN", 4)])),
    (4, lambda r: b_unir(r, [("GATO", "PATO"), ("RATÓN", "BOTÓN"),
                             ("FLOR", "COLOR"), ("PAN", "IMÁN")],
                         "Une las palabras que riman.")),
    (5, lambda r: b_lectura(r, "El perro de Ana es marrón y duerme debajo de la mesa.",
                            [("¿De quién es el perro?", "De Ana"),
                             ("¿De qué color es?", "Marrón"),
                             ("¿Dónde duerme?", "Debajo de la mesa")])),
]
BANCO[("lenguaje", 6)] = [
    (1, lambda r: b_silabas(r, [("🦋", "MARIPOSA"), ("🏫", "ESCUELA")])),
    (1, lambda r: b_unir(r, [("EL", "PERRO"), ("LA", "CASA"), ("LOS", "NIÑOS"), ("LAS", "FLORES")],
                         "Une cada artículo con su nombre.")),
    (2, lambda r: b_completar(r, [("🐴", "CABALLO", 3), ("🥁", "TAMBOR", 2), ("🦒", "JIRAFA", 0)])),
    (2, lambda r: b_clasificar(r, ["Se escribe con B", "Se escribe con V"],
                               [("BARCO", 0), ("VACA", 1), ("BOCA", 0),
                                ("VENTANA", 1), ("BOTA", 0), ("VERDE", 1)])),
    (3, lambda r: b_unir(r, [("ALTO", "BAJO"), ("FRÍO", "CALIENTE"),
                             ("DÍA", "NOCHE"), ("ABRIR", "CERRAR")],
                         "Une cada palabra con su contraria.")),
    (3, lambda r: b_ordenar(r, [("Ana se despierta.", 1), ("Desayuna.", 2),
                                ("Va al colegio.", 3), ("Vuelve a casa.", 4)])),
    (4, lambda r: b_verdadero_falso(r, [("Las frases empiezan por mayúscula.", True),
                                        ("Los nombres propios van en minúscula.", False),
                                        ("Las frases terminan en punto.", True)])),
    (5, lambda r: b_lectura(r, "El sábado fuimos al parque. Había tres columpios y un tobogán "
                               "muy alto. Merendamos un bocadillo de queso.",
                            [("¿Qué día fueron al parque?", "El sábado"),
                             ("¿Cuántos columpios había?", "Tres"),
                             ("¿Qué merendaron?", "Un bocadillo de queso")])),
]
BANCO[("lenguaje", 7)] = [
    (1, lambda r: b_silabas(r, [("📱", "TELÉFONO"), ("🎵", "MÚSICA")],
                            "Separa en sílabas y rodea la sílaba tónica.")),
    (1, lambda r: b_clasificar(r, ["Sustantivo", "Adjetivo", "Verbo"],
                               [("PERRO", 0), ("BONITO", 1), ("CORRER", 2),
                                ("CASA", 0), ("ALTO", 1), ("SALTAR", 2)])),
    (2, lambda r: b_completar(r, [("🎂", "CUMPLEAÑOS", 6), ("📚", "BIBLIOTECA", 3),
                                  ("🥪", "BOCADILLO", 4)])),
    (2, lambda r: b_unir(r, [("CASA", "VIVIENDA"), ("COCHE", "AUTOMÓVIL"),
                             ("PROFESOR", "MAESTRO"), ("CONTENTO", "ALEGRE")],
                         "Une cada palabra con su sinónimo.")),
    (3, lambda r: b_clasificar(r, ["Aguda", "Llana", "Esdrújula"],
                               [("SOFÁ", 0), ("LÁPIZ", 1), ("MÚSICA", 2),
                                ("RATÓN", 0), ("MESA", 1), ("PÁJARO", 2)])),
    (3, lambda r: b_verdadero_falso(r, [
        ("Las agudas llevan tilde si acaban en vocal, N o S.", True),
        ("«Reloj» lleva tilde.", False),
        ("«Camión» lleva tilde porque acaba en N.", True)])),
    (4, lambda r: b_ordenar(r, [("Un día encontró un mapa antiguo.", 1),
                                ("Lo siguió hasta la playa.", 2),
                                ("Cavó en la arena.", 3),
                                ("Encontró un cofre lleno de conchas.", 4)])),
    (5, lambda r: b_lectura(r, "Las abejas viven en colmenas y fabrican miel con el néctar de "
                               "las flores. Al ir de flor en flor transportan el polen, y gracias "
                               "a eso nacen frutos nuevos.",
                            [("¿Dónde viven las abejas?", "En colmenas"),
                             ("¿Con qué fabrican la miel?", "Con el néctar de las flores"),
                             ("¿Por qué son importantes?", "Transportan el polen")])),
]

# ------------------------------------------------------------------ HISTORIA
BANCO[("historia", 2)] = [
    (1, lambda r: b_concepto(r, [("☀️", "de día"), ("🌙", "de noche"), ("⭐", "de noche")],
                             "Colorea lo del DÍA de amarillo y lo de la NOCHE de azul.")),
    (1, lambda r: b_colorear(r, 3, 4)),
    (2, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_ordenar(r, [("🥚 Huevo", 1), ("🐥 Pollito", 2)],
                            "Numera con 1 lo de ANTES y con 2 lo de DESPUÉS.")),
    (3, lambda r: b_concepto(r, [("👶", "bebé"), ("🧒", "mayor"), ("🍼", "bebé")],
                             "Rodea lo que usa un BEBÉ.")),
    (3, lambda r: b_contar(r, 3, 3)),
    (4, lambda r: b_ordenar(r, [("🛏️ Me levanto", 1), ("🥣 Desayuno", 2), ("🏫 Voy al cole", 3)])),
    (5, lambda r: b_dibujar(r, "Dibuja algo de lo que has aprendido en esta ficha.",
                            "Mi dibujo", "mediano")),
]
BANCO[("historia", 3)] = [
    (1, lambda r: b_clasificar(r, ["De día", "De noche"],
                               [("☀️ Sol", 0), ("🌙 Luna", 1), ("🏫 Colegio", 0),
                                ("😴 Dormir", 1), ("🍽️ Comer", 0), ("⭐ Estrellas", 1)])),
    (1, lambda r: b_colorear(r, 3, 5)),
    (2, lambda r: b_ordenar(r, [("Ayer", 1), ("Hoy", 2), ("Mañana", 3)])),
    (2, lambda r: b_unir(r, [("Primavera", "🌸"), ("Verano", "🏖️"),
                             ("Otoño", "🍂"), ("Invierno", "❄️")],
                         "Une cada estación con su dibujo.")),
    (3, lambda r: b_clasificar(r, ["De antes", "De ahora"],
                               [("🕯️ Vela", 0), ("💡 Bombilla", 1), ("🐴 Caballo", 0),
                                ("🚗 Coche", 1), ("🛶 Barca", 0), ("✈️ Avión", 1)])),
    (3, lambda r: b_ordenar(r, [("👶 Bebé", 1), ("🧒 Niño", 2), ("🧑 Adulto", 3), ("🧓 Abuelo", 4)])),
    (4, lambda r: b_unir(r, [("🧑‍🚒 Bombero", "🔥"), ("👩‍⚕️ Médica", "🩺"),
                             ("👨‍🍳 Cocinero", "🍳"), ("👩‍🏫 Maestra", "📚")],
                         "Une cada oficio con lo que usa.")),
    (5, lambda r: b_dibujar(r, "Dibuja cómo te imaginas la escena de esta ficha.",
                            "Mi dibujo", "mediano")),
]
BANCO[("historia", 4)] = [
    (1, lambda r: b_clasificar(r, ["Ya no existen", "Existen hoy"],
                               [("🦕 Dinosaurio", 0), ("🐘 Elefante", 1), ("🦣 Mamut", 0),
                                ("🐅 Tigre", 1), ("🦖 T-Rex", 0), ("🐄 Vaca", 1)])),
    (1, lambda r: b_ordenar(r, [("🦕 Dinosaurios", 1), ("🔥 Prehistoria", 2),
                                ("🏜️ Egipto", 3), ("🚗 Hoy", 4)])),
    (2, lambda r: b_clasificar(r, ["Herbívoro", "Carnívoro"],
                               [("Diplodocus", 0), ("Tiranosaurio", 1), ("Triceratops", 0),
                                ("Velociraptor", 1)])),
    (2, lambda r: b_unir(r, [("🕳️ Cueva", "Prehistoria"), ("🏜️ Pirámide", "Egipto"),
                             ("🏢 Edificio", "Hoy")],
                         "Une cada construcción con su época.")),
    (3, lambda r: b_verdadero_falso(r, [
        ("Los dinosaurios vivieron antes que las personas.", True),
        ("Las pirámides las construyeron los dinosaurios.", False),
        ("Los fósiles nos ayudan a conocer el pasado.", True)])),
    (3, lambda r: b_ordenar(r, [("🚶 A pie", 1), ("🐴 A caballo", 2),
                                ("🚂 En tren", 3), ("✈️ En avión", 4)])),
    (4, lambda r: b_lectura(r, "Los arqueólogos excavan la tierra con mucho cuidado para "
                               "encontrar restos antiguos y saber cómo vivía la gente.",
                            [("¿Qué hacen los arqueólogos?", "Excavan para encontrar restos"),
                             ("¿Para qué sirve?", "Para saber cómo vivía la gente")])),
    (5, lambda r: b_dibujar(r, "Dibuja una escena de la época que has estudiado en esta ficha.",
                            "Mi escena", "mediano")),
]
BANCO[("historia", 5)] = [
    (1, lambda r: b_ordenar(r, [("🔥 Prehistoria", 1), ("🏜️ Egipto", 2),
                                ("🏛️ Roma", 3), ("🏰 Edad Media", 4)])),
    (1, lambda r: b_clasificar(r, ["Egipto", "Roma"],
                               [("Pirámides", 0), ("Coliseo", 1), ("Faraón", 0),
                                ("Acueducto", 1), ("Jeroglíficos", 0), ("Calzada", 1)])),
    (2, lambda r: b_verdadero_falso(r, [
        ("Las pirámides eran tumbas de los faraones.", True),
        ("Los romanos construyeron acueductos.", True),
        ("En la Edad Media había aviones.", False)])),
    (2, lambda r: b_unir(r, [("Torre", "La parte más alta"), ("Muralla", "El muro que rodea"),
                             ("Foso", "El agua alrededor")],
                         "Une cada parte del castillo con lo que es.")),
    (3, lambda r: b_lectura(r, "Los egipcios escribían con jeroglíficos sobre papiros, hechos "
                               "con una planta que crecía a orillas del Nilo.",
                            [("¿Cómo se llamaba su escritura?", "Jeroglíficos"),
                             ("¿Sobre qué escribían?", "Sobre papiros"),
                             ("¿De dónde salía el papiro?", "De una planta del Nilo")])),
    (3, lambda r: b_ordenar(r, [("Preparaban el cuerpo.", 1), ("Lo envolvían con vendas.", 2),
                                ("Lo metían en un sarcófago.", 3)],
                            "Numera los pasos para hacer una momia.")),
    (4, lambda r: b_unir(r, [("La rueda", "Mover cosas pesadas"),
                             ("La imprenta", "Hacer muchos libros"),
                             ("La bombilla", "Tener luz de noche")],
                         "Une cada invento con para qué sirve.")),
    (5, lambda r: b_dibujar(r, "Dibuja lo que más te ha llamado la atención de esta ficha "
                               "y escribe una frase explicándolo.", "Mi dibujo", "mediano")),
]
BANCO[("historia", 6)] = [
    (1, lambda r: b_ordenar(r, [("Prehistoria", 1), ("Edad Antigua", 2), ("Edad Media", 3),
                                ("Edad Moderna", 4), ("Edad Contemporánea", 5)])),
    (1, lambda r: b_unir(r, [("I", "1"), ("V", "5"), ("X", "10"), ("L", "50"), ("C", "100")],
                         "Une cada número romano con su valor.")),
    (2, lambda r: b_clasificar(r, ["Paleolítico", "Neolítico"],
                               [("Cazar y recolectar", 0), ("Cultivar la tierra", 1),
                                ("Ser nómada", 0), ("Vivir en poblados", 1)])),
    (2, lambda r: b_verdadero_falso(r, [
        ("Un siglo son cien años.", True),
        ("La Historia empieza con la escritura.", True),
        ("La democracia nació en Roma.", False)])),
    (3, lambda r: b_clasificar(r, ["Fuente escrita", "Fuente material"],
                               [("Un libro antiguo", 0), ("Una vasija", 1), ("Una carta", 0),
                                ("Una moneda", 1)])),
    (3, lambda r: b_ordenar(r, [("Se construyen las pirámides", 1),
                                ("Nace la democracia en Atenas", 2),
                                ("Cae el Imperio Romano", 3),
                                ("Colón llega a América", 4)])),
    (4, lambda r: b_lectura(r, "En la Edad Media los reyes daban tierras a los nobles a cambio "
                               "de ayuda en la guerra. Los campesinos trabajaban esas tierras y "
                               "entregaban parte de la cosecha al señor.",
                            [("¿Qué daban los reyes a los nobles?", "Tierras"),
                             ("¿Qué recibían a cambio?", "Ayuda en la guerra"),
                             ("¿Qué entregaban los campesinos?", "Parte de la cosecha")])),
    (5, lambda r: b_dibujar(r, "Haz una línea del tiempo con cuatro hechos de esta ficha, "
                               "del más antiguo al más nuevo.", "Mi línea del tiempo", "mediano")),
]
BANCO[("historia", 7)] = [
    (1, lambda r: b_unir(r, [("1492", "Siglo XV"), ("1789", "Siglo XVIII"),
                             ("1969", "Siglo XX"), ("2020", "Siglo XXI")],
                         "Une cada año con su siglo.")),
    (1, lambda r: b_ordenar(r, [("Prehistoria", 1), ("Edad Antigua", 2), ("Edad Media", 3),
                                ("Edad Moderna", 4), ("Edad Contemporánea", 5)])),
    (2, lambda r: b_clasificar(r, ["Atenas", "Esparta"],
                               [("La democracia", 0), ("El ejército", 1),
                                ("La filosofía", 0), ("El entrenamiento militar", 1)])),
    (2, lambda r: b_verdadero_falso(r, [
        ("El Imperio Romano de Occidente cayó en el año 476.", True),
        ("«a. C.» significa antes de Cristo.", True),
        ("Los romanos inventaron la imprenta.", False)])),
    (3, lambda r: b_clasificar(r, ["Fuente primaria", "Fuente secundaria"],
                               [("Una carta de la época", 0), ("Un libro de texto de hoy", 1),
                                ("Una moneda romana", 0), ("Un documental actual", 1)])),
    (3, lambda r: b_unir(r, [("Se inventa la agricultura", "La gente deja de ser nómada"),
                             ("Se inventa la imprenta", "Los libros se abaratan"),
                             ("Se inventa la máquina de vapor", "Nacen las fábricas")],
                         "Une cada causa con su consecuencia.")),
    (4, lambda r: b_lectura(r, "En Mesopotamia, entre los ríos Tigris y Éufrates, se inventó la "
                               "escritura cuneiforme hacia el 3300 a. C. Escribían sobre tablillas "
                               "de barro con una caña, y con la escritura empieza la Historia.",
                            [("¿Entre qué ríos estaba Mesopotamia?", "El Tigris y el Éufrates"),
                             ("¿Cómo se llamaba su escritura?", "Cuneiforme"),
                             ("¿Qué empieza con la escritura?", "La Historia")])),
    (5, lambda r: b_dibujar(r, "Explica con tus palabras, en cuatro o cinco líneas, lo más "
                               "importante de esta ficha.", "Mi resumen", "mediano")),
]

# ------------------------------------------------------------------- IDIOMAS
BANCO[("idiomas", 2)] = [
    (1, lambda r: b_vocabulario(r, [("👋", "HELLO", "Hola")])),
    (1, lambda r: b_colorear(r, 3, 4)),
    (2, lambda r: b_emparejar(r, 3)),
    (2, lambda r: b_vocabulario(r, [("🐶", "DOG", "Perro"), ("🐱", "CAT", "Gato")])),
    (3, lambda r: b_unir(r, [("🐶", "DOG"), ("🐱", "CAT"), ("☀️", "SUN")],
                         "Une cada dibujo con su palabra en inglés.")),
    (3, lambda r: b_contar(r, 3, 3)),
    (4, lambda r: b_colorear_seguro(r)),
    (5, lambda r: b_vocabulario(r, [("👋", "BYE", "Adiós")])),
]
BANCO[("idiomas", 3)] = [
    (1, lambda r: b_vocabulario(r, [("🔴", "RED", "Rojo"), ("🔵", "BLUE", "Azul")])),
    (1, lambda r: b_contar(r, 3, 5)),
    (2, lambda r: b_unir(r, [("1", "ONE"), ("2", "TWO"), ("3", "THREE"),
                             ("4", "FOUR"), ("5", "FIVE")],
                         "Une cada número con su palabra en inglés.")),
    (2, lambda r: b_emparejar(r, 3)),
    (3, lambda r: b_unir(r, [("🐮", "COW"), ("🐷", "PIG"), ("🐔", "HEN"), ("🐴", "HORSE")],
                         "Une cada animal con su nombre en inglés.")),
    (3, lambda r: b_clasificar(r, ["ANIMALS", "FRUIT"],
                               [("DOG", 0), ("APPLE", 1), ("CAT", 0), ("BANANA", 1)])),
    (4, lambda r: b_vocabulario(r, [("☀️", "SUN", "Sol"), ("🌙", "MOON", "Luna")])),
    (5, lambda r: b_unir(r, [("🍎", "APPLE"), ("🍌", "BANANA"), ("🍇", "GRAPES")],
                         "Une cada fruta con su nombre en inglés.")),
]
BANCO[("idiomas", 4)] = [
    (1, lambda r: b_unir(r, [("6", "SIX"), ("7", "SEVEN"), ("8", "EIGHT"),
                             ("9", "NINE"), ("10", "TEN")],
                         "Une cada número con su palabra en inglés.")),
    (1, lambda r: b_vocabulario(r, [("👁️", "EYE", "Ojo"), ("👃", "NOSE", "Nariz")])),
    (2, lambda r: b_unir(r, [("🚪", "DOOR"), ("🪟", "WINDOW"), ("🛏️", "BED"), ("🪑", "CHAIR")],
                         "Une cada objeto con su nombre en inglés.")),
    (2, lambda r: b_clasificar(r, ["FOOD", "CLOTHES"],
                               [("BREAD", 0), ("SHOES", 1), ("MILK", 0), ("T-SHIRT", 1)])),
    (3, lambda r: b_completar(r, [("🐶", "DOG", 1), ("☀️", "SUN", 2), ("🐟", "FISH", 1)])),
    (3, lambda r: b_escritura(r, [("🐶", "DOG"), ("☀️", "SUN")],
                              "Trace and write. Repasa y escribe.")),
    (4, lambda r: b_verdadero_falso(r, [("A DOG is an animal.", True),
                                        ("An APPLE is a colour.", False),
                                        ("BLUE is a colour.", True)])),
    (5, lambda r: b_vocabulario(r, [("☀️", "SUNNY", "Soleado"), ("🌧️", "RAINY", "Lluvioso")])),
]
BANCO[("idiomas", 5)] = [
    (1, lambda r: b_unir(r, [("MONDAY", "Lunes"), ("TUESDAY", "Martes"),
                             ("FRIDAY", "Viernes"), ("SUNDAY", "Domingo")],
                         "Une cada día con su significado.")),
    (1, lambda r: b_vocabulario(r, [("🦵", "LEG", "Pierna"), ("💪", "ARM", "Brazo")])),
    (2, lambda r: b_frase(r, [("MY NAME ", "IS", " ANNA."), ("I ", "LIKE", " CHOCOLATE.")])),
    (2, lambda r: b_clasificar(r, ["A", "AN"],
                               [("DOG", 0), ("APPLE", 1), ("CAT", 0), ("ORANGE", 1)])),
    (3, lambda r: b_unir(r, [("IN", "Dentro"), ("ON", "Encima"),
                             ("UNDER", "Debajo"), ("NEXT TO", "Al lado")],
                         "Une cada preposición con su significado.")),
    (3, lambda r: b_completar(r, [("🏫", "SCHOOL", 2), ("🥛", "MILK", 3), ("🪟", "WINDOW", 4)])),
    (4, lambda r: b_verdadero_falso(r, [("MONDAY is a day of the week.", True),
                                        ("GREEN is a number.", False),
                                        ("A TEACHER works at school.", True)])),
    (5, lambda r: b_escritura(r, [("🏫", "SCHOOL"), ("👩‍🏫", "TEACHER")],
                              "Trace and write. Repasa y escribe.")),
]
BANCO[("idiomas", 6)] = [
    (1, lambda r: b_unir(r, [("I", "AM"), ("YOU", "ARE"), ("HE / SHE / IT", "IS")],
                         "Une cada pronombre con su forma de TO BE.")),
    (1, lambda r: b_unir(r, [("30", "THIRTY"), ("40", "FORTY"), ("50", "FIFTY")],
                         "Une cada número con su palabra en inglés.")),
    (2, lambda r: b_frase(r, [("I ", "AM", " a pupil."), ("THERE ", "ARE", " five books.")])),
    (2, lambda r: b_unir(r, [("CAT", "CATS"), ("BOX", "BOXES"), ("DOG", "DOGS")],
                         "Une cada palabra con su plural.")),
    (3, lambda r: b_clasificar(r, ["CAN FLY", "CAN'T FLY"],
                               [("BIRD", 0), ("DOG", 1), ("BUTTERFLY", 0), ("FISH", 1)])),
    (3, lambda r: b_unir(r, [("BIG", "Grande"), ("HAPPY", "Contento"),
                             ("TIRED", "Cansado"), ("HUNGRY", "Hambriento")],
                         "Une cada adjetivo con su significado.")),
    (4, lambda r: b_ordenar(r, [("I wake up.", 1), ("I have breakfast.", 2),
                                ("I go to school.", 3), ("I go to bed.", 4)])),
    (5, lambda r: b_lectura(r, "My name is Sam. I am seven years old. I go to school every day "
                               "and my favourite subject is Art.",
                            [("What is his name?", "Sam"),
                             ("How old is he?", "Seven"),
                             ("What is his favourite subject?", "Art")])),
]
BANCO[("idiomas", 7)] = [
    (1, lambda r: b_unir(r, [("WHAT", "Qué"), ("WHERE", "Dónde"),
                             ("WHEN", "Cuándo"), ("WHO", "Quién")],
                         "Une cada palabra interrogativa con su significado.")),
    (1, lambda r: b_frase(r, [("I ", "PLAY", " football."), ("She ", "PLAYS", " the piano.")])),
    (2, lambda r: b_unir(r, [("GO", "WENT"), ("EAT", "ATE"), ("SEE", "SAW"), ("HAVE", "HAD")],
                         "Une cada verbo con su pasado.")),
    (2, lambda r: b_frase(r, [("I ", "DON'T", " like onions."), ("He ", "DOESN'T", " play tennis.")])),
    (3, lambda r: b_clasificar(r, ["IN", "ON", "AT"],
                               [("summer", 0), ("Monday", 1), ("3 o'clock", 2),
                                ("January", 0), ("my birthday", 1)])),
    (3, lambda r: b_unir(r, [("BIG", "BIGGER"), ("SMALL", "SMALLER"),
                             ("FAST", "FASTER"), ("GOOD", "BETTER")],
                         "Une cada adjetivo con su comparativo.")),
    (4, lambda r: b_unir(r, [("3:00", "THREE O'CLOCK"), ("4:15", "QUARTER PAST FOUR"),
                             ("5:30", "HALF PAST FIVE")],
                         "Une cada hora con su forma en inglés.")),
    (5, lambda r: b_lectura(r, "At our school we have a recycling club. Every Friday we collect "
                               "paper and plastic. Last month we planted two trees.",
                            [("When does the club meet?", "Every Friday"),
                             ("What do they collect?", "Paper and plastic"),
                             ("What did they plant?", "Two trees")])),
]


def b_colorear_seguro(r):
    """Mancha para colorear con su nombre en ingles (evita import circular)."""
    from bloques_texto import b_colorear_ingles
    return b_colorear_ingles(r, [("circulo", "RED", "rojo"), ("cuadrado", "BLUE", "azul")])


# ============================================================================
# COMPOSICION
# ============================================================================

def completar(r, tema, curso, nucleo):
    """
    Devuelve la lista final de bloques de una ficha, con al menos MINIMO
    ejercicios y ordenada de menor a mayor dificultad.

    El nucleo declarado en el curriculo se conserva intacto y se le asigna un
    rango medio (3), de modo que los calentamientos quedan delante y las
    consolidaciones detras.
    """
    banco = BANCO.get((tema, curso), [])
    faltan = MINIMO - len(nucleo)
    if faltan <= 0 or not banco:
        return nucleo

    tipos_nucleo = {b["tipo"] for b in nucleo}

    # Se prefieren complementos de un tipo que la ficha no tenga ya: repetir
    # cuatro veces el mismo ejercicio seria relleno, no practica.
    frescos = [e for e in banco if True]
    r.shuffle(frescos)

    elegidos, tipos_usados = [], set(tipos_nucleo)
    # Primera pasada: solo tipos nuevos. Segunda: se permite repetir.
    for permitir_repetir in (False, True):
        for rango, constructor in frescos:
            if len(elegidos) >= faltan:
                break
            bloque = constructor(r)
            if not permitir_repetir and bloque["tipo"] in tipos_usados:
                continue
            elegidos.append((rango, bloque))
            tipos_usados.add(bloque["tipo"])
        if len(elegidos) >= faltan:
            break

    # Orden final: calentamiento -> nucleo -> consolidacion.
    #
    # El nucleo va en la posicion 3. Un complemento de rango 3 empataria con el
    # y, al desempatar por indice, acabaria DELANTE: la ficha empezaria por la
    # consolidacion. Por eso a los complementos de rango >= 3 se les suma medio
    # punto, y asi caen siempre detras del nucleo.
    CALENTAMIENTO = 2

    marcados = []
    for i, (rango, b) in enumerate(elegidos):
        posicion = rango if rango <= CALENTAMIENTO else rango + 0.5
        marcados.append((posicion, i, b))
    # `enumerate` con desplazamiento mantiene estable el orden que el curriculo
    # dio al nucleo.
    marcados += [(3, 100 + i, b) for i, b in enumerate(nucleo)]

    marcados.sort(key=lambda x: (x[0], x[1]))
    return [b for _, _, b in marcados]
