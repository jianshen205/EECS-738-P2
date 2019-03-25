# EECS-738-P2 Hidden Markov Model


how machine learning can be used to learn word correlations and distributions with the dataset

In this project, we utilize Hidden Markov Model to generate new text from text corpus.
The text corpus is downloaded from https://www.kaggle.com/kingburrito666/shakespeare-plays. In this word generation context, each word represents one state. First of all, we load first word of each line to a dictionary named initial_words.  For each state/ word, we include all possible next states/ words based on corpus and calculate emission possibilities for each state transition. Note that last word in each line points to token END.

After model training, new text genration starts by randomly picking word from dictionary initial_words. Then continueously selecting words from transition dictionary that last selected word followed by, untill token END found.
