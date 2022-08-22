import tensorflow as tf


class CustomCrossEntropyLoss:
    def __init__(self,
                 label_probs: tf.lookup.StaticHashTable = None,
                 full_article_probs: tf.Tensor = None):
        self._label_probs = label_probs
        self._full_article_probs = full_article_probs

    def __call__(self, true_labels, logits, training):
        batch_size, nb_candidates = tf.shape(logits)

        if training:
            # Apply log q correction
            label_probs = self._label_probs.lookup(true_labels)
            logits -= tf.math.log(label_probs)
            # Override true labels to apply the softmax as if we only had "batch size" classes
            true_labels = tf.range(0, batch_size)

        # Compute softmax cross entropy
        loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=true_labels, logits=logits)
        return tf.reduce_sum(loss)
