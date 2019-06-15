from sklearn.preprocessing import OneHotEncoder
import numpy as np


integer_encoded = np.array([1,0,1,0,0,0,-1,-1,1,1,1])

onehot_encoder = OneHotEncoder(sparse=False, categories="auto")
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded)