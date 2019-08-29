import requests as r
import pickle
from itertools import islice
import inspect
from time import sleep
import pandas as pd
import numpy as np
import json
import wbdata
import wbpy
import datetime as dt
import pyreadr
import re

class world_bank_scraper:
# Scraping world bank data and forming Df required for analysis

    def __init__(self):
        pass

    # Main data to be extracted is from the WB Indicators. There are 2 options, through topics or sources.
    # Thus the first task is to view the list of topics or sources as required

# Extracts complete list of topics/sources from WB API
    @staticmethod
    def view_sources_topics():
        a=input('View list of sources or topics?')
        if a in ['sources','source','source list','sources list']:
            wbdata.get_source()
        if a in ['topic','topics','topic list','topics list']:
            wbdata.get_topic()
        else:
            print('Please enter whether you require sources or topics')

# When extracting data from world bank's API, country code needs to be specified, the following method extracts dictionary of countries and removes some
# regional aggregations that are irrelevant and would interfere with extraction of climate data

    def get_country_list(self):
        s=wbdata.get_country(display=False)
        a = {c.get('id'):c.get('iso2Code') for c in s}
        b = [key for key, val in a.items() if not val[1].isdigit() if not val[0].isdigit()]
        self.countrylist = [c for c in b if c not in ('UMC','OED','MNA','LMY','LMC','LIC','LDC','EMU','NAC','SSA',\
                                 'LAC','LCN','INX','IDX','IDB','IDA','IBT','IBD','IBB','HPC','HIC','EUU','SSF',\
                                                  'MIC','MEA','CHI')]
        return self.countrylist


 # Extracting Temperature (Target feature of the analysis) Data from World Bank Climate API
    def get_climate_data(self):
        c_api = wbpy.ClimateAPI()
        dataset1 = c_api.get_instrumental(data_type="tas", interval="year", locations=self.countrylist)
        dataset1=dataset1.as_dict()
        ClimateDf=pd.DataFrame(dataset1).unstack().reset_index()
        CountryNames={}
        for c in s:
            a=c.get('id')
            for f in self.countrylist:
                if a==f:
                    CountryNames[a]=c.get('name')
        ClimateDf['level_0']=ClimateDf['level_0'].map(CountryNames)
        self.ClimateDf=ClimateDf.rename(mapper={'level_0':'country', 'level_1':'date',0:'Temp(C)'},axis=1)
        return self.ClimateDf

# Forms a dictionary of indicator codes along with their names for later extraction of Df
## My own process was to first extract the indicators I wanted and then form one consolidated dictionary to get the Df
    def ind_dict_from_source(self,sourcelist:list):
        ind=[]
        for i in sourcelist:
            Pop=wbdata.get_indicator(source=i,display=False)
            Pop={c.get('id'):c.get('name') for c in Pop}
            ind.append(Pop)
        self.SourceInds={k:v for d in ind for k,v in d.items()}
        return self.SourceInds

    def ind_dict_from_topic(self,topiclist:list):
        ind=[]
        for i in topiclist:
            Pop=wbdata.get_indicator(source=i,display=False)
            Pop={c.get('id'):c.get('name') for c in Pop}
            ind.append(Pop)
        self.TopicInds={k:v for d in ind for k,v in d.items()}
        return self.TopicInds

# Removes duplicate indicators and combines indicators extracted from sources as well as topics
    def form_indicator_dict(self):
        self.Indicators={**self.SourceInds,**self.TopicInds}
        return self.Indicators


# After getting a dictionary, it was important to extract the indicators that were not available in the API causing error in the Df formation

    def na_indicators_del(self):
        Inds=[c for c in self.Indicators]
        X=[]
        for c in Inds:
            try:
                a=wbdata.get_data(indicator=c,'''country=countrylist''' #figure out how to handle the countrylist later)
            except:
                print(c)
                X.append(c)
                continue
        self.Indicators2={s:d for s,d in self.Indicators.items() if s not in X}
        return self.Indicators2


    def chunks(self, Indicators, SIZE):
        it = iter(self.Indicators2)
        for i in range(0, len(self.Indicators2), SIZE):
            yield {k:self.Indicators2[k] for k in islice(it, SIZE)}


    def get_Df(self):
        self.IndList= [item for item in self.chunks({i:j for i,j in self.Indicators2.items()},50)]
        its=iter(self.IndList)
        for k in range(0, len(self.IndList), 1):
            sleep(120)
            df=wbdata.get_dataframe(indicators=islice(its,1),country=self.countrylist)
            return df.to_pickle(str(k))
