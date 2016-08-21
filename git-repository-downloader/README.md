# Git Repository Downloader

We love using git. Many web developers love, too. The developers usually treat the whole directory containing a website as a git repository. In this case, a directory `.git` appears inside the directory of the web pages. Sometimes someone putting a website in public forgets to close the permission of downloading the contents of directory `.git`. Although we might not have the permission of listing the files inside `.git`, we can still figure out what exactly are inside `.git` using the knowledge of git internals.

After reading the documents about [git internals](https://git-scm.com/book/en/v1/Git-Internals), I wrote this script to automatically download and recover the git repository of a given website. The website should open the permission of downloading the contents inside directory `.git`. Otherwise, this script will not work.

## Requirement

- Python 2 (I am not sure if it can work on Python 3)
- [HTTP Requests Library for Python](https://github.com/kennethreitz/requests)

If you have already had Python, just use `pip install requests` to install the Requests library.

## Usage

```
python git-downloader.py [URL]
```

`[URL]` is the url to the target website. For example, if you want to download `http://example.com/.git`, the `[URL]` should be `http://example.com`.
