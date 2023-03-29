# this app is used to run ICA on raw data
# it first sets up the ICA object and then fits it on the raw data
# it then saves the ICA object and plots the components and sources


import os
import mne
import json
import helper

import matplotlib.pyplot as plt


# Load brainlife config.json
with open('config.json','r') as config_f:
    config = helper.convert_parameters_to_None(json.load(config_f))

# == LOAD DATA ==
fname = config['mne']
raw = mne.io.read_raw_fif(fname, preload=True)
if config['l_freq'] is not None:
    raw = raw.filter(l_freq=config['l_freq'], h_freq=config['h_freq'])

ica= mne.preprocessing.ICA(n_components=config['n_components'], noise_cov=config['noise_cov'],
                      random_state=config['random_state'], method=config['method'],
                      fit_params=config['fit_params'], max_iter=config['max_iter'],
                      allow_ref_meg=config['allow_ref_meg'])

ica.fit(raw)

ica.save('out_dir/ica.fif',overwrite=True)

plt.figure(1)
ica.plot_components()
plt.savefig(os.path.join('out_figs','ica.png'))

plt.figure(2)
ica.plot_sources(raw)
plt.savefig(os.path.join('out_figs','sources.png'))
