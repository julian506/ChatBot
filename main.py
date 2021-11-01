import random
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

nltk.download('stopwords')

nombre = ""

prefijos = ["¡Que buena pregunta! ", "¡Excelente pregunta! ", "¡Me encanta responder esto! ", "¡Wow me encanta que preguntes esto! ", "¡Genial tu pregunta! "]

errores = ["Lo siento, no te entendí :(", "No entendí tu pregunta, ¿Podrías reformularla?", "Creo que no entiendo a qué te refieres"]

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

	simbolos = ["?", "¿", "¡", "!", ".", ",", "}", "{"]
	tokens = list(entrada) # Usamos el list para dividir la instrucción. No usamos el word_tokenize porque no separa símbolos únicos del español como el ¿. Preferimos usar una lista
	# print(tokens)
	# input()

	# En este ciclo eliminamos todos los símbolos que puedan aparecer en la instrucción del usuario
	for simbolo in simbolos:
		if simbolo in tokens:
			while simbolo in tokens:
				tokens.remove(simbolo)

	stop_words = stopwords.words('spanish') # Importamos los stop words del idioma español
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
	return cadena

parejasLogicaPredicados = [
	# [ '(.*)logica(.*)predicados(.*)', ['Es una representación formal de conocimiento. Está basada en la idea de que las sentencias expresan relaciones entre los objetos o cualidades o atributos de estos.'] ],
    [ limpiarEntrada("¿Qué es la lógica de predicados?"), [ random.choice(prefijos) +  'Es una representación formal de conocimiento. Está basada en la idea de que las sentencias expresan relaciones entre los objetos o cualidades o atributos de estos.'] ],
	# [ '((.*)logica(.*)|(.*)primer orden(.*))', ['La lógica es el estudio del razonamiento y si este es correcto, se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular.'] ],
    [ limpiarEntrada("¿Qué es la lógica de primer orden?"), [random.choice(prefijos) + 'La lógica es el estudio del razonamiento y si este es correcto, se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular.'] ],
	# [ '((.*)centra logica primer orden(.*)|centra logica primer orden)', ['La lógica de primer orden se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular'] ],
    [ limpiarEntrada("¿En qué se centra la lógica de primer orden?"), [random.choice(prefijos) + 'La lógica de primer orden se centra en la relación entre las afirmaciones y no en el contenido de una afirmación en particular'] ],
	# [ '', [] ],
	# [ '', [] ],
	# [ '', [] ],

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
				user_input = input(nombre + ">")
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
				print("ChatBot> " + resp) # Mostramos la respuesta o mensaje de error del chatbot

def chatbotLogicaPredicados():
	global nombre
	global parejasLogicaPredicados
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
	print("\n--- ChatBot Informativo - Redes Semánticas ---")
	print("\nA continuación podrás encontrar información de los siguientes temas: ")

	print(" -> ¿Qué son redes semánticas")
	print(" -> Partes del grafo que representa una red semántica (nodos, arcos y relaciones)")
	print(" -> Mecanimo de inferencia básico (herencia de propiedades)")
	print(" -> Ejemplo de red semántica")
	print(" -> Enlaces en redes semánticas")
	print(" -> Relaciones binarias")
	print(" -> Relaciones no simétricas")
	print(" -> Redes semánticas representadas en  tuplas objeto - atributo-valor")
	print(" -> Herencia en redes semánticas")
	print(" -> Confrontación en redes semánticas")
	print(" -> Excepciones en la herencia")
	print(" -> Redes semánticas en la Web")
	print(" -> Ventajas de las redes semánticas")
	print(" -> Predicados binarios")


def main():
	global nombre
	print("\nBienvenido al ChatBot Informativo de Formas de Representación del Conocimiento")
	print("\nA continuación podrás acceder a información acerca de Lógica de Predicados de Primer Orden y Redes Semánticas")

	nombre = input("\nHola, ¿Cuál es tu nombre?\n")

	print("\n --- Menú Principal ---\n")

	print("1.\tLógica de Predicados de Primer Orden")
	print("2.\tRedes Semánticas")


	opcion = 0
	while opcion != 1 and opcion !=2:
		mensaje = "\n" + nombre + " ingresa la opción a la que desea acceder: "
		opcion = int(input(mensaje))
		if opcion != 1 and opcion !=2:
			print("\nError, ingrese una opción válida")


	if opcion == 1:
		chatbotLogicaPredicados()
	else:
		chatbotRedesSemanticas()

if __name__ == "__main__":
	main()