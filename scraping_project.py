from csv import writer
import requests
from bs4 import BeautifulSoup
from random import choice



BASE_URL='http://quotes.toscrape.com/'

def scrape_quotes():
	url="/page/1"
	all_quotes=[]
	while url:
		request = requests.get(f"{BASE_URL}{url}")
		soup = BeautifulSoup(request.text,'html.parser')
		quotes=soup.find_all(class_='quote')

		for quote in quotes:
			q=quote.find(class_='text')
			all_quotes.append(
				{

					"text":q.get_text(),
					"author":quote.find(class_='author').get_text(),
					"bio-link":quote.find("a")['href']
				})
		next_btn=soup.find(class_='next')
		url=next_btn.find("a")["href"] if next_btn else None
		return all_quotes

def start_game(quotes):
	quote = choice(quotes)
	remaining_guesses=4
	print("Here's a quote: ")
	print(quote['text'])
	guess=''
	while guess.lower() != quote['author'].lower() and remaining_guesses>0:
		guess=input(f"Who said this quote? Guesses remaining : {remaining_guesses}  ")
		if guess.lower() == quote["author"].lower():
			print("YOU GOT IT RIGHT!")
			break
		remaining_guesses-=1
		if remaining_guesses==3:
			res=requests.get(f"{BASE_URL}{quote['bio-link']}")
			soup=BeautifulSoup(res.text,'html.parser')
			birth_date=soup.find(class_="author-born-date").get_text()
			birth_place=soup.find(class_="author-born-location").get_text()
			print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
		elif remaining_guesses==2:
			print(f"Here's is other Hint:The author's first name starts with {quote['author'][0]}")
		elif remaining_guesses==1:
			n=quote['author'].split(" ")
			print(f"Here's is other Hint:The author's last name starts with {n[1][0]}")
		else:
			print(f"Sorry you ran out of guesses. The answer was {quote['author']}")

	again = ''
	while again.lower() not in ('y', 'n', 'yes', 'no'):
		again = input("Would you like to play again(y,n)?")
	if again.lower() in ('yes','y'):
		return start_game(quotes)
	else:
		print("OK, GOODBYE!")
quotes=scrape_quotes()
start_game(quotes)