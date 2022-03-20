## Music Transformer: experiements (for now)

#How to run it:
- gather a dataset inside the "dataset" folder
- run "preprocess.py" to process the data ("processed_data" folder)
- run "train.py" to train a model using the processed data ("model" folder)
- run "generate.py" to generate a midi file using the trained model ("generated_midi" folder)

#Goals:
- run it with a small dataset (DONE)
- run it with the full dataset at the big servers
- obtain a relatively decent midi file
- minimize vocabulary if possible
- simplify the code if possible
- introduce new mechanisms to the transformer

#Problems:
- generates velocities out of range