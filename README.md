__Update as of 13/03/2020:__
- Although a good blue print has been formulated, I am in the process of acquiring more data as well as performing further research on the features that showed promise in order to build a robust predictive model.
- Added an interactive plot displaying country-wise temperature change.

# Climate-WorldBank (Beta)

Analysis of raw macroeconomic data to explore potential links with global warming

### Temperature change snapshot
Following link gives a quick snapshot of the country-wise magnitude of temperature change over the period 1901-2012: ([Interactive Temp Change](https://wbplot.s3.amazonaws.com/tp.html)). This was a mini project on its own; the code is available here: ([Plot Code](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/Interactive%20Plot.py))

## Data Source
World Bank's (WB) APIs are an excellent free resource for macroeconomic data. All the data used in the project has been obtained either from WB's Indicators API or their Climate API.

## Objective
Discussion on the issue of climate change has become fairly ubiquitous in recent times. One of the most salient aspects of this discussion is the occurrence of global warming which is often designated as the cause of several natural disasters such as floods etc. One of the major points of contention with regards to the issue of global warming is the extent of it being anthropogenic (man-made). This project aims to explore links between global macroeconomic/social indicators and changes in temperature during the period 1960-2012. The final plan is to develop a framework which users can deploy to perform analysis of their own using their desired indicators from the World Bank API.

## Project Overview
The project can be divided into 4 major phases as follows:
- Phase 1: Data extraction
- Phase 2: Exploratory data analysis / Data cleaning
- Phase 3: Modeling
- Phase 4: Interpretive Data Analysis

### Phase 1 ([WB Scraper](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/World%20Bank%20DB%20Scraper.py))
- __Introduction__: Macroeconomic data (Independent Features) were obtained from World Bank's Indicators API; it was accessed using wbdata library for python. Temperature data (Target Feature) was obtained using World Bank's climate API; it was accessed using wbpy library.
- __Process__:
1. World Bank's database has regional data. The primary regional division used is countries. The API requires country code commands when requesting data. Thus, forming a list of countries was the first stage.
2. The second major requirement is the Indicator code needed by the API which tells it to provide the requested macroeconomic indicator (for instance GDP per capita). Thus, a dictionary of indicators was developed.
3. Temperature data (Target feature) was obtained from a separate API; the WB climate API.

### Phase 2 ([WB DataCleaning](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/WB%20Data%20Cleanup.py))

The extracted data had two major issues: sparseness (high number of missing values) & multicollinearity. There were several steps involved in the cleaning process, many of them were based on close examination of the data. Details can be found in the EDA notebook ([EDA](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/EDA.ipynb)).

### Phase 3 ([WB Modeling](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/WB%20Modeling.py))

At this stage, machine learning was primarily used to assist interpretive data analysis. Given the high number of features relative to training examples (high dimensionality), a predictive model was built and optimized primarily to identify important features from the dataset.
After trying several methods of dealing with missing values ranging from complete removal to multiple forms of imputation, it was clear that complete removal/imputation of missing values would alter the data too significantly. Thus, choice of algorithm was simple - XGboost - one of the few algos that works with missing values. Another major reason was the feature importance ranking capability of XGboost which is vital given the project's objectives. However, eventually, as more data becomes available, a full scale predictive model can be developed.

### Phase 4 ([WB Interpretation](https://github.com/InsciteAnalytics/Climate-WorldBank/blob/master/IDA.ipynb))

Due to the size of the dataset, complete reliance on the feature importance function would have been problematic. However, its still a great starting point as compared to exhaustive univariate/bivariate plotting and analyses which are often inconclusive.
