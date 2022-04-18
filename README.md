## Music Transformer: experiements (for now)

#How to run it:
- gather a dataset inside the "dataset" folder
- run "preprocess.py" to process the data
-- python preprocess.py [indata (default: dataset)] [outdata (default: processed_data)]
- run "train.py" to train a model using the processed data ("model" folder)
-- python train.py [modelname (default: final)]
- run "generate.py" to generate a midi file using the trained model ("generated_midi" folder)
-- python generate [modelname (default: final)] [config (default: generate_noref)]

#Goals:
- run it with a small dataset (DONE)
- run it with the full dataset at the big servers (DONE)
- obtain decent material, even if short (DONE)
- obtain a consistent melody
- obtain a consistent rhythm
- obtain a relatively decent midi file from start to finish

#Problems:
- generates velocities out of range (DONE)
- sequences with lenght between batch_size and 2*batch_size result in error (DONE)
- small sequences are skipped (Opcional ?)
- must consider more parts of the pieces than the beggining (DONE)

#Improvements
- implement teacher forcing (DONE)
- minimize vocabulary if possible
- simplify the code if possible
- introduce new mechanisms to the transformer
- Logs in a readable file (DONE)

#Status:
- It reveals note interdependency when generating the file
- After 100 epochs (16 hours of training), the results are still a bit rudimental
- After 1000 epochs (7.5 days of training), the results are still rudimental
- After 3500 epochs, the results are still rudimental but some interesting sequence can be found
- Training only mazurkas (1000 epochs) shows that can actually retain input material
- After 7000 epochs, the results show that there's already some melodic/harmonic material but rhythm fails
- Using Ecompdata set, after 2000 epochs, the rhytmic problem is smaller, but it distabelizes faster too
- The main struggle is still the note length