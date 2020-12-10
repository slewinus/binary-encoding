class Cellule:
    def __init__(self, v, n=None):
        self.value = v
        self.next = n


class File:
    def __init__(self):
        self.v = []

    def est_vide(self):
        return len(self.v) == 0

    def enfiler(self, x):
        self.v.insert(0, x)

    def defiler(self):
        return(self.v.pop())

    def taille(self):
        return(len(self.v))


class Noeud:
    def __init__(self, g, v, d):
        self.gauche = g
        self.droit = d
        self.valeur = v

    def donnee(self):
        return self.valeur

    def fils_gauche(self):
        return self.gauche

    def fils_droit(self):
        return self.droit


with open('data.txt', 'r') as file:
    data = file.read().replace('\n', '')

print(data)
string = data


def occurences(char, string):
	""" str, str -> int
		Retourne le nombre d'apparitions de char dans string
	"""
	total = 0
	for i in string:
		if i == char:
			total += 1
	return(char, total)


def char_list(string):
	""" str -> list(str)
	Retourne la liste des caracteres presents dans string
	"""
	list = []
	for i in string:
		if not i in list:
			list.append(i)
	return list


def tuple_list(string):
	""" string -> list(tuple)
		Retourne une liste de tuple contenant chacun un caractere
		present dans string et son nombre doccurences.
	"""
	liste = []
	l2 = char_list(string)
	for lettre in l2 :
		liste.append(occurences(lettre, string))
	return liste


def sort_tuple_list(tuplelist):
	""" list(tuple) -> list(tuple)
		Retourne la liste de tuple triee par son deuxieme element
	"""
	for i in range(len(tuplelist)):
		minimum = i
		for j in range(i+1, len(tuplelist)):
			if tuplelist[minimum][1] > tuplelist[j][1]:
				minimum = j
		tmp = tuplelist[i]
		tuplelist[i] = tuplelist[minimum]
		tuplelist[minimum] = tmp
	return tuplelist


def create_tree(tuplelist):
	file = File()
	for tuple in tuplelist:
		file.enfiler(tuple)
	while file.taille() > 1:
		gauche = file.defiler()
		droite = file.defiler()
		if type(gauche[0]) is str:
			data = gauche[0]
			gauche = (Noeud(None, data, None), gauche[1])
		if type(droite[0]) is str:
			data = droite[0]
			droite = (Noeud(None, data, None), droite[1])
		noeud = Noeud(gauche[0], gauche[1] + droite[1], droite[0])
		file.enfiler((noeud, gauche[1] + droite[1]))
		file.v = sort_tuple_list(file.v)
		file.v.reverse()
	return file.defiler()


def parcours(x, a, t):
	if a is None:
		return False
	elif parcours(x, a.fils_droit(), t):
		t.append(1)
		return True
	elif parcours(x, a.fils_gauche(), t):
		t.append(0)
		return True
	elif x == a.donnee():
		return True
	else:
		return False


def get_keys(string):
	tree = create_tree(tuple_list(string))[0]
	keys = []
	for char in char_list(string):
		k = []
		parcours(char, tree, k)
		key = str()
		for i in range(len(k) - 1, -1, - 1):
			key += str(k[i])
		keys.append((char, key))
	return(keys)


def get_char_key(char, keys):
	for key in keys:
		if key[0] == char:
			return key[1]


def compress(string):
	compressed = str()
	keys = get_keys(string)
	for char in string:
		compressed += get_char_key(char, keys)
	return compressed, keys


def eliminate_keys(available, pattern):
	av = []
	for key in range(len(available)):
		if available[key][1][0:len(pattern)] == pattern:
			av.append(available[key])
	return av


def decompress(compressed, keys):
	decompressed = str()
	i = 0
	while i < len(compressed):
		available = keys
		pattern = str()
		while len(available) > 1:
			if compressed[i] == '0':
				pattern += '0'
			else:
				pattern += '1'
			available = eliminate_keys(available, pattern)
			i += 1
		decompressed += available[0][0]
	return decompressed


compressed, cles = compress(string)
print(compressed)
print(cles)

print(decompress(compressed, cles))
