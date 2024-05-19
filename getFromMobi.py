import requests
import re, string

a = str(input("Login: "))
b = str(input("Haslo: ")) 
login_data = {"login":a,"haslo":b} #dane do logowania
start = "Planlekcji" #kiedy sie zaczynaja dane (uzyteczne dane)
koniec = "varpage" #javascript ktory nie jest filtrowany (juz jest)
startdata = "Podstawowy" #kiedy data sie zaczyna
dzien = "&nbsp;-&nbsp;" #kiedy kolejny dzien sie zaczyna
odwolane = "Lekcjaodwołana"
wolne = "Dzieńwolny"

s = requests.Session() #inicjalizacja
s.post("https://zslpoznan.mobidziennik.pl/dziennik", data=login_data) #zaloguj
read = s.get('https://zslpoznan.mobidziennik.pl/mobile/planlekcji?typ=podstawowy&kolejny_tydzien=1') #pobierz plan lekcji

text = re.sub('<[^<]+?>', '', read.text) #usun html
text = text.translate(str.maketrans('', '', string.whitespace)) #usun wszystkie znaki biale

text = text.replace(start, "", 1) #usun pierwszy duplikat tego slowa
text = text[text.index(start):text.index(koniec)].replace(start,"",1) #daj wszystko oprocz poczatku i konca

tydzien = text[:text.index(startdata)] #wypisz jaki tydzien
print(tydzien)

for i in range(0,5):
	text = text[text.index(dzien):].replace(dzien,"",1) #odpal dzien
	
	data = text[0:2]
	j=2
	jestWolne = False
	while(not text[j].isdigit()): #zdobadz date
		if(text[j:j+len(wolne)]==wolne):
			jestWolne = True
			break
		data += text[j]
		j+=1
	print(data)
	text = text.replace(data, "")
	if(jestWolne):
		print("JEST WOLNE!!!!!!!")
		continue

	while(True):
		if(text[11:11+len(odwolane)] == odwolane):
			text = text[text.index(")")+1:]
		else:
			godzina = text[0:11]
			print(godzina)
			text = text[11:]
			break
