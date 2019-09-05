import pandas as pd
import numpy as np
import json
import pickle
from sklearn.preprocessing import StandardScaler

class data_cleanup(world_bank_scraper):
    # The extracted Df had 2 major issues: sparseness, multicollinearity.

    # Returns a dict of Dfs extracted earlier
    def get_Dfs_dict(self):
        self.Dfs={'Df'+str(i):pd.read_pickle(str(i)) for i in range(0,34,1)}
        return self.Dfs

    # Forms one consolidated Df
    def form_cons_Df(self):
        self.Train=self.Dfs.get('Df0')
        DoneDfs=['Df0']
        for i,j in self.Dfs.items():
            if i not in DoneDfs:
                a=pd.merge(self.Train,j,on=['country','date'],how='left')
                DoneDfs.append(i)
                self.Train=a
        return self.Train

    # Removing features with 80% or greater missing values
    def remove_highMV_feats(self):
        MV=self.Train.isnull().sum()
        droplist=[i for i,j in MV.items() if (j/len(self.Train))>=0.8]
        self.Train.drop(labels=droplist,axis=1,inplace=True)
        return self.Train

    #Removing multicollinearity in excess of 90%
    def remove_highcoll_feats(self):
        corr_matrix = self.Train.corr().abs()
        uppertrian = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in uppertrian.columns if any(uppertrian[column] > 0.90)]
        self.Train.drop(labels=to_drop,axis=1,inplace=True)
        return self.Train
