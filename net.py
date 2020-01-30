import tensorflow as tf


class FCN(object):
    def __init__(self, prefix, n_layer, n_input, n_output, n_unit):
        super(FCN, self).__init__()

        self.layer_list = self.make_layer_list(prefix, n_layer, n_input, n_output, n_unit)

    def make_layer_list(self, prefix, n_layer, n_input, n_output, n_unit):
        layers = []
        layers.append(tf.keras.layers.InputLayer((n_input,)))

        for i in range(n_layer):
            layer_name = prefix + '/dense' + str(i + 1)
            layers.append(tf.keras.layers.Dense(n_unit, activation='relu', name=layer_name))

        layers.append(tf.keras.layers.Dense(n_output, name=prefix + '/dense' + str(n_layer + 1)))

        return layers

    def build(self):
        return tf.keras.Sequential(self.layer_list)


class Main(FCN):
    def __init__(self, d_in):
        super(Main, self).__init__("main", 2, d_in, 10, 50)


class Meta(FCN):
    def __init__(self):
        super(Meta, self).__init__("meta", 2, 42310, 3, 50)


class MetaAlpha(FCN):
    def __init__(self):
        super(MetaAlpha, self).__init__("meta", 2, 3*42310, 1, 50)


class MultiFCN(FCN):
    def __init__(self, prefix, n_layer, n_input, n_output, n_unit, n_layer_main):
        super(MultiFCN, self).__init__(prefix, n_layer, n_input, n_output, n_unit)

        self.net_list = []
        for j in range(n_layer_main):
            prefix = str(j) + "_" + prefix
            net = self.make_layer_list(prefix, n_layer, n_input, n_output, n_unit)
            self.net_list.append(net)

    def call(self, inputs):
        return self.net(inputs)
