# ucb-webcasts-cc
UC Berkeley Webcasts Closed-Captioning Project

(Unaffiliated with UC Berkeley)

This is an attempt at coordinating efforts to add proper closed-caption to UCB Webcasts to avoid them being unpublished, [because of human stupidity](https://fee.org/articles/when-equal-access-means-zero-access-for-all/).


## How can I help?


## python scripts

### extract_playlist.py

This extracts the current list of webcasts from the UCB website and fetches the youtube playlists for each of them, and dumps the result as ucb_webcasts.json.

### generate_master_pad.py

This loads ucb_webcasts.json and generates a markdown content for the master pad, linking to all the videos and the corresponding pads.
