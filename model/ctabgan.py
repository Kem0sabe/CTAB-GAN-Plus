"""
Generative model training algorithm based on the CTABGANSynthesiser

"""
import pandas as pd
import time
from model.pipeline.data_preparation2 import DataPrep
from model.synthesizer.ctabgan_synthesizer2 import CTABGANSynthesizer

import warnings

warnings.filterwarnings("ignore")

class CTABGAN():

    def __init__(self,
                 df,
                 test_ratio = 0.20,
                 categorical_columns = [ 'workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'native-country', 'income'], 
                 log_columns = [],
                 mixed_columns= {'capital-loss':[0.0],'capital-gain':[0.0]},
                 general_columns = ["age"],
                 non_categorical_columns = [],
                 integer_columns = ['age', 'fnlwgt','capital-gain', 'capital-loss','hours-per-week'],
                 problem_type= {"Classification": "income"}):

        self.__name__ = 'CTABGAN'
              
        self.synthesizer = CTABGANSynthesizer()
        self.raw_df = df
        self.test_ratio = test_ratio
        self.categorical_columns = categorical_columns
        self.log_columns = log_columns
        self.mixed_columns = mixed_columns
        self.general_columns = general_columns
        self.non_categorical_columns = non_categorical_columns
        self.integer_columns = integer_columns
        self.problem_type = problem_type
                
    def fit(self,epochs = 150):
        
        start_time = time.time()
        self.data_prep = DataPrep(self.raw_df,self.categorical_columns,self.log_columns,self.mixed_columns,self.general_columns,self.non_categorical_columns,self.integer_columns,self.problem_type,self.test_ratio)
        df = self.data_prep.df
        
        end_time = time.time()
    
        
        self.synthesizer.fit(train_data=self.data_prep.df, epochs=epochs,categorical = self.data_prep.column_types["categorical"], mixed = self.data_prep.column_types["mixed"],
        general = self.data_prep.column_types["general"], non_categorical = self.data_prep.column_types["non_categorical"], type=self.problem_type)
        return
        end_time = time.time()
        print('Finished training in',end_time-start_time," seconds.")


    def generate_samples(self,n=100,conditioning_column = None,conditioning_value = None):
        
        #TODO: self.data_prep.get_label_encoders()
        # This give the index for the label value which we are conditioning on
        # Pass the whole list for the given index to the sample method, or just pass the index for which it is relative to the ...abs
        n = 100
        column_value_index = self.data_prep.get_label_encoded(conditioning_column,conditioning_value)
        column_index = self.data_prep.df.columns.get_loc(conditioning_column)

        sample = self.synthesizer.sample(n,column_index,column_value_index) 
        sample_df = self.data_prep.inverse_prep(sample)
        
        return sample_df

    def generate_samples_index(self,n=100,index=None):

        sample = self.synthesizer.sample(n,index)
        sample_df = self.data_prep.inverse_prep(sample)

        return sample_df
