"""Start a hyperoptimization from a single node"""
import sys
import numpy as np
import pickle as pkl
import hyperopt
from hyperopt import hp, fmin, tpe, Trials
from HyperparameterSearch import test_args, ObjectView


#Change the following code to your file
################################################################################
# TODO: Declare a folder to hold all trials objects
TRIALS_FOLDER = 'trials_40000epochs'
NUMBER_TRIALS_PER_RUN = 1

def run_trial(args):
    """Run a training iteration based on args.

    :args: A dictionary containing all hyperparameters
    :returns: Average loss from cross-validation

    """
    args['loss'] = 'l1'
    args['output_dim'] = 1
    args['model'] = 'gln'
    args['num_epochs'] = 40000
    args['hidden_dim'] = int(args['hidden_dim'])
    args['layers'] = int(args['layers'])
    args['n_updates'] = int(args['n_updates'])
    args['batch_size'] = int(args['batch_size'])
    return test_args(ObjectView(args))

space = {
    'act' : hp.choice('act', ['softplus', 'swish', 'tanh', 'tanh_relu', 'soft_relu', 'relu_relu3', 'relu3_relu', 'relu_tanh']),
    'l2reg': hp.loguniform('l2reg', np.log(1e-12), np.log(5)),
    'dt': hp.loguniform('dt', np.log(1e-4), np.log(2)),
    'hidden_dim' : hp.qloguniform('hidden_dim', np.log(10), np.log(1000), 1),
    'layers' : hp.quniform('layers', 2, 6, 1),
    'n_updates' : hp.quniform('n_updates', 1, 6, 1),
    'lr': hp.loguniform('lr', np.log(1e-6), np.log(1e-1)),
    'lr2': hp.loguniform('lr2', np.log(1e-7), np.log(1e-3)),
    'batch_size': hp.qloguniform('batch_size', np.log(16), np.log(1024), 1),
}

################################################################################



def merge_trials(trials1, trials2_slice):
    """Merge two hyperopt trials objects

    :trials1: The primary trials object
    :trials2_slice: A slice of the trials object to be merged,
        obtained with, e.g., trials2.trials[:10]
    :returns: The merged trials object

    """
    max_tid = 0
    if len(trials1.trials) > 0:
        max_tid = max([trial['tid'] for trial in trials1.trials])

    for trial in trials2_slice:
        tid = trial['tid'] + max_tid + 1
        hyperopt_trial = Trials().new_trial_docs(
                tids=[None],
                specs=[None],
                results=[None],
                miscs=[None])
        hyperopt_trial[0] = trial

        if hyperopt_trial[0]['result']['status'] != 'ok':
            hyperopt_trial[0]['result']['loss'] = float('inf')

        hyperopt_trial[0]['tid'] = tid
        hyperopt_trial[0]['misc']['tid'] = tid
        for key in hyperopt_trial[0]['misc']['idxs'].keys():
            hyperopt_trial[0]['misc']['idxs'][key] = [tid]
        trials1.insert_trial_docs(hyperopt_trial) 
        trials1.refresh()
    return trials1

loaded_fnames = []
trials = None
# Run new hyperparameter trials until killed
while True:
    np.random.seed()

    # Load up all runs:
    import glob
    path = TRIALS_FOLDER + '/*.pkl'
    for fname in glob.glob(path):
        if fname in loaded_fnames:
            continue

        trials_obj = pkl.load(open(fname, 'rb'))
        n_trials = trials_obj['n']
        trials_obj = trials_obj['trials']
        if len(loaded_fnames) == 0: 
            trials = trials_obj
        else:
            print("Merging trials")
            trials = merge_trials(trials, trials_obj.trials[-n_trials:])

        loaded_fnames.append(fname)

    print("Loaded trials", len(loaded_fnames))
    assert len(loaded_fnames) == 0 or len(loaded_fnames) == len(trials.trials)
    if len(loaded_fnames) == 0:
        trials = Trials()

    n = NUMBER_TRIALS_PER_RUN
    try:
        best = fmin(run_trial,
            space=space,
            algo=tpe.suggest,
            max_evals=n + len(trials.trials),
            trials=trials,
            verbose=1,
            rstate=np.random.RandomState(np.random.randint(1,10**6))
            )
    except hyperopt.exceptions.AllTrialsFailed:
        continue

    print('current best', best)
    hyperopt_trial = Trials()

    # Merge with empty trials dataset:
    save_trials = merge_trials(hyperopt_trial, trials.trials[-n:])
    new_fname = TRIALS_FOLDER + '/' + str(np.random.randint(0, sys.maxsize)) + '.pkl'
    pkl.dump({'trials': save_trials, 'n': n}, open(new_fname, 'wb'))
    loaded_fnames.append(new_fname)
