import cv2
import numpy as np
from matplotlib import pyplot as plt
#  TODO REFERENCE
def Predict(file):
    img = cv2.imread("submissions/" + file, 0)
    # ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    img = cv2.resize(img, (28, 28))
    plt.imshow((img.reshape((28, 28))), cmap='gray_r')

    # print img, "\n"
    arr = np.array(img - 255)
    # print arr
    arr = np.array(arr / 255.)
    # print arr

    new_test_cnn = arr.reshape(1, 1, 28, 28).astype('float32')
    print(new_test_cnn.shape)

    import operator
    from tensorflow import keras
    model_cnn = keras.models.load_model('my_model.h5')
    # CNN predictions
    new_cnn_predict = model_cnn.predict(new_test_cnn, batch_size=32, verbose=0)
    print(new_cnn_predict)
    # pr = model_cnn.predict_classes(arr.reshape((1, 1, 28, 28)))
    # print pr
    # Plotting the X_test data and finding out the probabilites of prediction
    fig, ax = plt.subplots(figsize=(8, 3))

    # Finding the max probability
    max_index, max_value = max(enumerate(new_cnn_predict[0]), key=operator.itemgetter(1))
    label_dict = {0: 'arm', 1: 'bicycle', 2: 'book', 3: 'paper_clip'}
    print(file + ": The drawing is identified as --> ", label_dict[max_index], " <-- with a probability of ", max_value * 100)
    return {label_dict[max_index], max_value}

# for i in list(range(1)):
#     # plot probabilities:
#     ax = plt.subplot2grid((1, 5), (i, 0), colspan=4);
#     plt.bar(np.arange(4), new_cnn_predict[i], 0.35, align='center');
#     plt.xticks(np.arange(4), ['arm', 'bicycle', 'book', 'paper_clip'])
#     plt.tick_params(axis='x', bottom='off', top='off')
#     plt.ylabel('Probability')
#     plt.ylim(0, 1)
#     plt.subplots_adjust(hspace=0.5)

#     # plot picture:
#     ax = plt.subplot2grid((1, 5), (i, 4), colspan=1);
#     plt.imshow((img.reshape(28, 28)), cmap='gray_r')
#     plt.xticks([])
#     plt.yticks([])
