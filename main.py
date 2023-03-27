# this app is used to run ICA on raw data
# it first sets up the ICA object and then fits it on the raw data
# it then saves the ICA object and plots the components and sources


import os
import mne
import json
import helper

import matplotlib.pyplot as plt

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Load brainlife config.json
with open('config.json','r') as config_f:
    config = helper.convert_parameters_to_None(json.load(config_f))

# == LOAD DATA ==
fname = config['fif']
raw = mne.io.read_raw_fif(fname, verbose=False)

ica= mne.preprocessing.ICA(n_components=config['n_components'], noise_cov=None,
                      random_state=None, method=config['method'],
                      fit_params=None, max_iter=config['max_iter'],
                      allow_ref_meg=config['allow_ref_meg'])

ica.fit(raw)

ica.save('out_dir/ica.fif',overwrite=True)

plt.figure(1)
ica.plot_components()
plt.savefig(os.path.join('out_figs','ica.png'))

plt.figure(2)
ica.plot_sources(raw)
plt.savefig(os.path.join('out_figs','sources.png'))
