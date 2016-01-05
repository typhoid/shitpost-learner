# Shitpost Learner

shitpost /SCHIT-pohst/ - a comment that contains nothing of intended value, but at the
same time is not intended to troll with.

This script uses Markov chains to learn how to shitpost. Using a user-specified board,
this script trains a Markov chain on all posts on all pages of said board and generates
shitposts on command. Also includes a random image from the same board. This doesn't
actually post to 4chan.

This makes extensive use of 4chan's read-only JSON API.

# Dependencies

This requires PyMarkovChain to run.

For Linux users - simply run:

`sudo pip install PyMarkovChain`

# How to Use

0. Install the required dependencies if you don't already have them.

1. For Python 3 users, run `./shitposter3.py`.

For Python 2 users, run `./shitposter.py`.

2. Enter a board to train on - ex. /a/, /b/, /co/, /tv/, etc.
3. Once training is finished, hit enter to generate a shitpost.

The command `train` will re-train the Markov chain on the same board.

The command `board <board>` will switch to the specified board.

The command `exit` will exit the script.

# Credits
[ChangedNameTo](https://github.com/ChangedNameTo) - Image-grabbing
[franzwr](https://github.com/franzwr) - Data pickling
[Tim La Roche](https://github.com/timlaroche) - Python 3 support
