###############################################################################
#here is a very hard-coded scrape of Georgia General Assembly bills
###############################################################################

# I run it every two years to scrape a two-year term's work into a local spreadsheet
# Yes, it's old Python 2 but it still works.
# 
# There are a lot of lines that have to be modified -- like for example the root url of bills
# changes every two years
# And by hand I have to switch it to srape HBs, then SBs then HRs then SRs.


from bs4 import BeautifulSoup
import mechanize
import cookielib
import time
from mechanize import ParseResponse
import urllib
import urllib2
# import lxml.html
import re
import csv
import pprint


# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "ok headers"
#--- end headers

counter = 1



#---- end declarations
output = csv.writer(open("SR.csv", "w"))

for i in range(191):
	time.sleep(10)
	url = "http://www.legis.ga.gov/Legislation/en-US/display/20152016/SR/"
	url = (url + str(counter))
	response = br.open(url)
	html = response.read()
	soup = BeautifulSoup(html)
	print "#################### URL"
	print url
	soup = soup.find("div", {'id':'content'}) #give only the div of ID=content
	print type(soup)

	# soup = soup.find("div", {'class':'item'})

	print "^^^^^^^^ PRINTING SOUP"
	# pprint.pprint(soup)



	title = soup.find("div", {"class": "ggah1"})
	print "######### TITLE"
	print title.text
	title = str(title)
	# title = title.text.encode('latin-1')
	title = title.replace("<br/>", "*")
	title = title.replace("</div>", "")
	title = title.split("*", 1)[-1]
	# print "######### SENATE SPONSORS"
	# sponsors = soup.find_all(href=re.compile('http://www.senate.ga.gov/senators/en-US/Member*'))
	# # print sponsors
	# s_sponsors = str([sponsor.parent.text for sponsor in sponsors])
	# print type(s_sponsors)
	# print "######### HOUSE SPONSORS"
	# sponsors = soup.find_all(href=re.compile('http://www.house.ga.gov/representatives/en-US/Member*'))
	# # print sponsors
	# h_sponsors = str([sponsor.parent.text for sponsor in sponsors])
	# # print h_sponsors
	print "######### HOUSE COMMITTEE"
	hcs = soup.find_all(text=re.compile('HC: '))
	h_committees = hcs[0].parent.text
	print h_committees
	# h_committees = ([hc.parent.text for hc in hcs])
	# print h_committees.encode('utf-8')
	# print "######### SENATE COMMITTEE"
	scs = soup.find_all(text=re.compile('SC: '))
	s_committees = scs[0].parent.text
	print s_committees

	print "######### DATES"
	date_section = soup.find(text=re.compile('Status History'))
	italics_tag = date_section.parent
	bold_tag = italics_tag.parent
	item = bold_tag.parent
	# print item
	list_of_dates = item.findNext('div')
	# print list_of_dates
	# print list_of_dates.find('div')
	last_status = list_of_dates.find('div')
	last_status = last_status.text.strip()
	print last_status

	# row = []
	# hoppers = soup.find_all(text=re.compile('House' ))
	# for hopper in hoppers:
	# 	up = hopper.parent.parent
	# 	# print up
	# 	# print type(up)
	# # print up
	# 	divs = up.find_all("div")
	# # print divs
	
	counter = counter + 1

	url_list = []
	url_list.append(url)
	newrow = "SR", counter-1 , url, h_committees, s_committees, last_status, title # amend this row for what u want to output
	output.writerow(newrow)

print "OK DONE **********************"

