import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load the dataset
data_dict = pickle.load(open('./data.pickle', 'rb'))

data = data_dict['data']
labels = np.array(data_dict['labels'])

# Find the maximum length of feature vectors
max_length = max(len(seq) for seq in data)

# Pad all sequences to match the longest one
data_padded = np.array([seq + [0] * (max_length - len(seq)) for seq in data])

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(data_padded, labels, test_size=0.2, shuffle=True, stratify=labels)

# Train RandomForest model
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Make predictions
y_predict = model.predict(x_test)

# Compute accuracy
score = accuracy_score(y_predict, y_test)
print('{}% of samples were classified correctly!'.format(score * 100))

# Save trained model
# with open('model.p', 'wb') as f:
#     pickle.dump({'model': model}, f)


f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
