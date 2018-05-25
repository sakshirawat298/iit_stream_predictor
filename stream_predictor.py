import pandas as pd
import argparse

class Stream(object):
    """
    Stream class to predict the stream given rank and category.
    """
    def __init__(self, data_path):
        #Loading data
        self.load_data(data_path)
        
    def load_data(self, data_path):
        df = pd.read_csv('iit_data.csv')
        df = df.dropna()
        df['Category'] = df['Category'].str.lower()
        df['Opening Rank'] = df['Opening Rank'].apply(lambda x: int(x))
        df['Closing Rank'] = df['Closing Rank'].apply(lambda x: int(x))
        self.df = df
    
    def predict(self, rank, category):
        df_final = self.df[(self.df['Opening Rank'] < rank) & (self.df['Closing Rank'] > rank)]
        
        print (df_final[['Institute Name (Course Name)', 'Program Name']])
        
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
    predictor.predict(args.rank, args.category.lower())
    
if __name__ == '__main__':
    
    main()
    