import sys

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


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

def caller_id(number: int) -> None:
	resp = requests.post("https://api.calleridtest.com/freebie", json={"number": number}).json()
	if resp.get("status") == "success":
		provider = resp.get("data").get("data").get("lrn").get("company")
		city = resp.get("data").get("data").get("lrn").get("rc")
		state = resp.get("data").get("data").get("lrn").get("state_full_name")
		name = resp.get("data").get("data").get("cnam").get("name")
	else:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch caller info{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Name ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Location ] --> {Fore.LIGHTRED_EX}{city}, {state}{Fore.RESET}")
	print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Provider ] --> {Fore.LIGHTRED_EX}{provider}{Fore.RESET}")

def true_people_search(number: int) -> None:
	resp = requests.get("https://www.truepeoplesearch.com/resultphone?phoneno={0}".format(number)).text
	soup = BeautifulSoup(resp, 'html.parser')
	try:
		record_count = soup.find("div", attrs={'class': "row visible-left-side-visible record-count pl-1"}).find("div", attrs={'class': "col"}).text
		records = soup.find("div", attrs={'class': "content-center"}).find_all("div", attrs={'class': "card card-body shadow-form card-summary pt-3"})
		names = []
		for record in records:
			names.append(record.find("div", attrs={'class': "col-md-8"}).find("div", attrs={'class': "h4"}).text)
	except AttributeError as e:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch info from TruePeopleSearch - {Fore.RED}{e}{Fore.RESET}")
	print(f"{Fore.BLUE + Style.BRIGHT}[ Records ] {record_count}{Fore.RESET}")
	[print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Name ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}") for name in names]

def thats_them_search(number: int) -> None:
	resp = requests.get("https://thatsthem.com/phone/{0}".format(number)).text
	soup = BeautifulSoup(resp, 'html.parser')
	try:
		record_count = soup.find("div", attrs={'class': "query"}).text
		records = soup.find("div", attrs={'class': "records col-lg-8"}).find_all("div", attrs={'class': "record"})
		names = []
		for record in records:
			names.append(record.find("div", attrs={'class': "name"}).get_text())
	except AttributeError as e:
		return print(f"{Fore.YELLOW + Style.BRIGHT}[ Error ] --> Could not fetch info from ThatsThem - {Fore.RED}{e}{Fore.RESET}")
	print(f"{Fore.BLUE + Style.BRIGHT}[ Records ] {record_count}{Fore.RESET}")
	[print(f"{Fore.LIGHTBLUE_EX + Style.BRIGHT}[ Name ] --> {Fore.LIGHTRED_EX}{name}{Fore.RESET}") for name in names]

def main() -> None:
	banner(sys.argv[1])
	caller_id(sys.argv[1])
	true_people_search(sys.argv[1])
	thats_them_search(sys.argv[1])

if __name__ == "__main__":
	main()
