#--------------------- To parse and get the list of Menu for a restaurant -----------------
import urllib2
from bs4 import BeautifulSoup
import datetime as dt  

# page = urllib2.urlopen("http://hospitality.usc.edu/residential-dining-menus//?menu_venue=venue-514&menu_date=03/03/2017");
def getSpeech(dinningHall, meal):
	page = "";
	date = dt.datetime.today().strftime("%m/%d/%Y")
	if dinningHall == "Cafe 84":
		page = "http://hospitality.usc.edu/residential-dining-menus//?menu_venue=venue-507&menu_date=" + str(date);
	elif dinningHall == "Parkside":
		page = "http://hospitality.usc.edu/residential-dining-menus/?menu_venue=venue-518&menu_date=" + str(date);
	elif dinningHall == "EVK":
		page = "http://hospitality.usc.edu/residential-dining-menus//?menu_venue=venue-514&menu_date=" + str(date);
	print page;
	mealno = 0;
	if (meal == "brunch"):
		mealno = int(1);
	elif (meal == "lunch"):
		mealno = int(2)
	elif (meal == "dinner"):
		mealno = int(3)

	menu = getMenu(page, mealno);

	speechFinal = "At " + dinningHall + " for " + meal + ". ";
	# print menu;
	speech = "";
	for menuItem in menu[1]:
		speech += "At " + str(menuItem[0]) + ", ";
		for i in menuItem[1][:-1]:
			speech += str(i) + ", ";
		speech += "and " + menuItem[1][-1] +". ";

	if (speech == ""):
		speechFinal = "At " + dinningHall + " they are not serving " + meal + " today.";
	print speechFinal;



def getMenu(page, mealnum):
	soup = BeautifulSoup(urllib2.urlopen(page), "lxml")
	menu = soup.find("div", { "class" : "fw-accordion-content dining-location-accordion row" })
	[s.extract() for s in menu('span')]
	mydivs = menu.findAll("div", {"class": "col-sm-6 col-md-4"});
	finalMenu = [];
	for div in mydivs:
		meal =  div.find("h3", {"class": "menu-venue-title"}).getText();
		subs = div.findAll("h4");
		allLists = div.findAll("ul");
		allsublists = [];
		count = 0;
		for i in subs:
			if (str(i.getText())=="No items for this date"):
				continue;
			items = [];
			for item in allLists[count]:
				items.append(str(item.getText()))
			count+=1;
			items;
			allsublists.append((str(i.getText()), items))
		finalMenu.append((str(meal), allsublists));
	# print mealnum;
	return finalMenu [int(mealnum)];
	# return finalMenu[int(mealnum)];

getSpeech("EVK", "brunch");


