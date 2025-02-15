import numpy as np
import tensorflow as tf
from random import randrange

batch_size = 1
timesteps = 1
size = 1
units = 16
shape = (timesteps, size)

model = tf.keras.models.Sequential([
  tf.keras.layers.Input(shape = shape, batch_size = batch_size),
  tf.keras.layers.GRU(
    units,
    stateful = True,
    return_sequences = True
  )
])

model.compile(optimizer='adam',
              loss='mean_squared_error')

print(model.summary())

SAME = False

i = 0
prevIsBlack = False
x_batch, y_batch = [], []
x_steps, y_steps = [], []

while True:
  i += 1

  isBlack = randrange(4) == 2

  if SAME: prevIsBlack = isBlack 

  x_train = np.ones(size)   if isBlack else np.zeros(size)
  y_train = np.zeros(units) if prevIsBlack else np.ones(units)

  if not SAME: prevIsBlack = isBlack 

  x_steps.append(x_train)
  y_steps.append(y_train)

  if len(x_steps) < timesteps:
    continue

  x_batch.append(np.stack(x_steps))
  y_batch.append(np.stack(y_steps))

  x_steps, y_steps = [], []

  if len(x_batch) < batch_size:
    continue

  res = model.fit(np.stack(x_batch), np.stack(y_batch), 
    epochs = 1, 
    shuffle = False,
    batch_size = batch_size)

  print(res.history["loss"])

  x_batch = []
  y_batch = []