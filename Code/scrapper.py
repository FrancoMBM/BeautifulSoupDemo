import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
import os
import sys



class Scrap:

    ''' This is a very simple scrapper that deals with ordered tables.
        This uses a practice website. If using another website make sure
        to ask permision from the webmaster first!!!.
        Note that the more messy the website and the table,
        the more difficult it is to extract
        the information.
    '''

    def __init__(self, url):

        try:

            self.req = requests.get(url)
            self.con = self.req.content
            self.soup = BeautifulSoup(self.con,"html.parser")
        except:
            print ('No connection was established or content is not available.')



        #print(self.soup.prettify())


    def get_all(self):

        ''' Getting all the information from the html tags,
            see BeautifulSoup documentation for more info
        '''

        self.all = self.soup.find_all('table', {'class': 'table table-bordered'}) # this is a list.. each number a page
        print(len(self.all))
        self.all = self.all[0] # set the list to  a tag only tags can have text attribute
        print (self.all)

    def find_columns(self):

        ''' Creating a list that will contain all the headers from the table'''

        self.cols = []
        for item in self.all.find_all('thead'):
            for t in item.find_all('th'): # the minimun unity. it will find 3 of them and save them
                self.cols.append(t.text)

    def find_rows(self):
        ''' Creating a list that contains all the rows from the table,
            The row data it is defined inside the second loop because
            each time the the second loop goes trough each individual cells,
            it continues and then goes trough the second loop. Looping trough
            tbody may seems unnecesary but it prevents creating a first empty
            row in addition to the originals.
        '''

        self.cells = []

        for item in self.all.find_all('tbody'): #
            for row in item.find_all('tr'):
                row_data = []
                for cell in row.find_all('td'):
                    row_data.append(cell.text)
                self.cells.append(row_data)

        print(self.cells)

    def create_dataframe(self, *args):

        '''Using pandas to create a dataframe and saving to disk'''

        self.user = os.path.expanduser('~')
        self.cwd =  os.path.join(self.user, *args)

        self.Data = pd.DataFrame(data = self.cells, columns = self.cols)
        #self.Data.cols = self.cells[0]
        self.Data.to_csv(os.path.join(self.cwd, 'sample_data.csv'), sep = ',')

        print(self.Data)




if __name__ == '__main__':

    S = Scrap('https://www.webscraper.io/test-sites/tables')
    S.get_all()
    S.find_columns()
    S.find_rows()
    S.create_dataframe('Desktop', 'TA_Mac', 'Scrapper', 'Data')
