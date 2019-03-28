# EECS-738-P2 Hidden Markov Model


How machine learning can be used to learn word correlations and distributions with the dataset

In this project, we utilize a Hidden Markov Model to generate new text from text corpus.
The text corpus is downloaded from https://www.kaggle.com/kingburrito666/shakespeare-plays. In this word generation context, each word represents one state. First, we obtain first, second, and third words from the words that ocurred first, second, and third, respectively, in the training set.  For each state/ word, we include all possible next states/ words based on corpus and calculate emission possibilities for each state transition. Note that last word in each line points to token END. We use three dictionaries corresponding to three Markov chains of decreasing degrees (3 through 1) to calculate the state transitions.

Our motivation for using three Markov chain is to take advantage of each Markov chain. The greater the degree of the Markov chain, the more precise it is and the less variablity it allows for (overfitting). On the other hand, Markov chains of lower degrees allow us to generate more varied text but the text is less likely to be sensical (less precision). By using three Markov chains of different degrees, we maintain a moderate degree of precision while reducing the amount of overfitting.

After training our program contains three Markov chains plus the dictionaries conaining first, second, and third words. The first Markov chain is of first order and maps words to the relative frequency of the words that follow those words. The second Markov chain is of second order and maps pairs of words that to the relative frequency of the words that follow those words. The third Markov chain is of third order and maps triples of words to the relative frequency of the words that follow those words.

Next, our program begins the process of text generation. We generate a fixed number of lines (30). The first, second, and third word of each line are picked from the "firstWords", "secondWords", and "thirdWords" dictionaries, respectively. The first word is picked randomly among the first words that occurred in the training set. The second word is picked based on the first word. The third word is picked based on the first two words.

In this way, the number of lines that end abruptly in one or two words are reduced. Most lines are guaranteed to contain at least three words.

Starting from the fourth word in each line, words are predicted using the Markov chains. Initially, we attempt to predict the next word in a line based on the three previous words using the "thirdOrder" dictionary. For example:

    ('all', 'the', 'worlds') -> ['a', 'new', 'vastidity', 'my']
    ('wherefore', 'art', 'thou') -> ['romeo']
    ('cowards', 'die', 'many') -> ['times']
    ('thou', 'shalt', 'woo') -> []

It is not uncommon to find triplets of words that only lead to one option. Repeatedly following the only path available would have us end up with long strings of words that are identical to the ones in the training set. Hence, we attempt to reduce the number of "only path available" when follow when predicting words.

Additionally, when generating new text we often generate triples of words that do not even have an entry in the dictionary. This is a problem if we do not want to end a line prematurely. Since we want to have a somewhat uniform amount of words per line,
we will try to reduce the amount of times we reach a dead end.

To solve both of these problems we use the second and first order Markov chains. There are two cases (corresponding to both problems) in which we use a lower order Markov chain:

1) When we only find one possible next word based on the previous 3 words. For example:

    To solve this issue, we recursively try lower order Markov chains until we find one in which there is more than one option. For example:

        ('cowards', 'die', 'many') -> ['times']
        ('die', 'many') -> ['times']
        'many' -> ['pipes', 'smiling', 'years', 'ages', 'times', ...]

    In this example, since the last 3 words (third order) lead to only one option, we try just the last two words (second order). Since the last 2 words lead to only one option as well, we try the last word (first order).

    It is important to note that if we do not find a better option, we will return the only possible next word. For example:

        ('conquests', 'glories', 'triumphs') -> ['spoils']
        ('glories', 'triumphs') -> ['spoils']
        'triumphs' -> ['spoils']

    In this case, since we have failed to find a better option, our next word would be 'spoils'.

2) When we do not find any next word based on the previous 3 words. For example:

    To solve this issue, we attempt to find a next word based on only the previous 2 words. If this fails, we attempt to find a next word based on the previous word only. For example:

          ('Thou', 'shalt', 'woo') -> []
          ('shalt', 'woo') -> []
          'woo' -> ['her', 'thee']

    In this example, since the last 3 words (third order) lead to a dead end, we try just the last two words (second order). Since the last 2 words lead to a dead end as well, we try the last word (first order).

    If this fails, we give up and end the line. For example:

          ('they', 'were', 'glassd') -> ['tokEND']
          ('were', 'glassd') -> ['tokEND']
          'glassd' -> ['tokEND']

    In this case, we have no option but to end the line. Note that having only the option to go to 'tokEND' is interpreted as reaching a dead end.


Each line ends when either we have reached a dead end in all three Markov chains or we have reached the words per line limit (15).

Lastly, we print all 30 lines to the command line.

Refereneces:
    https://medium.com/ymedialabs-innovation/next-word-prediction-using-markov-model-570fc0475f96
