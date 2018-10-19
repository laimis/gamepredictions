from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
import pandas as pd

def evaluate(weeks_to_roll):
    data = pd.read_csv(f"output\\{weeks_to_roll}trainingdata.csv")
    
    y = data.home_win
    X = data.drop(["home_win", "home", "away"], axis=1, inplace=False)
    
    model = joblib.load(f"models\\{weeks_to_roll}_model.pkl")
    
    y_predicted = model.predict(X)
    
    accuracy = accuracy_score(y, y_predicted)
    
    print(f"{weeks_to_roll} accuracy: {accuracy}")

evaluate(2)
evaluate(3)
evaluate(4)
evaluate(5)