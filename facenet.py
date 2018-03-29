from inception_blocks_v2 import *
from fr_utils import *
from keras import backend as K
from os import listdir

K.set_image_data_format("channels_first")


class FaceNetClass:

    def __init__(self):
        self.faceNetModel = faceRecoModel(input_shape=(3, 96, 96))
        print('Total params: ', self.faceNetModel.count_params())
        self.faceNetModel.compile(optimizer='adam', loss=self.triplet_loss, metrics=['accuracy'])
        load_weights_from_FaceNet(self.faceNetModel)
        self.face_ids = {}
        self.files = listdir('images/')
        self.pre_train_count = 0
        self.pre_train()

    @staticmethod
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

    def pre_train(self):
        if self.pre_train_count is 1:
            return
        self.pre_train_count += 1
        print(self.files)
        for file in self.files:
            name = file.split('.')[0]
            if name is 'test':
                continue
            else:
                embedding = img_to_encoding('images/' + file, self.faceNetModel)
                if embedding is None:
                    continue
                if name in self.face_ids:
                    self.face_ids[name].append(embedding)
                else:
                    self.face_ids[name] = []
                    self.face_ids[name].append(embedding)

    def one_shot_train(self, data):
        name = data['name']
        image_paths = data['image']
        print(name, image_paths)
        for image_path in image_paths:
            if name in self.face_ids:
                self.face_ids[name].append(img_to_encoding(image_path, self.faceNetModel))
            else:
                self.face_ids[name] = []
                self.face_ids[name].append(img_to_encoding(image_path, self.faceNetModel))
        return

    def recognize(self, image_path):
        encoding = img_to_encoding(image_path, self.faceNetModel)
        if encoding is None:
            return None

        min_diff = 100

        for (person, encs) in self.face_ids.items():

            for enc in encs:
                if enc is None:
                    continue
                diff = np.linalg.norm(encoding - enc)
                print(person, diff)

                if diff < min_diff:
                    min_diff = diff
                    exp_person = person

        print(str(min_diff), exp_person)
        if min_diff > 0.65:
            return None

        return min_diff, exp_person
