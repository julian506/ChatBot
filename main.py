# INTEGRANTES:
# Julián Pachón Castrillón y Paula Andrea Taborda Montes
import random
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import os

def limpiarPantalla():
    os.system('cls' if os.name=='nt' else 'clear')

nltk.download('stopwords')

nombre = ""

prefijos = ["¡Que buena pregunta! ", "¡Excelente pregunta! ", "¡Me encanta responder esto! ", "¡Wow me encanta que preguntes esto! ", "¡Genial tu pregunta! "]

errores = ["Lo siento, no te entendí :(", "No entendí tu pregunta, ¿Podrías reformularla?", "Creo que no entiendo a qué te refieres"]

despedidas = ["¡Espero haber sido de utilidad!", "¡Que te vaya super bien!", "¡Muchas gracias por usarme!", "¡Espero que vuelvas pronto!", "¡Gracias por tu visita!", "¡Quiero seguir hablando contigo!"]

reflections = {
	"i am": "you are",
	"i was": "you were",
	"i": "you",
	"i'm": "you are",
	"i'd": "you would",
	"i've": "you have",
	"i'll": "you will",
	"my": "your",
	"you are": "I am",
	"you were": "I was",
	"you've": "I have",
	"you'll": "I will",
	"your": "my",
	"yours": "mine",
	"you": "me",
	"me": "you",
}

def limpiarEntrada(entrada):
	#Colocamos la entrada en minúsculas
	entrada = entrada.lower()
	#Definimos un diccionario para el cambio de las
	#vocales con tílde, a aquellas sin tílde
	reemplazos = {
		"á": "a",
		"é": "e",
		"í": "i",
		"ó": "o",
		"ú": "u",
	}

	simbolos = ["?", "¿", "¡", "!", ".", ",", "}", "{", "-"]
	tokens = list(entrada) # Usamos el list para dividir la instrucción. No usamos el word_tokenize porque no separa símbolos únicos del español como el ¿. Preferimos usar una lista
	# print(tokens)
	# input()

	# En este ciclo eliminamos todos los símbolos que puedan aparecer en la instrucción del usuario
	for simbolo in simbolos:
		if simbolo in tokens:
			while simbolo in tokens:
				tokens.remove(simbolo)

	stop_words = stopwords.words('spanish') # Importamos los stop words del idioma español
	stop_words.append("cuál")
	stop_words.append("cuáles")
	stop_words.append("cómo")
	stop_words.append("muéstrame")
	# print(stop_words)

	cadena = "".join(tokens) # Unimos la cadena que llevo hasta el momento. Hasta acá viene sin tildes y sin símbolos
	cadena = cadena.split(" ") # Dividimos nuevamente la cadena pero ahora no es por cada elemento, sino por cada palabra separada por espacio

	# Eliminamos los stop words de la instrucción del usuario
	# Teniendo las palabras de la instrucción por separado ahora podemos eliminar aquellas palabras que sean stop word
	for stop_word in stop_words:
		if stop_word in cadena:
			while stop_word in cadena: # Eliminamos todas las ocurrencias
				cadena.remove(stop_word)
	
	# Unimos la instrucción después de eliminar las stop words
	nuevaCadena = ""
	for i in range(len(cadena)):
		nuevaCadena += cadena[i]
		if(i < len(cadena)-1):
			nuevaCadena += " "
	cadena = nuevaCadena

	# La volvemos otra vez una lista para poder quitar los acentos
	tokens = list(cadena)
	# print(tokens)
	# input()

	# En este ciclo reemplazamos las vocales con tilde por su versión sin tilde
	for i in range (len(tokens)):
		if tokens[i] in reemplazos:
			tokens[i] = reemplazos[tokens[i]]
	
	#Volvemos a unir la cadena
	cadena = "".join(tokens)

	#Importamos el stemmer en español
	stemmer = SnowballStemmer('spanish')

	# La partimos por espacios y a cada palabra le sacamos su raíz con el stemming
	cadena = cadena.split(" ")
	for i in range(len(cadena)):
		cadena[i] = stemmer.stem(cadena[i])

	# Volvemos a unir toda la cadena
	nuevaCadena = ""
	for i in range(len(cadena)):
		nuevaCadena += cadena[i]
		if(i < len(cadena)-1):
			nuevaCadena += " "
	cadena = nuevaCadena

	# Finalmente, la retornamos.
	# No hacemos lematización porque no valdría la pena al ya tener la raíz de cada palabra usando stemming
	return cadena.strip()

