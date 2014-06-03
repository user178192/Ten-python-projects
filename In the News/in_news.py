from urllib import urlopen
import textwrap
import re

#reference : Beginning Python: From Novice to Professional - Project 3: In The News

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
                titles = self.titlePattern.findall(text)
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
                 <title>Today's News</title>
                </head>
                <body>
                <h1>Today's News</hi>
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
        times_url = 'http://www.nytimes.com/'
        times_title = r'(?s)a href="[^"]*">\s*<b>\s*(.*?)\s*</b>'
        times_body = r'(?s)</a>\s*<br/>\s*(.*?)\s*<'
        # ge news from url
        times = SimpleWebSource(times_url, times_title, times_body)

        agent.addSource(times)

        #create the html file for the news
        agent.addDestination(HTMLDestination('news.html'))

        #agent.distribute()

if __name__ == '__main__':
        runDefaultSetup()
