import pandas as pd
import numpy as np
import json
import pickle
from sklearn.preprocessing import StandardScaler

class data_cleanup(world_bank_scraper):
    # The extracted Df had 2 major issues: sparseness, multicollinearity.

    def remove_high_collinearity(self):
        