parejasLogicaPredicados = [
	# [ '(.*)logica(.*)predicados(.*)', ['Es una representación formal de conocimiento. Está basada en la idea de que las sentencias expresan relaciones entre los objetos o cualidades o atributos de estos.'] ],
    [ limpiarEntrada("¿Qué es la lógica de predicados?"), [ random.choice(prefijos) +  'La lógica de predicados es una representación formal de conocimiento. Está basada en la idea de que las sentencias expresan relaciones entre los objetos o cualidades o atributos de estos.'] ],
    [ '(' + limpiarEntrada("¿Qué es la lógica de primer orden?"  + '|' + limpiarEntrada("Lógica") + '|' + limpiarEntrada("Primer orden") +')'), [random.choice(prefijos) + 'La lógica o lógica de primer orden es el estudio del razonamiento y si este es correcto, se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular.'] ],
    [ limpiarEntrada("¿En qué se centra la lógica de primer orden?"), [random.choice(prefijos) + 'La lógica de primer orden se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular'] ],
	[ '(' + limpiarEntrada("¿Qué es una proposición?") + '|' + limpiarEntrada("¿Qué es una proposición en lógica de predicados?") + '|' + limpiarEntrada("¿Qué es una proposición en lógica?") +')', [random.choice(prefijos) + 'Una proposición es una unidad semántica que, o solo es verdadero, o solo es falsa, pero no ambas cosas. Los enunciados que expresen admiración, duda, interrogación, suspenso, etc., no son proposiciones.'] ],
	[ '('+ limpiarEntrada("¿Cuáles son los tipos de proposiciones?") + "|" + limpiarEntrada("Tipos de proposiciones") +')', [random.choice(prefijos) + 'Una proposición es una unidad semántica que, o solo es verdadero, o solo es falsa, pero no ambas cosas. Los enunciados que expresen admiración, duda, interrogación, suspenso, etc., no son proposiciones.'] ],
	[ '(' + limpiarEntrada("¿Qué es un predicado") + '|' + limpiarEntrada("¿Qué es un predicado en lógica de predicados?") + ')', [random.choice(prefijos) + 'Un predicado es un enunciado que describe características y/o relaciones entre los objetos del mundo. Representan relaciones o asociaciones dentro del dominio. Son falsos o verdaderos según se dé la relación entre los elementos'] ],
	[ '('+ limpiarEntrada("¿Cuáles son los elementos de la logica de predicados?") + "|" + limpiarEntrada("¿Cómo está conformada la lógica de predicados?") + "|" + limpiarEntrada("¿Cuáles son las partes de la lógica de predicados?") +')', [random.choice(prefijos) + 'Los elementos que componen la lógica de predicados son el alfabeto, el lenguaje formal, el conjunto de enunciados y el conjunto de reglas de inferencia'] ],
	[ '('+ limpiarEntrada("Partes del alfabeto") + "|" + limpiarEntrada("¿Qué es el alfabeto en lógica de predicados?") + "|" + limpiarEntrada("¿Qué es el alfabeto?") + "|" + limpiarEntrada("Componentes del alfabeto") +')', [random.choice(prefijos) + 'El alfabeto en lógica de predicados es el conjunto de símbolos usados para la representación del conocimiento. Sus partes son las constantes, variables, funciones, predicados, conjunciones, cuantificadores y átomos. ¡Puedes preguntarme por cada uno de ellos!'] ],
	[ '('+ limpiarEntrada("¿Qué son constantes?") + "|" + limpiarEntrada("¿Qué son constantes en lógica de predicados?") +')', [random.choice(prefijos) + 'Las constantes son los términos que se usan para representar argumentos de predicados que no cambian en un proceso de inferencia, es decir, su valor no se modifica. Estas tienen la particularidad de que siempre inician con una letra minúscula. Por ejemplo, se puede tener la constante “azul”.'] ],
	[ '('+ limpiarEntrada("¿Qué son variables?") + "|" + limpiarEntrada("¿Qué son variables en lógica de predicados?") +')', [random.choice(prefijos) + 'Las variables son los términos que se usan para representar argumentos de predicados que pueden variar en un proceso de inferencia, es decir, su valor puede ser modificado. Tienen la particularidad de siempre iniciar con una letra mayúscula. Un ejemplo de variable es “Color”'] ],
	[ '('+ limpiarEntrada("¿Qué son funciones?") + "|" + limpiarEntrada("¿Qué son funciones en lógica de predicados?") +')', [random.choice(prefijos) + 'Las funciones en lógica de predicados se utilizan para identificar un elemento único del dominio, es decir, son una forma de denotar a un individuo sin hacer una referencia directa al mismo. Puede ser aplicada a una o más constantes (individuos) y expresará o retornará solo un individuo. Por ejemplo, la funcion mas_alto(juan, jose).'] ],
	[ '('+ limpiarEntrada("¿Qué es dominio?") + "|" + limpiarEntrada("¿Qué es dominio en lógica de predicados?") +')', [random.choice(prefijos) + 'El dominio en lógica de predicados es el conjunto de individuos que están enmarcados bajo el conocimiento que se desea representar. También es conocido como el universo del discurso. Por ejemplo en el problema  del lobo, de la cabra y de la col el dominio estará conformado por estos mismos objetos: lobo, cabra y col, ya que son los valores disponibles (individuos) para asignar a variables a usar. '] ],
	[ '('+ limpiarEntrada("¿Qué son las conjunciones?") + "|" + limpiarEntrada("¿Qué son las conjunciones en lógica de predicados?") +')', [random.choice(prefijos) + 'Una conjunción entre dos proposiciones es un conector lógico cuyo valor de la verdad resulta en cierto solo si ambas proposiciones son ciertas, y en falso de cualquier otra forma. Las conjunciones utilizadas en lógica de proposiciones son: \n* ^  AND (Y) \n* v  OR  (O) \n* =>  Implicación \n* <= =>  Equivalente a \n* ~  ¬  NOT  (Negación)'] ],
	[ '('+ limpiarEntrada("¿Qué son los cuantificadores?") + "|" + limpiarEntrada("¿Qué son los cuantificadores en lógica de predicados?") + "|" + limpiarEntrada("Tipos de cuantificadores") + "|" + limpiarEntrada("Cuantificadores existenciales") + "|" + limpiarEntrada("Cuantificadores universales") + "|" + limpiarEntrada("¿Qué son los cuantificadores existenciales?") + "|" + limpiarEntrada("¿Qué son los cuantificadores universales?") +')', [random.choice(prefijos) + 'Un cuantificador es una expresión que indica la cantidad de veces que un predicado o propiedad P se satisface dentro de una determinada clase. No es posible cuantificar predicados. \n Existen cuantificadores universales y existenciales. \n Los cuantificadores universales se utilizan para aseverar que una fórmula es verdadera para todos los valores de la variable asociada. \n Los cuantificadores existenciales se emplean para aseverar que por lo menos existe alguna asignación para X que hará que la fórmula asociada sea veraz.'] ],
	[ '('+ limpiarEntrada("¿Qué es un átomo?") + "|" + limpiarEntrada("¿Qué es átomo en lógica de predicados?") +')', [random.choice(prefijos) + 'Los átomos son aquellos predicados cuyos argumentos son constantes, variables o funciones. Es la mínima expresión que puede escribirse en lógica.'] ],
	[ '('+ limpiarEntrada("¿Cómo se simbolizan los cuantificadores?") + "|" + limpiarEntrada("¿Cómo se simbolizan los cuantificadores universales?") + "|" + limpiarEntrada("¿Cómo se simbolizan los cuantificadores existenciales?") + "|" + limpiarEntrada("Símbolos cuantificadores") +')', [random.choice(prefijos) + 'Para el cuantificador universal se utiliza el símbolo de para todo, y para el cuantificador existencial se utiliza el símbolo de existe.'] ],
	[ '('+ limpiarEntrada("Lenguajes y reglas de formación") + "|" + limpiarEntrada("¿Cuáles son los lenguajes y reglas de formación?") + "|" + limpiarEntrada("lenguajes") + "|" + limpiarEntrada("Reglas de formación") + "|" + limpiarEntrada("FBF") + "|" + limpiarEntrada("Fórmulas bien formadas") + "|" + limpiarEntrada("¿Qué son las fórmulas bien formadas?") + "|" + limpiarEntrada("lenguajes de formación") +')', [random.choice(prefijos) + 'El lenguaje y reglas de formación determinan los elementos válidos en la combinación del alfabeto, lo que se conoce como Fórmulas Bien Formadas (FBF).\n* Una fórmula atómica es una FBF. \n*Si F y G son FBF entonces sus conjunciones también lo son. \n*Si F es FBF y X es una variable entonces las cuantificaciones existenciales o universales entre F y X también son FBF. \n*Una función NO es una FBF.'] ],
	[ '('+ limpiarEntrada("¿Qué es la inferencia?") + "|" + limpiarEntrada("¿Qué es la inferencia en lógica de predicados?") +')', [random.choice(prefijos) + 'Es el proceso de generar nuevas FBF a partir de las FBF existentes mediante la aplicación de reglas de inferencia como lo son Modus Ponens , Modus Tollens y Especialización Universal. ¡Pregúntame por cada uno de ellos para saber más!'] ],
	[ '('+ limpiarEntrada("¿Cuáles son las reglas de la inferencia?") + "|" + limpiarEntrada("¿Cuáles son las reglas de la inferencia en lógica de predicados?") + "|" + limpiarEntrada("Reglas de la inferencia") + "|" + limpiarEntrada("Enumerar las reglas de la inferencia") + "|" + limpiarEntrada("Reglas de la inferencia más comunes") +')', [random.choice(prefijos) + 'Las reglas de la inferencia más comunes son: Modus Ponens, Modus Tollens y Especialización Universal. ¡Puedes preguntarme por cada uno de estos, para que obtengas más información!'] ],
	[ '('+ limpiarEntrada("¿Qué es el modus ponens?") + "|" + limpiarEntrada("modus ponens") + "|" + limpiarEntrada("¿Qué es el modus ponens en lógica de predicados?") +')', [random.choice(prefijos) + 'El Modus Ponens es una forma de razonamiento deductivo y una regla de inferencia en lógica proposicional. Se puede resumir de la forma “si P implica Q y P es verdadero, entonces Q también es verdadero”. Un ejemplo es: “Si está lloviendo (P), te espero dentro del teatro (Q)” Si suponemos que P es verdadero (Está lloviendo) entonces Q inmediatamente es verdadero (Por lo tanto, te espero en el teatro).'] ],
	[ '('+ limpiarEntrada("¿Qué es el modus tollens?") + "|" + limpiarEntrada("modus tollens") + "|" + limpiarEntrada("¿Qué es el modus tollens en lógica de predicados?") +')', [random.choice(prefijos) + 'El Modus Tollens es una forma de argumento válida y una regla de inferencia en lógica proposicional. Se puede resumir de la forma “Si P implica Q y Q no es cierto, entonces P no es cierto”. Un ejemplo es: “Si el agua hierve (P), entonces soltará vapor (Q)” Si suponemos que Q es falso (No suelta vapor) entonces P también es falso (No está hirviendo el agua).'] ],
	[ '('+ limpiarEntrada("¿Qué es especialización universal?") + "|" + limpiarEntrada("especialización universal") + "|" + limpiarEntrada("¿Qué es la especialización universal en lógica de predicados?") +')', [random.choice(prefijos) + 'También conocida como instanciación universal, es una regla de inferencia válida que a partir de una verdad sobre cada miembro de una clase de individuos da la verdad sobre un individuo en particular de esa clase. Un ejemplo es: “Todos los perros son mamíferos. PitufoLIGRED es un perro. Por lo tanto PitufoLIGRED es un mamífero”.'] ],
	[ '('+ limpiarEntrada("¿Qué es unificación?") + "|" + limpiarEntrada("unificación") + "|" + limpiarEntrada("¿Qué es la unificación en lógica de predicados?") +')', [random.choice(prefijos) + 'Se basa en el reconocimiento de las leyes de equivalencia que son ciertas para todas las fórmulas y se puede utilizar para construir una FBF. Un ejemplo sería:\n(1) pitufoLIGRED es un perro  = perro(pitufoLIGRED)\n\t(paraTodo X) perro(X) => tiene_cola(X)\n\tpitufoLIGRED reemplaza a X\n\tperro(pitufoLIGRED) => tiene_cola(pitufoLIGRED)\n(2)pitufoLIGRED tiene cola = tiene_cola(pitufoLIGRED)'] ],
	# [ '', [] ],
	# [ '', [] ],
	# [ '', [] ],

	['salir', ["Gracias por hablar conmigo.", "Adiós.", "Gracias, queda pendiente el café", "Que tengas un buen día!"]],
]

