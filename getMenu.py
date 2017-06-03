#--------------------- To parse and get the list of Menu for a restaurant -----------------
import urllib2
from bs4 import BeautifulSoup

page = urllib2.urlopen("http://hospitality.usc.edu/residential-dining-menus//?menu_venue=venue-514&menu_date=03/03/2017");
soup = BeautifulSoup(page, "lxml")

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

print finalMenu;


