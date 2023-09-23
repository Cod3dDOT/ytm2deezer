The what: This is a simple experiment of transfering my music library over to deezer.

The how: use publicly available apis to:

1. query songs in an old service
2. match each song in a new service (using the name and/or other attributes)
3. (todo) ask what to do when [no matches] / [multiple matches] are found
4. (todo) add each song in a new service

P.S Code quality is bad. Success rate is about 70%ish, false positives are rare.

TODO:

1. see above
2. move logging code to main.py and raise Exceptions whenever possible
3. complete deezer api to allow deezer -> yt music
