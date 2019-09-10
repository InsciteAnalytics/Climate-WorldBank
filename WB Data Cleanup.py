import pandas as pd
import numpy as np
import json
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

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

    # Removing multicollinearity in excess of 90%
    def remove_highcoll_feats(self):
        corr_matrix = self.Train.corr().abs()
        uppertrian = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in uppertrian.columns if any(uppertrian[column] > 0.90)]
        self.Train.drop(labels=to_drop,axis=1,inplace=True)
        return self.Train

    # Adding target feature to Df & removing rows where Temp(C) is NaN
    def target_feat_merge(self):
        self.Train=pd.merge(self.Train,self.ClimateDf,on=['country','date'])
        emptytarget=self.Train[self.Train['Temp(C)'].isnull()].index
        self.Train.drop(index=emptytarget,inplace=True)
        self.Train.reset_index(inplace=True)
        self.Train.drop(labels='index',axis=1,inplace=True)
        return self.Train

    # Remove countries with over 90% missing values
    def remove_highMV_countries(self):
        indices=[self.Train[self.Train['country']==i].index for i,j in self.Train.groupby('country') if (j.isnull().sum().mean()/len(j))>=0.9]
        droplist=[a for i in indices for a in i]
        self.Train.drop(index=droplist,inplace=True)
        self.Train.reset_index(inplace=True)
        self.Train.drop(labels='index',axis=1,inplace=True)
        return self.Train

    # Countrywise Standardisation of Df, excluding date, country and target feature
    def countrywise_standardisation(self):
        CountryWiseDf={s:d for s,d in self.Train.groupby('country')}
        cols=self.Train.columns.tolist()
        cols=cols[+2:-1]+cols[:+2]+cols[-1:]
        self.StandardisedDfs={}
        for s,d in CountryWiseDf.items():
            ctr=ColumnTransformer([('strange',StandardScaler(),[i for i in d.columns if i not in ['country','date','Temp(C)']])],verbose=True,remainder='passthrough')
            strain=ctr.fit_transform(d)
            strain=pd.DataFrame(strain,columns=cols)
            self.StandardisedDfs[s]=strain
        return self.StandardisedDfs

    # Converting Temp(C) values to indices base year 1960
    def temp_to_index(self):
        for i,g in self.StandardisedDfs.items():
            base=float(g[g['date']=='1960']['Temp(C)'])
            g['Temp(C)']=g['Temp(C)']-base
        newdfs=[j for i,j in StandardisedDfs.items()]
        self.Train=pd.concat(newdfs)
        self.Train=self.Train.infer_objects()
        return self.Train
