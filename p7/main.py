# project: p7
# submitter: jchalem
# partner: none
# hours: 2

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score

class UserPredictor:
    def __init__(self):
        pass
    
    def clean(self, users, logs):
        # Clean train_logs, group by user id and url
        new_logs = logs.groupby(['user_id', 'url']).sum()
        new_logs['user_id'] = new_logs.index.get_level_values('user_id')
        new_logs['url'] = new_logs.index.get_level_values('url')
        new_logs.index = range(len(new_logs))

        pages = logs['url'].unique()
        for p in pages:
            combined = new_logs.loc[new_logs['url'] == p][['user_id','seconds']]
            users[p] = users.merge(combined[['user_id', 'seconds']], on = 'user_id', how = 'left')['seconds']
            users[p] = users[p].fillna(0)
        users.insert(len(users.columns), "gold", users["badge"] == "gold")
        users.insert(len(users.columns), "silver", users["badge"] == "silver")
        users.insert(len(users.columns), "bronze", users["badge"] == "bronze")
        return users
    
    def fit(self, users, logs, y):
        df = self.clean(users, logs)
        self.pipe = Pipeline([
            ("pf", PolynomialFeatures(degree = 2)),
            ("sd", StandardScaler()),
            ("lr", LogisticRegression(max_iter = 1000))
        ])

        self.pipe.fit(df[["age","past_purchase_amt","gold","silver","bronze","/keyboard.html",
                      "/blender.html","/laptop.html","/cleats.html","/tablet.html"]], y["y"])
        
        scores = cross_val_score(self.pipe, users[["age","past_purchase_amt","gold","silver","bronze","/keyboard.html",
                      "/blender.html","/laptop.html","/cleats.html","/tablet.html"]], y["y"])
        return scores.mean()
    
    def predict(self, users, logs):
        df = self.clean(users, logs)
        outcome = self.pipe.predict(df[["age","past_purchase_amt","gold","silver","bronze","/keyboard.html",
                      "/blender.html","/laptop.html","/cleats.html","/tablet.html"]])
        return outcome
    