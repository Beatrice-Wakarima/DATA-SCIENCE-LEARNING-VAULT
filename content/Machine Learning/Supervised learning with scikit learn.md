# Machine Learning with scikit-learn

#MachineLearning #ScikitLearn #Python #DataScience

## Table of Contents

1. [[#Introduction]]
2. [[#Data Preprocessing]]
3. [[#Model Training]]
4. [[#Model Evaluation]]
5. [[#Model Tuning]]
6. [[#Deployment Basics]]
7. [[#Capstone Project]]

---

## Introduction

Machine Learning with **scikit-learn** is one of the most popular approaches to implementing ML algorithms in [[Python for Data Science]]. Scikit-learn provides a consistent API for both [[Supervised Learning]] and [[Unsupervised Learning]] tasks.

### What is scikit-learn?

- Open-source machine learning library for Python
- Built on NumPy, SciPy, and matplotlib
- Provides simple and efficient tools for data mining and analysis
- Consistent API across different algorithms

### Key Components

- **Estimators**: Objects that fit models to data
- **Predictors**: Estimators that can make predictions
- **Transformers**: Estimators that can transform data
- **Meta-estimators**: Estimators that take other estimators as parameters

### Installation and Basic Import

```python
# Installation
# pip install scikit-learn

# Basic imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
```

### Practice Tasks - Introduction

- [ ] Install scikit-learn and import basic modules (10 XP)
- [ ] Load a sample dataset using `sklearn.datasets` (15 XP)
- [ ] Explore the structure of a scikit-learn dataset object (20 XP)

---

## Data Preprocessing

Data preprocessing is crucial for successful machine learning. Scikit-learn provides numerous tools for preparing your data.

### Loading Data

```python
from sklearn.datasets import load_iris, load_boston, fetch_california_housing
import pandas as pd

# Load sample dataset
iris = load_iris()
X, y = iris.data, iris.target

# Or load from pandas
df = pd.read_csv('your_dataset.csv')
X = df.drop('target_column', axis=1)
y = df['target_column']
```

### Train-Test Split

The **train-test split** is fundamental to machine learning - it separates your data into training and testing portions to evaluate model performance on unseen data.

```python
from sklearn.model_selection import train_test_split

# Basic split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y  # Ensures balanced distribution across classes
)

print(f"Training set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")
```

### Feature Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Important: only transform test data

# Min-Max Scaling (0-1 range)
minmax_scaler = MinMaxScaler()
X_train_minmax = minmax_scaler.fit_transform(X_train)
X_test_minmax = minmax_scaler.transform(X_test)
```

### Handling Categorical Data

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Label Encoding for target variables
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# One-Hot Encoding for features
categorical_features = ['category_col1', 'category_col2']
numeric_features = ['numeric_col1', 'numeric_col2']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ])
```

### Handling Missing Values

```python
from sklearn.impute import SimpleImputer

# Numerical imputation
num_imputer = SimpleImputer(strategy='mean')  # or 'median', 'most_frequent'
X_train_imputed = num_imputer.fit_transform(X_train)

# Categorical imputation
cat_imputer = SimpleImputer(strategy='most_frequent')
```

### Practice Tasks - Data Preprocessing

- [ ] Perform train-test split with stratification (25 XP)
- [ ] Apply StandardScaler to a dataset (20 XP)
- [ ] Handle missing values using SimpleImputer (30 XP)
- [ ] Create a preprocessing pipeline with ColumnTransformer (40 XP)

---

## Model Training

### Supervised Learning Models

#### Classification

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Logistic Regression
log_reg = LogisticRegression(random_state=42)
log_reg.fit(X_train_scaled, y_train)

# Random Forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Support Vector Machine
svm_classifier = SVC(kernel='rbf', random_state=42)
svm_classifier.fit(X_train_scaled, y_train)

# K-Nearest Neighbors
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train_scaled, y_train)
```

#### Regression

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# Linear Regression
lin_reg = LinearRegression()
lin_reg.fit(X_train_scaled, y_train)

# Ridge Regression (L2 regularization)
ridge_reg = Ridge(alpha=1.0)
ridge_reg.fit(X_train_scaled, y_train)

# Lasso Regression (L1 regularization)
lasso_reg = Lasso(alpha=1.0)
lasso_reg.fit(X_train_scaled, y_train)

# Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)
```

### Unsupervised Learning Models

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
cluster_labels = kmeans.fit_predict(X_train_scaled)

# Principal Component Analysis
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_train_scaled)

# DBSCAN Clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_train_scaled)
```

### Pipelines

**Pipelines** allow you to chain preprocessing and modeling steps together, ensuring consistent data transformation and making your code more maintainable.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Simple Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(random_state=42))
])

# Fit and predict with pipeline
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# Complex Pipeline with preprocessing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(drop='first'), categorical_features)
])

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])
```

### Practice Tasks - Model Training

- [ ] Train a logistic regression model (25 XP)
- [ ] Train a random forest classifier (25 XP)
- [ ] Create a simple pipeline with scaling and classification (35 XP)
- [ ] Train an unsupervised clustering model (30 XP)
- [ ] Build a complex pipeline with preprocessing (45 XP)

---

## Model Evaluation

### Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

# Make predictions
y_pred = pipeline.predict(X_test)
y_pred_proba = pipeline.predict_proba(X_test)[:, 1]  # For binary classification

# Basic metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

# ROC Curve (for binary classification)
if len(np.unique(y)) == 2:
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.2f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.show()
```

### Regression Metrics

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Make predictions
y_pred = regressor.predict(X_test)

# Regression metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.4f}")
print(f"Root Mean Squared Error: {rmse:.4f}")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# Prediction vs Actual plot
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predictions vs Actual Values')
plt.show()
```

### Cross-Validation

**Cross-validation** is a technique to assess how well your model generalizes to unseen data by splitting the training data into multiple folds.

```python
from sklearn.model_selection import cross_val_score, cross_validate, StratifiedKFold

# Simple cross-validation
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# More detailed cross-validation
scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
cv_results = cross_validate(pipeline, X_train, y_train, cv=5, scoring=scoring)

for score in scoring:
    scores = cv_results[f'test_{score}']
    print(f"CV {score}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Stratified K-Fold for imbalanced datasets
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
stratified_scores = cross_val_score(pipeline, X_train, y_train, cv=skf, scoring='accuracy')
```

### Practice Tasks - Model Evaluation

- [ ] Calculate and interpret classification metrics (30 XP)
- [ ] Create a confusion matrix visualization (25 XP)
- [ ] Plot ROC curve for binary classification (35 XP)
- [ ] Perform 5-fold cross-validation (40 XP)
- [ ] Compare multiple models using cross-validation (45 XP)

---

## Model Tuning

### Hyperparameter Tuning

**Hyperparameter tuning** involves finding the best combination of model parameters to optimize performance.

#### Grid Search

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [3, 5, 7, None],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Grid search with cross-validation
grid_search = GridSearchCV(
    pipeline, 
    param_grid, 
    cv=5, 
    scoring='accuracy',
    n_jobs=-1,  # Use all available processors
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")

# Use best model
best_model = grid_search.best_estimator_
```

#### Random Search

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Define parameter distributions
param_dist = {
    'classifier__n_estimators': randint(50, 200),
    'classifier__max_depth': [3, 5, 7, 10, None],
    'classifier__min_samples_split': randint(2, 20),
    'classifier__min_samples_leaf': randint(1, 10),
    'classifier__max_features': ['auto', 'sqrt', 'log2']
}

# Random search
random_search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=100,  # Number of parameter settings sampled
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
```

### Feature Selection

```python
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier

# Univariate feature selection
selector = SelectKBest(score_func=f_classif, k=5)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

# Recursive Feature Elimination
estimator = RandomForestClassifier(random_state=42)
rfe = RFE(estimator, n_features_to_select=5)
X_train_rfe = rfe.fit_transform(X_train, y_train)
X_test_rfe = rfe.transform(X_test)

# Feature importance from tree-based models
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)

feature_importance = pd.DataFrame({
    'feature': X.columns if hasattr(X, 'columns') else range(X.shape[1]),
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance.head(10))
```

### Learning Curves

```python
from sklearn.model_selection import learning_curve

# Generate learning curves
train_sizes, train_scores, val_scores = learning_curve(
    pipeline, X_train, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10)
)

# Plot learning curves
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', label='Training score')
plt.plot(train_sizes, np.mean(val_scores, axis=1), 'o-', label='Cross-validation score')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy Score')
plt.title('Learning Curves')
plt.legend()
plt.grid(True)
plt.show()
```

### Practice Tasks - Model Tuning

- [ ] Perform grid search hyperparameter tuning (40 XP)
- [ ] Compare grid search vs random search results (35 XP)
- [ ] Apply feature selection techniques (45 XP)
- [ ] Generate and interpret learning curves (35 XP)
- [ ] Optimize a complete ML pipeline (50 XP)

---

## Deployment Basics

### Model Persistence

```python
import joblib
import pickle

# Save model using joblib (recommended for scikit-learn)
joblib.dump(best_model, 'trained_model.pkl')

# Load model
loaded_model = joblib.load('trained_model.pkl')

# Alternative: using pickle
with open('model_pickle.pkl', 'wb') as f:
    pickle.dump(best_model, f)

with open('model_pickle.pkl', 'rb') as f:
    loaded_model_pickle = pickle.load(f)
```

### Creating Prediction Functions

```python
def make_prediction(model, input_data):
    """
    Make predictions on new data
    
    Parameters:
    model: trained scikit-learn model
    input_data: array-like, shape (n_samples, n_features)
    
    Returns:
    predictions: array of predictions
    probabilities: array of prediction probabilities (if available)
    """
    predictions = model.predict(input_data)
    
    # Get probabilities if available
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(input_data)
        return predictions, probabilities
    else:
        return predictions, None

# Example usage
new_data = [[5.1, 3.5, 1.4, 0.2]]  # New sample
pred, prob = make_prediction(loaded_model, new_data)
print(f"Prediction: {pred[0]}")
if prob is not None:
    print(f"Probabilities: {prob[0]}")
```

### Model Validation in Production

```python
def validate_input(input_data, expected_features):
    """Validate input data before making predictions"""
    if input_data.shape[1] != expected_features:
        raise ValueError(f"Expected {expected_features} features, got {input_data.shape[1]}")
    
    # Check for missing values
    if np.isnan(input_data).any():
        raise ValueError("Input data contains missing values")
    
    return True

def predict_with_confidence(model, input_data, confidence_threshold=0.8):
    """Make predictions with confidence checking"""
    predictions, probabilities = make_prediction(model, input_data)
    
    if probabilities is not None:
        max_probs = np.max(probabilities, axis=1)
        confident_predictions = max_probs >= confidence_threshold
        
        return predictions, probabilities, confident_predictions
    else:
        return predictions, None, None
```

### Basic Flask API Example

```python
# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model at startup
model = joblib.load('trained_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        
        # Validate input
        validate_input(features, expected_features=model.n_features_in_)
        
        # Make prediction
        prediction, probabilities = make_prediction(model, features)
        
        response = {
            'prediction': int(prediction[0]),
            'probabilities': probabilities[0].tolist() if probabilities is not None else None
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### Practice Tasks - Deployment

- [ ] Save and load a trained model (25 XP)
- [ ] Create a prediction function with input validation (35 XP)
- [ ] Implement confidence-based predictions (30 XP)
- [ ] Set up a basic Flask API for model serving (45 XP)

---

## Capstone Project: Customer Churn Prediction

### Project Overview

Build a complete machine learning system to predict customer churn using a telecommunications dataset.

### Dataset

We'll use the Telco Customer Churn dataset, which contains information about:

- Customer demographics
- Services each customer has signed up for
- Customer account information

### Project Structure

```python
# 1. Data Loading and Exploration
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load dataset (you can download from Kaggle or use a similar dataset)
df = pd.read_csv('telco_customer_churn.csv')

print("Dataset shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

print("\nDataset info:")
print(df.info())

print("\nTarget variable distribution:")
print(df['Churn'].value_counts())
```

### Step 1: Data Exploration and Preprocessing

```python
# Exploratory Data Analysis
plt.figure(figsize=(12, 8))

# Churn distribution
plt.subplot(2, 3, 1)
df['Churn'].value_counts().plot(kind='bar')
plt.title('Churn Distribution')
plt.xticks(rotation=0)

# Monthly charges distribution
plt.subplot(2, 3, 2)
df['MonthlyCharges'].hist(bins=30)
plt.title('Monthly Charges Distribution')

# Tenure distribution
plt.subplot(2, 3, 3)
df['tenure'].hist(bins=30)
plt.title('Tenure Distribution')

# Churn by Contract Type
plt.subplot(2, 3, 4)
pd.crosstab(df['Contract'], df['Churn']).plot(kind='bar')
plt.title('Churn by Contract Type')

plt.tight_layout()
plt.show()

# Data preprocessing
def preprocess_data(df):
    """Preprocess the customer churn dataset"""
    df_processed = df.copy()
    
    # Convert TotalCharges to numeric (it might be stored as string)
    df_processed['TotalCharges'] = pd.to_numeric(df_processed['TotalCharges'], errors='coerce')
    
    # Handle missing values
    df_processed['TotalCharges'].fillna(df_processed['TotalCharges'].mean(), inplace=True)
    
    # Convert binary categorical variables
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in binary_cols:
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].map({'Yes': 1, 'No': 0})
    
    # Convert gender
    df_processed['gender'] = df_processed['gender'].map({'Male': 1, 'Female': 0})
    
    return df_processed

df_processed = preprocess_data(df)

# Separate features and target
X = df_processed.drop(['customerID', 'Churn'], axis=1)
y = df_processed['Churn']

# Identify categorical and numerical columns
categorical_columns = X.select_dtypes(include=['object']).columns.tolist()
numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("Categorical columns:", categorical_columns)
print("Numerical columns:", numerical_columns)
```

### Step 2: Pipeline Creation and Model Training

```python
# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_columns)
    ])

# Create model pipelines
models = {
    'Logistic Regression': Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42))
    ]),
    'Random Forest': Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
}

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train and evaluate models
results = {}

for name, pipeline in models.items():
    print(f"\nTraining {name}...")
    
    # Cross-validation
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='roc_auc')
    
    # Train on full training set
    pipeline.fit(X_train, y_train)
    
    # Predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Store results
    results[name] = {
        'cv_auc': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'test_auc': roc_auc_score(y_test, y_pred_proba),
        'pipeline': pipeline
    }
    
    print(f"CV AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    print(f"Test AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
```

### Step 3: Hyperparameter Tuning

```python
# Hyperparameter tuning for the best model
best_model_name = max(results.keys(), key=lambda k: results[k]['test_auc'])
print(f"Best model: {best_model_name}")

# Define parameter grid for Random Forest
if 'Random Forest' in best_model_name:
    param_grid = {
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [5, 10, 15, None],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]
    }
else:  # Logistic Regression
    param_grid = {
        'classifier__C': [0.1, 1, 10, 100],
        'classifier__penalty': ['l1', 'l2'],
        'classifier__solver': ['liblinear', 'saga']
    }

# Grid search
best_pipeline = results[best_model_name]['pipeline']
grid_search = GridSearchCV(
    best_pipeline, 
    param_grid, 
    cv=5, 
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

print("Performing hyperparameter tuning...")
grid_search.fit(X_train, y_train)

print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV AUC: {grid_search.best_score_:.4f}")

# Final model evaluation
final_model = grid_search.best_estimator_
final_pred = final_model.predict(X_test)
final_pred_proba = final_model.predict_proba(X_test)[:, 1]

print(f"\nFinal Model Performance:")
print(f"Test AUC: {roc_auc_score(y_test, final_pred_proba):.4f}")
print(f"\nFinal Classification Report:")
print(classification_report(y_test, final_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, final_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Final Model')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()
```

### Step 4: Feature Importance and Model Interpretation

```python
# Feature importance (for tree-based models)
if hasattr(final_model.named_steps['classifier'], 'feature_importances_'):
    # Get feature names after preprocessing
    feature_names = (numerical_columns + 
                    list(final_model.named_steps['preprocessor']
                         .named_transformers_['cat']
                         .get_feature_names_out(categorical_columns)))
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': final_model.named_steps['classifier'].feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot top 15 features
    plt.figure(figsize=(10, 8))
    top_features = importance_df.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance')
    plt.title('Top 15 Feature Importances')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    
    print("Top 10 Most Important Features:")
    print(importance_df.head(10))
```

### Step 5: Model Deployment Preparation

```python
# Save the final model
joblib.dump(final_model, 'churn_prediction_model.pkl')
joblib.dump(X.columns.tolist(), 'feature_columns.pkl')

# Create deployment functions
def load_churn_model():
    """Load the trained churn prediction model"""
    model = joblib.load('churn_prediction_model.pkl')
    feature_columns = joblib.load('feature_columns.pkl')
    return model, feature_columns

def predict_churn(model, customer_data, feature_columns):
    """
    Predict churn probability for a customer
    
    Parameters:
    model: trained model
    customer_data: dict with customer information
    feature_columns: list of expected feature names
    
    Returns:
    dict with prediction and probability
    """
    # Convert to DataFrame
    df = pd.DataFrame([customer_data])
    
    # Ensure all columns are present
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0  # Default value for missing columns
    
    # Reorder columns to match training data
    df = df[feature_columns]
    
    # Make prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0, 1]
    
    return {
        'will_churn': bool(prediction),
        'churn_probability': float(probability),
        'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.3 else 'Low'
    }

# Example usage
sample_customer = {
    'gender': 0,  # Female
    'SeniorCitizen': 0,
    'Partner': 1,  # Yes
    'Dependents': 0,  # No
    'tenure': 12,
    'PhoneService': 1,  # Yes
    'MultipleLines': 'Yes',
    'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No',
    'OnlineBackup': 'No',
    'DeviceProtection': 'No',
    'TechSupport': 'No',
    'StreamingTV': 'Yes',
    'StreamingMovies': 'Yes',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 1,  # Yes
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 80.0,
    'TotalCharges': 960.0
}

# Load model and make prediction
model, features = load_churn_model()
prediction_result = predict_churn(model, sample_customer, features)
print(f"Churn Prediction Result: {prediction_result}")
```

### Step 6: Business Insights and Recommendations

```python
# Generate business insights
def generate_business_insights(model, X_test, y_test):
    """Generate actionable business insights from the model"""
    
    # Predict on test set
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    
    # Create segments based on churn probability
    risk_segments = pd.cut(probabilities, 
                          bins=[0, 0.3, 0.7, 1.0], 
                          labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    segment_analysis = pd.DataFrame({
        'actual_churn': y_test,
        'predicted_churn': predictions,
        'churn_probability': probabilities,
        'risk_segment': risk_segments
    })
    
    print("Customer Risk Segmentation:")
    print(segment_analysis['risk_segment'].value_counts())
    
    print("\nChurn Rate by Risk Segment:")
    churn_by_segment = segment_analysis.groupby('risk_segment')['actual_churn'].agg(['count', 'sum', 'mean'])
    churn_by_segment.columns = ['Total_Customers', 'Churned_Customers', 'Churn_Rate']
    print(churn_by_segment)
    
    # Calculate potential revenue impact
    if 'MonthlyCharges' in X_test.columns:
        monthly_charges_idx = list(X_test.columns).index('MonthlyCharges')
        # Get original monthly charges (before scaling)
        monthly_charges = X_test.iloc[:, monthly_charges_idx]
        
        segment_analysis['monthly_charges'] = monthly_charges
        revenue_impact = segment_analysis.groupby('risk_segment').agg({
            'monthly_charges': ['count', 'sum', 'mean'],
            'actual_churn': 'sum'
        })
        
        print("\nRevenue Impact Analysis:")
        print(revenue_impact)
    
    return segment_analysis

# Generate insights
insights = generate_business_insights(final_model, X_test, y_test)

# Actionable recommendations
print("\n" + "="*50)
print("BUSINESS RECOMMENDATIONS")
print("="*50)

recommendations = """
1. HIGH RISK CUSTOMERS (Probability > 0.7):
   - Immediate intervention required
   - Offer personalized retention incentives
   - Assign dedicated customer success manager
   - Provide service upgrades or discounts

2. MEDIUM RISK CUSTOMERS (Probability 0.3-0.7):
   - Proactive engagement campaigns
   - Improve service quality based on pain points
   - Offer loyalty programs
   - Regular satisfaction surveys

3. LOW RISK CUSTOMERS (Probability < 0.3):
   - Focus on upselling opportunities
   - Maintain service quality
   - Leverage as brand ambassadors
   - Monitor for changes in behavior

4. KEY FOCUS AREAS (Based on Feature Importance):
   - Contract terms: Encourage longer contracts
   - Payment methods: Promote automatic payments
   - Service bundling: Offer comprehensive packages
   - Customer support: Improve technical support quality
"""

print(recommendations)
```

### Step 7: Model Monitoring Framework

```python
# Model monitoring functions
def calculate_model_drift(reference_data, current_data, threshold=0.1):
    """
    Calculate data drift between reference and current data
    """
    from scipy.stats import ks_2samp
    
    drift_results = {}
    
    for column in reference_data.columns:
        if column in current_data.columns:
            # Kolmogorov-Smirnov test for continuous variables
            if reference_data[column].dtype in ['int64', 'float64']:
                statistic, p_value = ks_2samp(reference_data[column], current_data[column])
                drift_results[column] = {
                    'drift_detected': p_value < threshold,
                    'statistic': statistic,
                    'p_value': p_value
                }
    
    return drift_results

def monitor_model_performance(model, new_data, new_labels, performance_threshold=0.75):
    """
    Monitor model performance on new data
    """
    predictions = model.predict_proba(new_data)[:, 1]
    current_auc = roc_auc_score(new_labels, predictions)
    
    performance_degradation = current_auc < performance_threshold
    
    return {
        'current_auc': current_auc,
        'performance_degradation': performance_degradation,
        'threshold': performance_threshold
    }

# Example monitoring setup
print("Model Monitoring Framework Setup Complete")
print("Monitor the following metrics regularly:")
print("1. Model performance (AUC, Precision, Recall)")
print("2. Data drift in key features")
print("3. Prediction distribution changes")
print("4. Business KPIs (actual churn rate, revenue impact)")
```

### Capstone Project Tasks

- [ ] Complete data exploration and visualization (50 XP)
- [ ] Build preprocessing pipeline with categorical encoding (40 XP)
- [ ] Train and compare multiple models (60 XP)
- [ ] Perform hyperparameter tuning (50 XP)
- [ ] Analyze feature importance and generate insights (45 XP)
- [ ] Create deployment-ready prediction functions (55 XP)
- [ ] Generate business recommendations (40 XP)
- [ ] Set up model monitoring framework (45 XP)
- [ ] **BONUS**: Create a simple web interface for predictions (100 XP)

### Project Extensions

- [ ] Implement advanced feature engineering (60 XP)
- [ ] Try ensemble methods (Voting, Stacking) (70 XP)
- [ ] Add model interpretability with SHAP values (80 XP)
- [ ] Create automated retraining pipeline (90 XP)
- [ ] Implement A/B testing framework (100 XP)

---

## Additional Resources

### Related Notes

- [[Python for Data Science]] - Core Python skills for ML
- [[Supervised Learning]] - Deep dive into classification and regression
- [[Unsupervised Learning]] - Clustering and dimensionality reduction
- [[Feature Engineering]] - Advanced feature creation techniques
- [[Model Deployment]] - Production ML systems
- [[MLOps]] - ML Operations and lifecycle management

### Key Libraries and Documentation

- **scikit-learn**: https://scikit-learn.org/stable/
- **pandas**: https://pandas.pydata.org/docs/
- **matplotlib**: https://matplotlib.org/stable/contents.html
- **seaborn**: https://seaborn.pydata.org/
- **joblib**: https://joblib.readthedocs.io/

### Best Practices Checklist

- [ ] Always split data before any preprocessing
- [ ] Use pipelines to prevent data leakage
- [ ] Validate model performance with cross-validation
- [ ] Monitor model performance in production
- [ ] Document model decisions and assumptions
- [ ] Version control your models and data
- [ ] Consider ethical implications of your models

### Total XP Available: 1,485 XP

**Mastery Levels:**

- **Beginner**: 0-300 XP
- **Intermediate**: 300-700 XP
- **Advanced**: 700-1200 XP
- **Expert**: 1200+ XP

---

_Last updated: [09/11/2015]_ _Tags: #MachineLearning #ScikitLearn #Python #DataScience_