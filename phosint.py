import re
import sys

import cloudscraper
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

regex = re.compile(r"\+?\d?([0-9]{3})-?([0-9]{3})-?([0-9]{4})", re.UNICODE)

def banner(number: int) -> None:
	print(f"""
{Fore.LIGHTGREEN_EX + Style.BRIGHT} _____  _               _       _   
{Fore.LIGHTGREEN_EX + Style.BRIGHT}|  __ \| |             (_)     | |  
{Fore.LIGHTGREEN_EX + Style.BRIGHT}| |__) | |__   ___  ___ _ _ __ | |_ 
{Fore.LIGHTGREEN_EX + Style.BRIGHT}|  ___/| '_ \ / _ \/ __| | '_ \| __|
{Fore.LIGHTGREEN_EX + Style.BRIGHT}| |    | | | | (_) \__ \ | | | | |_ 
{Fore.LIGHTGREEN_EX + Style.BRIGHT}|_|    |_| |_|\___/|___/_|_| |_|\__|

	Target -> {Fore.RED}{number}

	{Fore.RESET}""")

def caller_id(number: str) -> None:
	if len(number) >= 11:
		number = str(number[len(number) - 10:])
	number = int('1' + ''.join(regex.match(str(number)).groups()))
	resp = requests.post("https://api.calleridtest.com/freebie", json={"number": number}).json()
	if resp.get("status") == "success":
		provider = resp.get("data").get("data").get("lrn").get("company")
		city = resp.get("data").get("data").get("lrn").get("rc")
		state = resp.get("data").get("data").get("lrn").get("state_full_name")
		name = resp.get("data").get("data").get("cnam").get("name")
	else:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch caller info{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Caller ID ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Location ] --> {Fore.LIGHTRED_EX}{city}, {state}{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Provider ] --> {Fore.LIGHTRED_EX}{provider}{Fore.RESET}")

def zaba_search(number: int) -> None:
	scraper = cloudscraper.create_scraper()
	if len(number) >= 11:
		number = str(number[len(number) - 10:])
	resp = scraper.get("https://www.zabasearch.com/phone/{0}".format(number)).text
	soup = BeautifulSoup(resp, 'html.parser')
	try:
		record_count = soup.find("div", attrs={'class': "resultsbox"}).find("h1").text
		records = soup.find("div", attrs={'class': "sub-container"}).find_all("section", attrs={'class': "person people-results resultsbox"})
		print(f"\n{Fore.BLUE + Style.BRIGHT}[ Zaba Search ] {record_count}{Fore.RESET}")
		for record in records:
			name = record.find("a", attrs={'class': "name-link"}).text.strip()
			pi = record.find_all("p")
			age = pi[0].text.split("Age: ")[1]
			addy = pi[1].text
			print(f"\n{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Name ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}")
			print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Age ] --> {Fore.LIGHTRED_EX}{age}{Fore.RESET}")
			print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Address ] --> {Fore.LIGHTRED_EX}{addy}{Fore.RESET}")
	except AttributeError as e:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch info from ZabaSearch - {Fore.RED}{e}{Fore.RESET}")

def us_phone_book(number: int) -> None:
	scraper = cloudscraper.create_scraper()
	if len(number) >= 11:
		number = str(number[len(number) - 10:])
	number = str('-'.join(regex.match(str(number)).groups()))
	resp = scraper.get("https://www.usphonebook.com/{0}".format(number)).text
	soup = BeautifulSoup(resp, 'html.parser')
	try:
		name = " ".join([elem.text.strip() for elem in soup.find("span", attrs={"itemprop": "name"}).find_all("strong")])
		url = "https://www.usphonebook.com" + soup.find("a", attrs={"class": "ls_contacts-btn"}).attrs["href"].strip()
		print(f"\n{Fore.BLUE + Style.BRIGHT}[ US Phone Book ]{Fore.RESET}")
		print(f"\n{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Name ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}")
		print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Url ] --> {Fore.LIGHTRED_EX}{url}{Fore.RESET}")
	except AttributeError as e:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch info from USPhoneBook - {Fore.RED}{e}{Fore.RESET}")

def main() -> None:
	banner("({0}) {1}-{2}".format(*regex.match(str(sys.argv[1])).groups()))
	caller_id(sys.argv[1])
	zaba_search(sys.argv[1])
	us_phone_book(sys.argv[1])

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"{Fore.RED}You must only specify a phone number !{Fore.RESET}")
		sys.exit(1)
	if not bool(regex.match(sys.argv[1])):
		print(f"{Fore.RED}That is not a valid phone number{Fore.RESET}")
		sys.exit(1)
	main()
