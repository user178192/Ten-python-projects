from urllib import urlopen
import urlparse
import textwrap
import re

#reference : Beginning Python: From Novice to Professional - Project 3: In The News
#reference : http://www.youtube.com/watch?v=SFas42HBtMg


# Number of seconds in one day
day = 24 * 60 * 60


class NewsAgent:
        '''
        An object that can distribute news items from news
        sources to news destinations.
        '''
        def __init__(self):
                self.sources = []
                self.destinations = []

        def addSource(self, source):
                self.sources.append(source)

        def addDestination(self, dest):
                self.destinations.append(dest)

        def distribute(self):
                '''
                Retrieve all news items from all sources, and
                Distribute them to all destinations.
                '''
                items = []
                for source in self.sources:
                        items.extend(source.getItems())
                for dest in self.destinations:
                        dest.receiveItems(items)


class NewsItem:
        '''
        A simple news item consisting of a title and a body text.
        '''
        def __init__(self, title, body):
                self.title = title
                self.body = body


class SimpleWebSource:
        '''
        A news source that extracts news items from a Web page using
        regular expressions.
        '''
        def __init__(self, url, titlePattern, bodyPattern):
                self.url = url
                self.titlePattern = re.compile(titlePattern)
                self.bodyPattern = re.compile(bodyPattern)

        def wrap(self, string, max=70):
                '''
                Wraps a string to a maximum line width.
                '''
                return '\n'.join(textwrap.wrap(string)) + '\n'

        def getItems(self):
                text = urlopen(self.url).read()
                #print text
                titles = self.titlePattern.findall(text)
                print titles
                bodies = self.bodyPattern.findall(text)

                for title, body in zip(titles, bodies):
                        yield NewsItem(title, self.wrap(body))


class HTMLDestination:

        def __init__(self, filename):
                self.filename = filename

        def receiveItems(self, items):
                out = open(self.filename, 'w')
                print >> out, '''
                <html>
                <head>
                 <title>The Tv Schedule</title>
                </head>
                <body>
                <h1>The Tv Schedule</hi>
                '''

                print >> out, '<ul>'
                id = 0
                for item in items:
                        id += 1
                        print >> out, '<li><a href="#">%s</a></li>' % (id, item.title)
                print >> out, '</ul>'

                id = 0
                for item in items:
                        id += 1
                        print >> out, '<h2><a name="%i">%s</a></h2>' % (id, item.title)
                        print >> out, '<pre>%s</pre>' % item.body

                print >> out, '''
                </body>
                </html>
                '''


def runDefaultSetup():
        agent = NewsAgent()
        tv_url = 'http://www.tv.com/'
        tv_title = r'<title.*?\/title>'
        tv_schedule = r'<div id=\"episode_listing\".*?\/div>'
        # ge news from url
        tv = SimpleWebSource(tv_url, tv_title, tv_schedule)

        agent.addSource(tv)
        #create the html file for the news
        agent.addDestination(HTMLDestination('tv.html'))
        agent.distribute()

if __name__ == '__main__':
        runDefaultSetup()
