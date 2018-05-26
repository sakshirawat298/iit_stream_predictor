import pandas as pd
import argparse
import mysql.connector
from datetime import datetime


class Stream(object):
    """
    Stream class to predict the stream given rank and category.
    """
    def __init__(self, data_path):
        
        #Loading data and asking for inputs
        self.load_data(data_path)
        self.inputs()
        
    def load_data(self, data_path):
        """
        Function to Load data from CSV file for digging out eligible Institutes and Programmes/Streams
        """
        df = pd.read_csv(data_path)
        df = df.dropna()
        df['Category'] = df['Category'].str.lower()
        df['Opening Rank'] = df['Opening Rank'].apply(lambda x: int(x))
        df['Closing Rank'] = df['Closing Rank'].apply(lambda x: int(x))
        self.df = df
    
    def predict(self):
        """
        Function to generate a list of eligible Institutes along with Stream names for the candidate
        """
        df_final = self.df[(self.df['Category'] == self.category.lower()) & (self.df['Closing Rank'] > self.rank)]
        
        self.institutes = df_final['Institute Name'].tolist()
        self.programs = df_final['Program Name'].tolist()
        
        if self.institutes:
            print ("Results : \n")
            print (df_final[['Institute Name', 'Program Name']])
            self.push_to_sql()
        else:
            print ("\nSorry, Couldnt find Stream")
        
    
    def push_to_sql(self):
        """
        Function to push the log/result data to mysql db
        """
        cnx = mysql.connector.connect(user='root', password='sakshi298',
                              host='127.0.0.1',
                              database='python_db')
        
        cur = cnx.cursor()
        date = str(datetime.now()).split()[0]
        for i,p in zip(self.institutes, self.programs):
            
            cur.execute("INSERT INTO stream_logs VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"\
                        .format(date, self.name, self.rank, self.category, i, p))
        print ("Logged into MySql...")
        cnx.commit()
        cnx.close()
        
        
    def inputs(self):
        """
        Taking inputs from the user in console mode
        """
        self.name = raw_input("Enter your name :\n")
        self.rank = input("Enter your Rank :\n")
        self.category = raw_input("Enter your category :\n")
        
def main(argv=None):
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank',
                        type=int,
                        help='Specify Rank of the candidate')
    
    parser.add_argument('--category', 
                        type=str,
                        help='Specify the Category of the candidate : General, OBC, SC, ST')

    args, _ = parser.parse_known_args(argv)    
    
    predictor = Stream('iit_data.csv')
    predictor.predict()
    
if __name__ == '__main__':
    
    main()
    