parejasRedesSemanticas = [
	# [ '(.*)logica(.*)predicados(.*)', ['Es una representación formal de conocimiento. Está basada en la idea de que las sentencias expresan relaciones entre los objetos o cualidades o atributos de estos.'] ],
    [ limpiarEntrada("¿Qué son las redes semanticas?"), [ random.choice(prefijos) +  'Las redes semánticas son sistemas de organización del conocimiento que estructuran los conceptos, no como una jerarquía sino como una red. Son grafos orientados que proporcionan una representación declarativa de objetos, propiedades y relaciones; además, están compuestos por nodos, arcos y relaciones. En resumen, es una forma de representación de conocimiento lingüístico en la que los conceptos y sus interrelaciones se representan mediante un grafo. ¡Puedes preguntarme más acerca de los nodos, arcos y relaciones o acerca del mecanismo de inferencia!'] ],
    [ '(' + limpiarEntrada("¿Qué son nodos y arcos?")+'|'+ limpiarEntrada("¿Cuáles son las partes de un grafo que representa una red semántica?") + '|' + limpiarEntrada("¿Cuáles son las partes de un grafo de una red semántica?") + '|' + limpiarEntrada("¿Qué son nodos?") + '|' + limpiarEntrada("¿Qué son arcos?") + '|' + limpiarEntrada("¿Qué son relaciones?")  +')', [random.choice(prefijos) + 'PARTES DE UN GRAFO QUE REPRESENTA UNA RED SEMÁNTICA: (i) Los nodos se utilizan para representar objetos o propiedades. (ii)Los arcos representan las relaciones entre nodos. (iii) Las relaciones son las palabras descriptivas sobre cada arco. Pueden ser de tipo todo-parte, causa-efecto, padre-hijo, “es un” o “es parte”'] ],
    [ '(' + limpiarEntrada("¿Cuál es el mecanismo de inferencia básico en las redes semánticas?") + '|' + limpiarEntrada("inferencia") + '|' + limpiarEntrada("¿Qué es herencia de propiedades?") + '|' + limpiarEntrada("¿Qué es el mecanismo de inferencia de herencia de propiedades?") + '|' + limpiarEntrada('¿Cuál es el mecanismo de inferencia básico?') + ')', [random.choice(prefijos) + 'El mecanismo de inferencia básico en las redes semánticas es la herencia de propiedades. Esto es que un nodo hereda las propiedades de los otros nodos que estén en un mayor nivel de jerarquía y tengan un arco con él.'] ],
	[ '(' + limpiarEntrada("Ejemplo de red semántica") + '|' + limpiarEntrada("Red semántica ejemplo") + '|' + limpiarEntrada("Ver red semántica") + '|' + limpiarEntrada("Visualiza red semántica") + '|' + limpiarEntrada("Visualización red semántica") + ')', [random.choice(prefijos) + 'Se abrirá una imagen que contiene una red semántica de ejemplo. Por favor haz click al siguiente enlace: https://imgur.com/a/p7TYPZ9'] ],
	[ '(' + limpiarEntrada("¿Qué son enlaces en redes semánticas?") + '|' + limpiarEntrada("¿Qué son enlaces?") + ')', [random.choice(prefijos) + 'Los enlaces son una aseveración respecto de un elemento con relación a otro. Dado que las aseveraciones pueden ser solamente verdaderas o falsas, un enlace es una relación binaria. Si quieres saber sobre relaciones binarias o relaciones no simétricas ¡pregúntame! '] ],
	[ '(' + limpiarEntrada("¿Qué son las relaciones binarias?") + '|' + limpiarEntrada('¿Cuáles son las relaciones binarias?') + '|' + limpiarEntrada('¿Cuáles son las relaciones binarias más comunes?') + '|' + limpiarEntrada('¿Cuáles son las relaciones binarias más comúnmente empleadas?') + '|' + limpiarEntrada("Ejemplos de las relaciones binarias más comúnmente empleadas") + '|' + limpiarEntrada("Ejemplos de relaciones binarias") + '|' + limpiarEntrada("relaciones binarias en redes semánticas") + ')', [random.choice(prefijos) + 'Las relaciones binarias son aquellas que se dan en ambos sentidos en los elementos relacionados, las más comúnmente empleadas son es-un (ISA) y parte-de (PARTOF). Por ejemplo: \nCABALLO es-un MAMÍFERO \n COLA parte-de CABALLO '] ],
	['(' + limpiarEntrada("¿Qué son las relaciones no simétricas?") + '|' + limpiarEntrada('¿Cuáles son las relaciones no simétricas?') + '|' + limpiarEntrada('¿Cuáles son las relaciones no simétricas más comunes?') + '|' + limpiarEntrada('¿Cuáles son las relaciones no simétricas más comúnmente empleadas?') + '|' + limpiarEntrada("Ejemplos de las relaciones no simétricas más comúnmente empleadas") + '|' + limpiarEntrada("Ejemplos de relaciones no simétricas") + '|' + limpiarEntrada("relaciones no simétricas en redes semánticas") + ')', [random.choice(prefijos) + 'Las relaciones no simétricas son aquellas que se dan en un solo sentido en los elementos relacionados, estas requieren grafos dirigidos que usan flechas en lugar de líneas. Para el ver el ejemplo, abre el siguiente enlace: https://imgur.com/a/5C6PC9g'] ],
	[ '(' + limpiarEntrada("ejemplo tuplas objeto atributo valor") + '|' + limpiarEntrada("tuplas objeto atributo valor") + ')', [random.choice(prefijos) + 'Puedes ver la representación de las redes semánticas en tuplas objeto atributo valor en la imagen, que aparece  en el siguiente link: https://imgur.com/a/1XqdwQh'] ], 
	[ '(' + limpiarEntrada("¿Qué es herencia en redes semánticas?") + '|'+ limpiarEntrada("¿qué es herencia?") + '|' + limpiarEntrada("ejemplo de herencia") + ')', [random.choice(prefijos) + 'Definimos la herencia como el sistema de razonamiento que lleva a un agente a deducir propiedades de un concepto basándose en las propiedades de conceptos más altos en la jerarquía Haz click en el siguiente link para un ejemplo: https://imgur.com/a/NEsJRrq \n\n La herencia, por tanto, puede ser definida como el proceso mediante el cual se determinan unas propiedades de un concepto C, buscando las propiedades atribuidas localmente a C, si esta información no se encuentra a nivel local, buscando las propiedades atribuidas a conceptos que se encuentran en los niveles superiores a C en la jerarquía conceptual.'] ],
	[ '(' + limpiarEntrada("¿Qué es confrontación en redes semánticas?") + '|'+ limpiarEntrada("¿qué es confrontación?") + '|' + limpiarEntrada("ejemplo de confrontación") + ')', [random.choice(prefijos) + 'La confrontación es reemplazar un elemento particular externo del que se conoce una característica que está relacionada con un nodo general del grafo y así empezar con el proceso de inferencia. Para ver el ejemplo da click al siguiente enlace: https://imgur.com/a/DR0t9pi'] ],
	[ '(' + limpiarEntrada("¿Cuáles son las excepciones en la herencia?") +')', [random.choice(prefijos) + 'Para entender las excepciones en la herencia es necesario que abras el siguiente enlace: https://imgur.com/a/bpnjHmI'] ],
	[ '(' + limpiarEntrada("www") + '|' + limpiarEntrada("triple dobleu") + '|' + limpiarEntrada("triple w") + '|' + limpiarEntrada("web") + '|' + limpiarEntrada("web semántica") + '|' + limpiarEntrada("semantic web") +')', [random.choice(prefijos) + '\n->La web semántica busca incorporar “significado” a la información en el WWW: \n \t-Ontologías (las cuales definen conceptos y relaciones de algún dominio, de forma compartida y consensuada; esta conceptualización debe ser representada de una manera formal, legible y utilizable por los ordenadores) de conceptos en   diversos dominios. \n\t -Relaciones entre conceptos. \n->Esto facilitará a agentes el “entender” la información y hacer búsquedas mucho más sofisticadas \n->Uso de estándares como XML (metalenguaje que permite definir lenguajes de marcas desarrollado por el World Wide Web Consortium utilizado para almacenar datos en forma legible) y RDF (es un método general para descomponer cualquier tipo de conocimiento en trozos pequeños, con algunas reglas acerca de la semántica o significado). '] ],
	[ '(' + limpiarEntrada("Ventajas de las redes semánticas")+ '|' + limpiarEntrada("ventajas") + ')', [random.choice(prefijos) + 'Las ventajas de las redes semánticas son: \n• Representación “estructurada” del conocimiento. \n• Economía cognoscitiva: no es necesario representar en forma explícita todas las propiedades. \n• Definición de distancia semántica entre conceptos (número de enlaces a recorrer).\n • Representación “analógica” de conocimiento'] ],
	[ '(' + limpiarEntrada("¿Qué son predicados binarios?") + '|' + limpiarEntrada("Predicados binarios") + '|' + limpiarEntrada("¿Cuál es la representación alternativa?") + '|' + limpiarEntrada("Representación alternativa de redes semánticas") + ')', [random.choice(prefijos) + ' Los predicados binarios son una representación alternativa a los correspondientes arcos en el grafo. El símbolo del predicado corresponde a la etiqueta del arco , los argumentos del predicado corresponden a los vértices incidentes de dicho arco. Un ejemplo de esta representación es: Is_a(tanque, componente) que sería una relación del tipo ISA entre tanque y componente.'] ],

	['salir', ["Gracias por hablar conmigo.", "Adiós.", "Gracias, queda pendiente el café", "Que tengas un buen día!"]],
]




