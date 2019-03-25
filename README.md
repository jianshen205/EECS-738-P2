# EECS-738-P2 Hidden Markov Model


How machine learning can be used to learn word correlations and distributions with the dataset

In this project, we utilize a Hidden Markov Model to generate new text from text corpus.
The text corpus is downloaded from https://www.kaggle.com/kingburrito666/shakespeare-plays. In this word generation context, each word represents one state. First of all, we load first word of each line to a dictionary named initial_words.  For each state/ word, we include all possible next states/ words based on corpus and calculate emission possibilities for each state transition. Note that last word in each line points to token END.

After training our program contains three Markov chains plus the dictionary of initial_words mentioned previously. The first Markov chain is of first order and maps words to the relative frequency of the words that follow those words. The second Markov chain is of second order and maps pairs of words that to the relative frequency of the words that follow those words. The third Markov chain is of third order and maps triples of words to the relative frequency of the words that follow those words.

After training the model, new text generation starts. We generate a fixed number of lines (30).

The first word of each line is picked randomly from "initial_words". The second word uses the first order Markov chain. The third word uses the second order Markov chain. If we cannot find a next third word with the second order Markov chain or if we only have one option (more on this below), the program tries to use the first order Markov chain.

Similarly, to find the nth word (n > 3) in the line, we try the third, second, and finally first Markov Chain to find a next word. If we encounter a single option in the dictionary corresponding to an nth order Markov chain, we also try to look in a dictionary corresponding to the (n-1) th order Markov chain (where n > 1). This reduces the probability of repeating long strings of words that exist in the input file. The algorithm
continues until we have 20 words in a line or until we reach a dead end in all the Markov chains.
