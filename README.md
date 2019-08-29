# Climate-WorldBank (Beta)
Analysis of raw macroeconomic data to explore potential links with global warming

## Data Source
World Bank's (WB) APIs are an excellent free resource for macroeconomic data. All the data used in the project has been obtained either from WB's Indicators API or their Climate API.

## Objective
Discussion on the issue of climate change has become fairly ubiquitous in recent times. One of the most salient aspects of this discussion is the occurrence of global warming which is often designated as the cause of several natural disasters such as floods etc. One of the major points of contention with regards to the issue of global warming is the extent of it being anthropogenic (man-made). This project aims to explore links between our economic activities and change in temperature during the period 1960-2012. The final plan is to develop a framework which users can deploy to perform analysis of their own using desired indicators from the World Bank API.

## Objective of current Repo
This is the development phase of the project. Following are the major goals:
- Develop the project in a way that will showcase code/insights such as to highlight skills that may be important for employers.
- Collaborate with Fan Zhang who will review the project at this stage to provide guidance aimed at achieving the above mentioned goal

## Project Overview
The project can be divided into 4 major phases as follows:
- Phase 1: Data extraction
- Phase 2: Data Cleaning
- Phase 3: Modeling
- Phase 4: Exploring

### Phase 1 ([WB Scraper](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/World%20Bank%20DB%20Scraper.py))
- __Introduction__: Macroeconomic data (Independent Features) were obtained from World Bank's Indicators API; it was accessed using wbdata library for python. Temperature data (Target Feature) was obtained using World Bank's climate API; it was accessed using wbpy library.
- __Process__:
1. World Bank's database has regional data. The primary regional division used is countries. The API requires country code commands when requesting data. Thus, forming a list of countries was the first stage.
2. The second major requirement is the Indicator code needed by the API which tells it to provide the requested macroeconomic indicator (for instance GDP per capita). Thus, a dictionary of indicators was developed.
3. Temperature data (Target feature) was obtained from a separate API; the WB climate API.
