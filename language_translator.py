# -*- coding: utf-8 -*-
"""Language_Translator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HWTiTVd5uHhTLvJiPebOrn5-8AqrtkPJ
"""

import collections
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.layers import GRU, Input, Dense, TimeDistributed, Activation, RepeatVector, Bidirectional,LSTM
from keras.layers.embeddings import Embedding
from keras.optimizers import *
from keras.losses import sparse_categorical_crossentropy
from keras.models import Sequential
from keras import optimizers

def load_data(filename):
	# open the file as read only
	file = open(filename, mode='rt', encoding='utf-8')
	# read all text
	text = file.read()
	# close the file
	file.close()
	return text
# split a loaded document into sentences
def to_sentences(doc):
	return doc.strip().split('\n')
  #load english data
eng_doc = load_data('/content/drive/MyDrive/small_vocab_en.csv')
eng_sentences = to_sentences(eng_doc)

# Load French data
fre_doc = load_data('/content/drive/MyDrive/small_vocab_fr.csv')
fre_sentences = to_sentences(fre_doc)

print('Dataset Loaded')

for sample_i in range(2):
    print('small_vocab_en Line {}:  {}'.format(sample_i + 1, eng_sentences[sample_i]))
    print('small_vocab_fr Line {}:  {}'.format(sample_i + 1, fre_sentences[sample_i]))

english_words_counter = collections.Counter([word for sentence in eng_sentences for word in sentence.split()])
french_words_counter = collections.Counter([word for sentence in fre_sentences for word in sentence.split()])

print('{} English words.'.format(len([word for sentence in eng_sentences for word in sentence.split()])))
print('{} unique English words.'.format(len(english_words_counter)))
print('10 Most common words in the English dataset:')
print('"' + '" "'.join(list(zip(*english_words_counter.most_common(10)))[0]) + '"')
print()
print('{} French words.'.format(len([word for sentence in fre_sentences for word in sentence.split()])))
print('{} unique French words.'.format(len(french_words_counter)))
print('10 Most common words in the French dataset:')
print('"' + '" "'.join(list(zip(*french_words_counter.most_common(10)))[0]) + '"')

def tokenization(lines):
  tokenizer=Tokenizer(num_words=10,oov_token="<OOV>")
  tokenizer.fit_on_texts(lines)
  sequence=tokenizer.texts_to_sequences(lines)
  one_hot_result=tokenizer.texts_to_matrix(lines,mode='binary')
  word_index=tokenizer.word_index
  print('found %s unique tokens.'%len(word_index))
  print(word_index)
  print(one_hot_result.shape)
 # print(one_hot_result)
  #print(sequence)
  return sequence

#print(eng_tokenization)
eng_lenth=8
#print(type(eng_tokenization))

eng_tokenization=tokenization(eng_sentences[:10])
eng_padded=pad_sequences(eng_tokenization,padding='post')
print(eng_padded)
print(eng_padded.shape)
fre_tokenization=tokenization(fre_sentences[:10])
fre_padded=pad_sequences(fre_tokenization,padding='post')
print(fre_padded)

#print(eng_tokenization)

from sklearn.model_selection import train_test_split
train_x,test_x,train_y,test_y=train_test_split(eng_padded,fre_padded,test_size=0.2,random_state=4)
#train_y,test_y=train_test_split(fre_tokenization,test_size=0.2,random_state=4)
print(train_x,train_y)
print(train_x.shape)
print(train_y.shape)

from tensorflow import keras
from keras import layers
vocab_size1=len(english_words_counter)
print(vocab_size1)
vocab_size2=len(french_words_counter)
print(vocab_size2)

model=keras.Sequential([
                           layers.Embedding(vocab_size1,vocab_size2,input_length=15),
                           
                           layers.GlobalAveragePooling1D(),
                           tf.keras.layers.Dense(24,activation='relu'),
                           tf.keras.layers.Dense(1,activation='sigmoid')

                                                     ])
model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])

history=model.fit(train_x,train_y,epochs=25,validation_data=(test_x,test_y),verbose=2)

preds=model.predict(test_x.reshape(test_x.shape[0],test_x.shape[1]))

print(preds)