# Obtenido de: https://www.nltk.org/_modules/nltk/chat/util.html
# La librería es open source, por lo que no hay problema en modificarla: https://github.com/nltk/nltk#natural-language-toolkit-nltk
class Chat:
	def __init__(self, pairs, reflections={}):
		"""
		Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
		pattern is a regular expression matching the user's statement or question,
		e.g. r'I like (.*)'.  For each such pattern a list of possible responses
		is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
		which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
		the numbered positions in the responses, e.g. %1.

		:type pairs: list of tuple
		:param pairs: The patterns and responses
		:type reflections: dict
		:param reflections: A mapping between first and second person expressions
		:rtype: None
		"""

		self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
		self._reflections = reflections
		self._regex = self._compile_reflections()


	def _compile_reflections(self):
		sorted_refl = sorted(self._reflections, key=len, reverse=True)
		return re.compile(
			r"\b({})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
		)

	def _substitute(self, str):
		"""
		Substitute words in the string, according to the specified reflections,
		e.g. "I'm" -> "you are"

		:type str: str
		:param str: The string to be mapped
		:rtype: str
		"""

		return self._regex.sub(
			lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
		)

	def _wildcards(self, response, match):
		pos = response.find("%")
		while pos >= 0:
			num = int(response[pos + 1 : pos + 2])
			response = (
				response[:pos]
				+ self._substitute(match.group(num))
				+ response[pos + 2 :]
			)
			pos = response.find("%")
		return response

	def respond(self, str):
		"""
		Generate a response to the user input.

		:type str: str
		:param str: The string to be mapped
		:rtype: str
		"""

		# check each pattern
		for (pattern, response) in self._pairs:
			match = pattern.match(str)

			# did the pattern match?
			if match:
				resp = random.choice(response)  # pick a random response
				resp = self._wildcards(resp, match)  # process wildcards

				# fix munged punctuation at the end
				if resp[-2:] == "?.":
					resp = resp[:-2] + "."
				if resp[-2:] == "??":
					resp = resp[:-2] + "?"
				return resp


	# Hold a conversation with a chatbot
	def converse(self, quit="salir"):
		user_input = ""
		global errores # Incluímos la lista de mensaje de errores por si se debiera mostrar alguno
		global nombre
		while user_input != quit:
			user_input = quit
			try:
				user_input = input('\n' + nombre + "> ")
			except EOFError:
				print(user_input)
			if user_input:
				while user_input[-1] in "!.":
					user_input = user_input[:-1]
				if user_input == quit:
					return
				user_input = limpiarEntrada(user_input) # Acá llamamos a la función que creamos. En esa función se hace el proceso de limpieza de la instrucción del usuario.
				resp = self.respond(user_input)
				if resp is None: 
					resp = random.choice(errores) # Obtenemos un error aleatorio en caso de que el chatbot no encuentre respuesta
				print( '\n' + "ChatBot> " + resp) # Mostramos la respuesta o mensaje de error del chatbot

def chatbotLogicaPredicados():
	global nombre
	global parejasLogicaPredicados
	limpiarPantalla()
	print("\n--- ChatBot Informativo - Lógica de Predicados de Primer Orden ---")
	print("\nA continuación podrás encontrar información de los siguientes temas: ")

	print(" -> ¿Qué es la lógica de predicados?")
	print(" -> ¿Qué es la lógica (lógica de primer orden)?")
	print(" -> ¿En qué se centra la lógica de primer orden?")
	print(" -> ¿Qué es una proposición?")
	print(" -> Tipos de proposiciones")
	print(" -> ¿Qué es un predicado?")
	print(" -> ¿Cuáles son los elementos de la lógica de predicados?")
	print(" -> ¿Qué es el alfabeto en lógica de predicados?")
	print(" -> ¿Qué son constantes en lógica de predicados?")
	print(" -> ¿Qué son variables en lógica de predicados?")
	print(" -> ¿Qué son funciones en lógica de predicados?")
	print(" -> ¿Qué es dominio en lógica de predicados?")
	print(" -> ¿Qué son las conjunciones en lógica de predicados?")
	print(" -> ¿Qué son los cuantificadores en lógica de predicados?")
	print(" -> ¿Cómo se simbolizan los cuantificadores?")
	print(" -> ¿Qué es un átomo en lógica de predicados?")
	print(" -> ¿Cuáles son los lenguajes y reglas de formación?")
	print(" -> Inferencia")
	print(" -> Reglas de la inferencia")
	print(" -> Modus Ponens")
	print(" -> Modus Tollens")
	print(" -> Especialización Universal")
	print(" -> Unificación")

	print("¡Puedes empezar a chatear ahora mismo! ¡Escribe Salir si deseas terminar!")
	chatLogica = Chat(parejasLogicaPredicados, reflections)
	chatLogica.converse()


