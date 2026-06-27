import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

print('Loading dataset...')
df = pd.read_csv('dataset/transactions.csv')
print('Loaded', len(df), 'transactions')
print('Fraud cases:', df["is_fraud"].sum(), '({:.1f}% of data)'.format(df["is_fraud"].mean() * 100))

X = df[['account_no', 'amount', 'location', 'transaction_count', 'transaction_type', 'device_type', 'is_new_location']]
y = df['is_fraud']

label_encoders = {}
categorical_features = ['location', 'transaction_type', 'device_type']

for col in categorical_features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

le_y = LabelEncoder()
y_encoded = le_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

print('Train set:', len(X_train), 'samples')
print('Test set:', len(X_test), 'samples')

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    class_weight='balanced',
    n_jobs=-1
)

print('Training model...')
model.fit(X_train, y_train)

preds = model.predict(X_test)

report = classification_report(y_test, preds, target_names=['Normal', 'Fraud'])

print('\nModel Evaluation:')
print('Accuracy: {:.4f}'.format(accuracy_score(y_test, preds)))
print('\nClassification Report:')
print(report)

os.makedirs('fraud_detection', exist_ok=True)

with open('fraud_detection/model.pkl', 'wb') as f:
    joblib.dump(model, f)

with open('fraud_detection/label_encoders.pkl', 'wb') as f:
    joblib.dump(label_encoders, f)

with open('fraud_detection/label_encoder_y.pkl', 'wb') as f:
    joblib.dump(le_y, f)

print('Model and encoders saved successfully to fraud_detection/ directory')

sample_features = [[0, 162969, 0, 7, 1, 0, 0]]
pred = model.predict(sample_features)
prob = model.predict_proba(sample_features)[0]
print('\nSample prediction (ACC9958): {} (0=Normal, 1=Fraud)'.format(pred[0]))
print('Probabilities: Normal={:.2f}, Fraud={:.2f}'.format(prob[0], prob[1]))
print('\nTraining complete!')
