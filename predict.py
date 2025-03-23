from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import TruncatedSVD,PCA
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, mutual_info_regression
import pandas as pd
import xgboost as xgb
from sklearn.linear_model import Ridge

def predict(model_name,df,outcome):
  all_features=df.drop(['age','a','e','o','c','n'],axis=1).columns
  corr_features=['Tops','Hair_Style','Tops_Bottom','Tops_Color','Tops_Sleeve']
  causal_features=['Tops_Color','Tops']


  y=df[outcome]
  features=[all_features,corr_features,causal_features]

  if model_name=='SVR':
    for i in range(3):
        X=df[features[i]]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)

        # Define preprocessing for categorical features (one-hot encode)
        categorical_transformer = Pipeline(steps=[
            ('pca', PCA(n_components=2)),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        # Combine preprocessing steps
        preprocessor = ColumnTransformer(
        transformers=[
          ('cat', categorical_transformer, features[i])
        ])
        X_train_transformed = preprocessor.fit_transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)


        # model = SVR(kernel='rbf')  # Using Radial Basis Function (RBF) kernel
        # model =GradientBoostingRegressor(random_state=42)
        # model = KNeighborsRegressor()
        # model=xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=3)
        model = Ridge(alpha=1.0)
        # grid_search = GridSearchCV(estimator=svr, param_grid=param_grid, cv=5, verbose=1, n_jobs=-1, scoring = {'NMSE': make_scorer(lambda y, y_pred: -mean_squared_error(y, y_pred)),  # Negating the value
        #   'R2': 'r2',
        #   'NMAE': make_scorer(lambda y, y_pred: -mean_absolute_error(y, y_pred)),  # Negating the value
        # },refit='R2',)
        # grid_search.fit(X_train, y_train)
        model.fit(X_train_transformed, y_train)
        y_pred = model.predict(X_test_transformed)
        nmse = -mean_squared_error(y_test, y_pred)

        # Calculate R-squared (R2)
        r2 = r2_score(y_test, y_pred)

        # Calculate Negative Mean Absolute Error (NMAE)
        nmae = -mean_absolute_error(y_test, y_pred)
        if i==0:
            print(f"All features")
        elif i==1:
            print(f"Correlation features")
        else:
            print(f"Causal features")



        print(nmse)  # Mean test NMSE scores for all parameter combinations
        print(r2)    # Mean test R2 scores
        print(nmae)  # Mean test NMAE scores



  elif model_name=='GBR':
    for i in range(3):
          X=df[features[i]]
          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)
          continuous_transformer = Pipeline(steps=[
          ('scaler', StandardScaler())
          ])

          # Define preprocessing for categorical features (one-hot encode)
          categorical_transformer = Pipeline(steps=[
          ('onehot', OneHotEncoder(handle_unknown='ignore'))
          ])
          # Combine preprocessing steps
          preprocessor = ColumnTransformer(
          transformers=[
              ('num', continuous_transformer, continuous_cols[i]),
              ('cat', categorical_transformer, categorical_cols[i])
          ])
          X_train_transformed = preprocessor.fit_transform(X_train)
          X_test_transformed = preprocessor.transform(X_test)

          param_grid = {
          'n_estimators': [100, 200, 300],  # Number of boosting stages to be run
          'learning_rate': [0.01, 0.1, 0.2],  # Shrinks the contribution of each tree
          'max_depth': [3, 4, 5],  # Maximum depth of the individual regression estimators
          'min_samples_split': [2, 4],  # Minimum number of samples required to split an internal node
          'min_samples_leaf': [1, 2]  # Minimum number of samples required to be at a leaf node
      }

          gbm_regressor = GradientBoostingRegressor(random_state=42)
          grid_search = GridSearchCV(estimator=gbm_regressor, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
          grid_search.fit(X_train, y_train)
          if i==0:
            print(f"All features")
          elif i==1:
            print(f"Correlation features")
          else:
            print(f"Causal features")
          print("Best parameters found: ", grid_search.best_params_)
          print("Best score (neg_mean_squared_error): ", grid_search.best_score_)

  elif model_name=='KNN':
    for i in range(3):
          X=df[features[i]]
          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)
          continuous_transformer = Pipeline(steps=[
          ('scaler', StandardScaler())
          ])

          # Define preprocessing for categorical features (one-hot encode)
          categorical_transformer = Pipeline(steps=[
          ('onehot', OneHotEncoder(handle_unknown='ignore'))
          ])
          # Combine preprocessing steps
          preprocessor = ColumnTransformer(
          transformers=[
              ('num', continuous_transformer, continuous_cols[i]),
              ('cat', categorical_transformer, categorical_cols[i])
          ])
          X_train_transformed = preprocessor.fit_transform(X_train)
          X_test_transformed = preprocessor.transform(X_test)

          param_grid = {
              'n_neighbors': [3, 5, 7, 10],  # Number of neighbors to use
              'weights': ['uniform', 'distance'],  # Weight function used in prediction
              'metric': ['euclidean', 'manhattan', 'minkowski'],  # Distance metric for tree search
          }

          knn_regressor = KNeighborsRegressor()
          grid_search = GridSearchCV(estimator=knn_regressor, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
          grid_search.fit(X_train, y_train)
          if i==0:
            print(f"All features")
          elif i==1:
            print(f"Correlation features")
          else:
            print(f"Causal features")
          print("Best parameters found: ", grid_search.best_params_)
          print("Best score (neg_mean_squared_error): ", grid_search.best_score_)

  elif model_name=='naive':
    for i in range(3):
          X=df[features[i]]
          X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)
          continuous_transformer = Pipeline(steps=[
          ('scaler', StandardScaler())
          ])

          # Define preprocessing for categorical features (one-hot encode)
          categorical_transformer = Pipeline(steps=[
          ('onehot', OneHotEncoder(handle_unknown='ignore'))
          ])
          # Combine preprocessing steps
          preprocessor = ColumnTransformer(
          transformers=[
              ('num', continuous_transformer, continuous_cols[i]),
              ('cat', categorical_transformer, categorical_cols[i])
          ])
          X_train_transformed = preprocessor.fit_transform(X_train)
          X_test_transformed = preprocessor.transform(X_test)

          parameters = {
    'vect__ngram_range': [(1, 1), (1, 2)],  # unigrams or bigrams
    'tfidf__use_idf': (True, False),
    'clf__alpha': (1e-2, 1e-3, 1e-4),
}
          pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])
          grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

          grid_search.fit(X_train, y_train)
          if i==0:
            print(f"All features")
          elif i==1:
            print(f"Correlation features")
          else:
            print(f"Causal features")
          print("Best parameters found: ", grid_search.best_params_)
          print("Best score (neg_mean_squared_error): ", grid_search.best_score_)



df=pd.read_csv('modified_merged_data.csv')
df.shape
df=df[['Tops', 'Bottom', 'Color', 'Hair_Style', 'Hair_Color', 'Sleeve',
           'Tops_Bottom', 'Tops_Color', 'Color_Sleeve', 'Tops_Sleeve',
       'Top_Color_Sleeve',  'age', 'a', 'e', 'o', 'c', 'n']]
predict('SVR',df,'e')


