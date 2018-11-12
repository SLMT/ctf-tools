# Git Repository Downloader (Linux and Windows)
## Basic idea
Ever found a `.git ` directory on a webserver? This tool will try to download this file and recreate the most recent commit of this downloaded repository. Useful for reconnaissance and further analysis of attack vectors.

## Functionality
As git has a naming convention of its files. Sometimes we are not allowed to see the contents of the git directory on the webserver, but still are able to download it. This tool tries to download those git files and recreates the repository locally.


## Requirements

- Python 2 or 3
- git
```
# Python 2
pip install -r requirements.txt

# Python 3
pip3 install -r python3_requirements.txt
```

# On Windows

** git must be inside PATH, or it will fail! **



## Usage

```
python git-downloader.py [URL]
```

`[URL]` is the url to the target website. For example, if you want to download `http://example.com[:port]/.git`, the `[URL]` should be `http://example.com[:port]`.
