from inception_blocks_v2 import *
from fr_utils import *
from keras import backend as K

K.set_image_data_format("channels_first")


faceNetModel = faceRecoModel(input_shape=(3, 96, 96))
print('Total params: ', faceNetModel.count_params())


def triplet_loss(y_pred, alpha=0.2):
    """
    Implementation of the triplet loss as defined in FaceNet paper

    Arguments:
    y_pred -- python list containing three objects:
            anchor -- the encodings for the anchor images, of shape (None, 128)
            positive -- the encodings for the positive images, of shape (None, 128)
            negative -- the encodings for the negative images, of shape (None, 128)

    Returns:
    loss -- real number, value of the loss
    """

    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), -1)
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), -1)
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    loss = tf.reduce_mean(tf.maximum(basic_loss, 0.0))

    return loss


faceNetModel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
load_weights_from_FaceNet(faceNetModel)

face_ids = {}


def one_shot_train(phone, name, image_path):
    face_ids[str(phone) + '|' + name] = img_to_encoding(image_path, faceNetModel)


def recognize(image_path):
    encoding = img_to_encoding(image_path, faceNetModel)
    min_diff = 100

    for (person, enc) in face_ids.items():
        diff = np.linalg.norm(encoding - enc)
        if diff < min_diff:
            min_diff = diff
            exp_person = person

    if min_diff < 0.7:
        return None

    return min_diff, exp_person


one_shot_train(8010879484, 'neeraj', "images/rneeraj.jpg")
