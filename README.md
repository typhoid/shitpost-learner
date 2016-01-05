# Shitpost Learner - Web Version

shitpost /SCHIT-pohst/ - a comment that contains nothing of intended value, but at the
same time is not intended to troll with.

This script uses Markov chains to learn how to shitpost. Using a user-specified board,
this script trains a Markov chain on all posts on all pages of said board and generates
shitposts on command. Also includes a random image from the same board. This doesn't
actually post to 4chan.

This makes extensive use of 4chan's read-only JSON API.

This is a web version of the CLI shitpost-learner. Its primary components are:

* A script that downloads post/image URL data from all 65 boards (runs on a crontab)
* A Python CGI page that displays posts/images

# Dependencies

* A decent web server
* CGI enabled on said server
* PHP also enabled on said server
* Python 3
* PyMarkovChain
* urllib3

# How to Use

0. Install the required dependencies if you don't already have them.
1. Run `cron/shitpost_data.py <board>` on your desired boards. Optionally, use the provided crontab to scrape data from 4chan every hour.
2. Once training is finished, boards will appear in the form in index.php. Only boards with post/image data will appear. Select a board and between 5 and 20 posts to display.
3. Click "Submit" to be taken to a page where you can see the Markov chains do their thing.

# Credits
* [ChangedNameTo](https://github.com/ChangedNameTo) - Image-grabbing
* [franzwr](https://github.com/franzwr) - Data pickling
* [Tim La Roche](https://github.com/timlaroche) - Python 3 support
