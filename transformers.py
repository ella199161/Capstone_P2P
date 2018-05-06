import pandas as pd
import numpy as np
import os
import datetime
import time
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import roc_curve, auc, confusion_matrix
from datetime import timedelta, datetime
import math
from sklearn.preprocessing import LabelEncoder, OneHotEncoder 
from sklearn import base
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion

class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_names):
        self.col_names = col_names  # We will need these in transform()
    
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self
    
    def transform(self, X):   
            # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        return X[self.col_names]

class CreditTimeTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, credit_L, issued):
        self.credit_L = credit_L  # We will need these in transform()
        self.issued = issued
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self
    
    def transform(self, X):   
            # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        X.loc[:,self.credit_L] = pd.to_datetime(X[self.credit_L])
        X.loc[:,self.issued] = pd.to_datetime(X[self.issued])
        X.loc[:,self.credit_L] = (X[self.issued] - X[self.credit_L]).apply(lambda x: x.days)
        
        return X
    
    
class NaInputeTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, zerox_inp, mean_inp, maj_inp):
        self.zerox_inp = zerox_inp
        self.mean_inp = mean_inp
        self.maj_inp = maj_inp
        pass  
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):   
        for i in self.zerox_inp:
            X[i].fillna(0, inplace = True)
        for i in self.mean_inp:
            X[i].fillna(X[i].mean(skipna = True), inplace = True)
            
        for i in self.maj_inp:
            
            X_group = X.groupby(i).size()
            maj = X_group[X_group == X_group.max()].index[0]
            X[i].fillna(maj, inplace = True)
        return X
cata = ['addrstate', 'purpose', 'homeownership']
columns_keep = ['addrstate','annualinc','chargeoffwithin12mths','delinq2yrs', 'purpose',
                'delinqamnt', 'dti','earliestcrline','emplength','ficorangehigh','pubrec',
               'installment','intrate','loanamount', 'numoprevtl', 'numrevaccts',
       'homeownership','numbcsats','revolbal','revolutil','taxliens','totcurbal'
               ]
zerox_inp = ['chargeoffwithin12mths','delinq2yrs', 'delinqamnt','emplength',
             'numoprevtl', 'numrevaccts','numbcsats','pubrec','revolbal',
             'revolutil','taxliens','totcurbal'
            ]
mean_inp = ['ficorangehigh','annualinc','dti']
maj_inp = ['addrstate','purpose', 'homeownership', 'earliestcrline']

pipe = Pipeline([
    ('ctt', CreditTimeTransformer('earliestcrline', 'issued')),
    ('cst', ColumnSelectTransformer(columns_keep)),
    ('nit', NaInputeTransformer(zerox_inp, mean_inp, maj_inp))
])

class EstimatorTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, estimator):
        self.estimator = estimator
        # What needs to be done here?
    
    def fit(self, X, y):
        self.estimator.fit(X,y)
        return self
        # Fit the stored estimator.
        # Question: what should be returned?
    
    def transform(self, X):
        
        return self.X

class ColumnUnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_names):
        self.col_names = col_names  # We will need these in transform()
    
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self
    
    def transform(self, X):   
            # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        return X.drop(self.col_names, axis = 1)

class OneColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col_name):
        self.col_name = col_name  # We will need these in transform()
    
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self
    
    def transform(self, X):   
            # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        return X[self.col_name].values

class MyLabelEncoder(LabelEncoder):
    def fit(self, X, y=None):
        super( MyLabelEncoder, self).fit(X)
        return self #
    def fit_transform(self, X, y=None):
        return super( MyLabelEncoder, self).fit_transform(X)

class ReshapeTransformer(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self):
         # We will need these in transform()
        pass
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self
    
    def transform(self, X):   
            # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        return X.reshape(-1, 1)

purpose_pipe = Pipeline([('cst1', OneColumnSelectTransformer('purpose')),
    ('lab', MyLabelEncoder()),
    ('rft', ReshapeTransformer()),                     
    ('ohe', OneHotEncoder(sparse=False))
                        ])

homeownership_pipe = Pipeline([('cst1', OneColumnSelectTransformer('homeownership')),
    ('lab', MyLabelEncoder()),
    ('rft', ReshapeTransformer()),                     
    ('ohe', OneHotEncoder(sparse=False))
                        ])


union =  FeatureUnion([
    ('cust', ColumnUnSelectTransformer(cata)),
    ('purpose_pipe', purpose_pipe),
    ('homeownership_pipe', homeownership_pipe)
   # ('addrstate_pipe', addrstate_pipe)
    ])

full_pipe = Pipeline([
    ('pipe_clean', pipe),
    ('pipe_enc', union),
    ('clf', LogisticRegression(class_weight='balanced'))
])