 A Mamba Based Classifier and parallel hidden Markov model algorithm to detect heart murmurs

Adrian Florea



## Running scripts:


You can install the dependencies for these scripts by creating a Docker image (see below) and running

    pip install bi-hsmm-murmur/requirements.txt

Training: 
    python3 train_model.py training_data model

Predict:
    python3 run_model.py model test_data test_outputs

Evaluate Performance:

    python evaluate_model.py labels outputs scores.csv class_scores.csv

## Experiements to run:
bimamba_params to be changed in: /bi-hsmm-murmur/src/neural_networks/py line 369 in RecurrentNeworkModel class

bimamba_tiny: 180,145 parameters

        d_model=dim, # Model dimension d_model
        d_state=16,  # SSM state expansion factor
        d_conv=4,    # Local convolution width
        expand=2,    #  Block expansion factori
        n_mamba = 9,     
        
    Training:
    python3 bi-hsmm-murmur/train_model.py the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data/ results/bimamba_tiny/model

    Predict:
    python3 bi-hsmm-murmur/run_model.py results/bimamba_tiny/model data/filtered/ results/bimamba_tiny/filt/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_tiny/model data/wavs/ results/bimamba_tiny/wavs/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_tiny/model data/lp/ results/bimamba_tiny/lp/

    Evaluate: 
    python3 bi-hsmm-murmur/evaluate_model.py data/filtered/ results/bimamba_tiny/filt/
    python3 bi-hsmm-murmur/evaluate_model.py data/wavs/ results/bimamba_tiny/wavs/
    python3 bi-hsmm-murmur/evaluate_model.py data/lp/ results/bimamba_tiny/lp/

bimamba_m: 1,914,625 params

        d_model=dim, # Model dimension d_model
        d_state=64,  # SSM state expansion factor
        d_conv=4,    # Local convolution width
        expand=5,    #  Block expansion factori
        n_mamba = 18,     

    Training:
    python3 bi-hsmm-murmur/train_model.py the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data/ results/bimamba_m/model

    Predict:
    python3 bi-hsmm-murmur/run_model.py results/bimamba_m/model data/filtered/ results/bimamba_m/filt/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_m/model data/wavs/ results/bimamba_m/wavs/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_m/model data/lp/ results/bimamba_m/lp/

    Evaluate: 
    python3 bi-hsmm-murmur/evaluate_model.py data/filtered/ results/bimamba_m/filt/
    python3 bi-hsmm-murmur/evaluate_model.py data/wavs/ results/bimamba_m/wavs/
    python3 bi-hsmm-murmur/evaluate_model.py data/lp/ results/bimamba_m/lp/


bimamba_l: 5,857,345 parms 

        d_model=dim, # Model dimension d_model
        d_state=128,  # SSM state expansion factor
        d_conv=4,    # Local convolution width
        expand=5,    #  Block expansion factori
        n_mamba = 32, ## Docker

        
    Training:
    python3 bi-hsmm-murmur/train_model.py the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data/ results/bimamba_l/model

    Predict:
    python3 bi-hsmm-murmur/run_model.py results/bimamba_l/model data/filtered/ results/bimamba_l/filt/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_l/model data/wavs/ results/bimamba_l/wavs/
    python3 bi-hsmm-murmur/run_model.py results/bimamba_l/model data/lp/ results/bimamba_l/lp/

    Evaluate: 
    python3 bi-hsmm-murmur/evaluate_model.py data/filtered/ results/bimamba_l/filt/
    python3 bi-hsmm-murmur/evaluate_model.py data/wavs/ results/bimamba_l/wavs/
    python3 bi-hsmm-murmur/evaluate_model.py data/lp/ results/bimamba_l/lp/



requires nvidia-docker2
