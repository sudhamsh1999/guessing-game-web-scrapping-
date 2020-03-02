import requests,random,pyfiglet
url = "https://icanhazdadjoke.com/search"
print(pyfiglet.figlet_format("DAD JOKES"))
user_input=input("What kind of joke do you want to hear?: ")
response = requests.get(
	url, 
	headers={"Accept": "application/json"},
	params={"term": str(user_input) , "limit": 20}
)

data = response.json()
x=len(data["results"])
if x>0:
	print(f"there are totally {x} jokes & here's one for you: ")
	print(random.choice(data["results"])['joke'])
else :
	print("sorry no results found")