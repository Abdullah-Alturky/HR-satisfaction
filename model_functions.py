import pickle
import pandas as pd

# import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    classification_report,
    r2_score,
    accuracy_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


model = None
with open("./storage/model.bin", "rb") as f:
    model = pickle.load(f)
    # print(model.predict())

def num_pipeline_transformer(data):
    '''
    Function to process numerical transformations
    Argument:
        data: original dataframe
    Returns:
        num_attrs: numerical dataframe
        num_pipeline: numerical pipeline object

    '''
    numerics = ['int64','float64']

    num_attrs = data.select_dtypes(include=numerics)

    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),
        ])##what is insid the function?
    return num_attrs, num_pipeline
# Complete transformation for categorical and numeric data
def pipeline_transformer(data):
    '''
    Complete transformation pipeline for both
    nuerical and categorical data.

    Argument:
        data: original dataframe
    Returns:
        prepared_data: transformed data, ready to use
    '''
    cat_attrs = ["Department","GEO","Role","salary","Gender"]
    num_attrs, num_pipeline = num_pipeline_transformer(data)
    global full_pipeline
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, list(num_attrs)),
        ("cat", OneHotEncoder(), cat_attrs),
        ])
    prepared_data = full_pipeline.fit_transform(data)
    return prepared_data



def predict_attrition(config):
    if type(config) == dict:
        df_prep = config.copy()
        df = pd.DataFrame(df_prep, index=[0])

    else:
        df = config.copy()
    

    # Read in and filter out columns from original data for use for the pipe
    attrition_df_temp = pd.read_csv("./storage/HR.csv")
    data_temp = attrition_df_temp.copy()
    data_temp_dropped_X = data_temp.drop(['ID', 'Name','Will_Relocate','number_project','average_montly_hours','Emp_Satisfaction'], axis=1)
    data_temp_dropped_Y = data_temp["Emp_Satisfaction"].copy()
    # Run pipeline_transformer once to make full_pipeline available for make_pipeline

    _ = pipeline_transformer(data_temp_dropped_X)

    pipe = make_pipeline(full_pipeline, model)

    # Fit the pipe onto the original data to remember possible values for each categorical feature
    pipe.fit(data_temp_dropped_X, data_temp_dropped_Y)

    y_pred = pipe.predict(df)

    probability = pipe.predict_proba(df)

    if y_pred >= 5:
      st=1
    else:
      st=0
    return st
