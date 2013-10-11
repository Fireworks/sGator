from django.core.management.base import BaseCommand, CommandError
from course.models import Course
import HTMLParser
import urllib2
import re
import string
from bs4 import BeautifulSoup
from pyquery import PyQuery



class Command(BaseCommand):
    args = ''
    help = 'Updates the Database'

    def handle(self, *args, **options):
                
            url = "http://www.registrar.ufl.edu/soc/201308/all/"
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            list1 = list()      # list of categories
            list2 = list()      #list of website endings
            soup2 = [option.get('value') for option in soup.findAll('option')]
            contents = [str(x.text) for x in soup.find_all('option')]
            x = 0
            for value in contents:
                # all option values all DEPARTMENTS
                list1.append(value)
    
            for value in soup2:
                # all endings for the web addresses per department 
                list2.append(value)

            for idx, website in enumerate(list2):
                temp1 = website.strip()
                if not not temp1:
                    print "OPENING: " + url + website
                    page = urllib2.urlopen(url+ website)
                    pages = str( page.read()) 
                    
                    started = False
                    moveA = False
                    y = 0
                    g = Course('0','0','0','0','0','0','0','0','0','0','0','0','0','0','0')
                    pq = PyQuery(pages)
                    tag = pq('td')
                    index = list2.index(website)
                    
                    for c in  pq('td'):
                        if (pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " "):
                                y = 0
                                x= x+1
                                if g.name != '0':
                                    g.dept = list1[index] # Department added to each course
                                    g.save()
                                    
                                g = Course(x,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ')
                                
                                g.name = pq(c).text()
                                started = True
                                moveA = False
                                
                        if (not (pq(c).text().__len__() == 8 and pq(c).text()[3:4] == " ") or (pq(c).text().__len__() == 9 and pq(c).text()[3:4] == " ")) and started == True:
                                y = y+1        
                                if y == 7 and moveA != True:
                                     g.lday = pq(c).text()
                                if y == 21 and moveA != True:
                                     g.dday = pq(c).text()
                                if y == 22 and moveA != True:
                                     g.dtime = pq(c).text()
                                if y == 23 and moveA != True:
                                     g.dbuild = pq(c).text()
                                if y == 24 and moveA != True:
                                     g.droom = pq(c).text()
                                if y == 5 and moveA != True:
                                     if (len(pq(c).text()) == 0) or (len(pq(c).text()) == 1):
                                             moveA = True
                                     else: g.section = pq(c).text()
                                if y == 6 and moveA != True:
                                     g.cedits = pq(c).text()
                                if y == 8 and moveA != True:
                                     g.ltime = pq(c).text()
                                if y == 9 and moveA != True:
                                     g.lbuild = pq(c).text()
                                if y == 10 and moveA != True:
                                     g.lroom = pq(c).text()
                                if y == 12 and moveA != True:
                                    g.cname = pq(c).text()
                                if y == 13 and moveA != True:
                                    g.cinst = pq(c).text()

                                if y == 6 and moveA == True:
                                     g.section = pq(c).text()
                                if y == 7 and moveA == True:
                                     g.cedits = pq(c).text()
                                if y == 9 and moveA == True:
                                     g.ltime = pq(c).text()
                                if y == 22 and moveA == True:
                                     g.dday = pq(c).text()
                                if y == 23 and moveA == True:
                                     g.dtime = pq(c).text()
                                if y == 24 and moveA == True:
                                     g.dbuild = pq(c).text()
                                if y == 25 and moveA == True:
                                     g.dbuild = pq(c).text()
                                if y == 8 and moveA == True:
                                     g.lday = pq(c).text()
                                if y == 10 and moveA == True:
                                     g.lbuild = pq(c).text()
                                if y == 11 and moveA == True:
                                     g.lroom = pq(c).text()
                                if y == 13 and moveA == True:
                                     g.cname = pq(c).text()
                                if y == 14 and moveA == True:
                                     g.cinst = pq(c).text()

