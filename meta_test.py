import dataset
import tensorflow as tf
import grouplearner
import optimizer as op
import spec

def main(unused_argv):
    learning_rate = 5e-2
    n_epoch = 1
    n_batch = 10
    n_task = 10

    # model path
    model_dir = "meta_test"

    # config
    run_config = tf.estimator.RunConfig(model_dir=model_dir, save_checkpoints_steps=6000)
    ws0 = tf.estimator.WarmStartSettings(ckpt_to_initialize_from=model_dir, vars_to_warm_start=["meta"])
    ws1 = tf.estimator.WarmStartSettings(ckpt_to_initialize_from=model_dir, vars_to_warm_start=["main", "meta"])

    # generate sequence dataset
    set_of_datasets = dataset.SetOfRandPermMnist(n_task)
    d_in = set_of_datasets.list[0].d_in

    # learning specs
    opt = op.SGDOptimizer().build(learning_rate)
    opt_spec = spec.OptimizerSpec(opt, d_in)
    learning_spec = spec.LearningSpec(n_epoch, n_batch, n_task, model_dir, opt_spec)

    my_grouplearner = grouplearner.GroupMetaTestLearner(set_of_datasets, learning_spec, n_task, run_config, ws0, ws1)

    accuracy_matrix = my_grouplearner.train_and_evaluate()
    print(accuracy_matrix)

    n_total = n_task * (n_task + 1) / 2.0
    print(accuracy_matrix.sum() / n_total)


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
