import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

# Set parameters
random_state = 1
output_file = 'model/final_model_v2.bin'
DATA_PATH = 'Stress-Lysis.csv'  # Update to match your dataset file name

# Load the dataset
print("Loading the dataset...")
df = pd.read_csv(DATA_PATH)
df.columns = ['humidity', 'temperature', 'step_count', 'stress_level']

# Define features to be used for training
features = ['humidity', 'temperature', 'step_count']

# Split data into training and validation sets
df_train, df_val = train_test_split(df, test_size=0.4, random_state=random_state, stratify=df.stress_level)

# Training function
def train(df_train, y_train, random_state=1):
    dicts = df_train[features].to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)
    
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=random_state,
        use_label_encoder=False,
        eval_metric='mlogloss'  # Use this for multi-class classification
    )
    
    model.fit(X_train, y_train)
    return dv, model

# Prediction function
def predict(df, dv, model):
    dicts = df[features].to_dict(orient='records')
    X = dv.transform(dicts)
    y_pred = model.predict(X)
    return y_pred

# Train the model
print("Training the model...")
dv, model = train(df_train, df_train.stress_level.values, random_state)

# Run predictions and evaluate
print("Evaluating model...")
y_pred = predict(df_val, dv, model)
y_test = df_val.stress_level.values
acc = accuracy_score(y_test, y_pred)
print("Accuracy for Validation = %.3f" % acc)

# Save model and vectorizer
print(f"Saving the model to {output_file}...")
with open(output_file, 'wb') as f_out:
    pickle.dump((dv, model), f_out)

print('☑️ Model training is completed and saved.')