def chatbotRedesSemanticas():
	global nombre
	global parejasRedesSemanticas
	limpiarPantalla()
	print("\n--- ChatBot Informativo - Redes Semánticas ---")
	print("\nA continuación podrás encontrar información de los siguientes temas: ")

	print(" -> ¿Qué son redes semánticas?")
	print(" -> Partes del grafo que representa una red semántica (nodos, arcos y relaciones)")
	print(" -> Mecanimo de inferencia básico (herencia de propiedades)")
	print(" -> Ejemplo de red semántica")
	print(" -> Enlaces en redes semánticas")
	print(" -> Relaciones binarias")
	print(" -> Relaciones no simétricas")
	print(" -> Ejemplo tuplas objeto atributo valor")
	print(" -> Herencia en redes semánticas")
	print(" -> Confrontación en redes semánticas")
	print(" -> Excepciones en la herencia")
	print(" -> Redes semánticas en la Web")
	print(" -> Ventajas de las redes semánticas")
	print(" -> Predicados binarios")

	print("¡Puedes empezar a chatear ahora mismo! ¡Escribe Salir si deseas terminar!")
	chatRedes=Chat(parejasRedesSemanticas, reflections)
	chatRedes.converse()
	


def main():
	global nombre
	print("\nBienvenido al ChatBot Informativo de Formas de Representación del Conocimiento")
	print("\nA continuación podrás acceder a información acerca de Lógica de Predicados de Primer Orden y Redes Semánticas")

	nombre = input("\nHola, ¿Cuál es tu nombre?: ")

	bandera = True
	while bandera:
		limpiarPantalla()
		print("\n --- Menú Principal ---\n")

		print("1.\tLógica de Predicados de Primer Orden")
		print("2.\tRedes Semánticas")
		print("3.\tSalir del ChatBot")


		opcion = 0
		while opcion != 1 and opcion !=2 and opcion !=3:
			mensaje = "\n" + nombre + " ingresa la opción a la que desea acceder: "
			try:
				opcion = int(input(mensaje))
			except ValueError:
				print("\nError, ingresa un número")
			if opcion != 1 and opcion !=2 and opcion !=3:
				print("\nError, ingrese una opción válida")

		if opcion == 1:
			chatbotLogicaPredicados()
		elif opcion == 2:
			chatbotRedesSemanticas()
		else:
			mensaje = random.choice(despedidas)
			print(mensaje)
			bandera = False

if __name__ == "__main__":
	main()