import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as metrices
from xgboost import XGBClassifier

dataset = pd.read_csv("Social_Network_Ads.csv")

dataset = dataset.drop(columns=['User ID'])

# print(dataset.head(5))

# 원핫 인코딩
enc = preprocessing.OneHotEncoder()
enc.fit(dataset.iloc[:, [0]])
onehotlabels = enc.transform(dataset.iloc[:, [0]]).toarray()
genders = pd.DataFrame({'Female': onehotlabels[:, 0], 'Male': onehotlabels[:, 1]})
result = pd.concat([genders, dataset.iloc[:, 1:]], axis=1, sort=False)
# print(result.head(5))

# 특성과 라벨 설정
y = result['Purchased']
X = result.drop(columns = ['Purchased'])

# 훈련과 테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# XGBoost 알고리즘
classifier = XGBClassifier()
classifier.fit(X_train, y_train)

XGBClassifier(
    base_score = 0.5, 
    booster = 'gbtree', 
    cosample_bylevle = 1, 
    cosample_bynode = 1, 
    cosample_bytree = 1, 
    gamma = 0, 
    learning_rate = 0.1, 
    max_delta_step = 0, 
    max_depth = 3, 
    min_child_weight = 1,
    missing = None,
    n_estimators = 100,
    n_jobs = 1,
    nthread = None,
    objective = 'binary:logistic',
    random_state = 0,
    reg_alpha = 0,
    reg_lambda = 1,
    scale_pos_weight = 1,
    seed = None,
    silent = None,
    subsample = 1,
    verbosity = 1)

y_pred = classifier.predict(X_test)
cm = metrices.confusion_matrix(y_test, y_pred)
print(cm)

accuracy = metrices.accuracy_score(y_test, y_pred)
recall = metrices.recall_score(y_test, y_pred)
precision = metrices.precision_score(y_test, y_pred)
print(accuracy, recall, precision)