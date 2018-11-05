import requests
import os
import errno
import sys
import subprocess
import re

def check_and_create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

def download_file(base_url, local_dir, relative_path):
    remote_path = base_url + "/" + relative_path
    local_path = os.path.join(local_dir, relative_path)

    print "downloading the file from %s to %s" % (remote_path, local_path)

    r = requests.get(remote_path, stream=True)
    if r.status_code == 200:
        check_and_create_dir(local_path[0: local_path.rfind("/")])
        with open(local_path, "wb+") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print "cannot download %s (status code: %d)" % (remote_path, r.status_code)

def exec_and_cap_output(cmd, working_dir):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
    out, err = p.communicate()
    return (out, err)

def find_sha1(message):
    SHA1s = []
    for m in re.finditer(r"\b[0-9a-f]{40}\b", message):
        SHA1s.append(m.group(0))
    return SHA1s

# Read command line arguments
if len(sys.argv) < 2:
    print "Usage: python %s [URL]" % sys.argv[0]
    sys.exit(1)

url = sys.argv[1]

# TODO: Maybe I should check if it is possible to download a file in .git first ?

# Set my working directory for executing commands
working_dir = url
working_dir = working_dir.replace("http://", "")
working_dir = working_dir.replace("http://", "")
working_dir = os.path.join(os.getcwd(), working_dir)

print "Set the working directory: %s" % working_dir

# TODO: If the directory exists, delete it maybe ?
check_and_create_dir(working_dir)

# Initialize an empty repository
exec_and_cap_output(["git", "init"], working_dir)

# Download basic files
git_dir = ".git/"
basic_files = [
    # Root
    "HEAD",
    "config",
    "COMMIT_EDITMSG",

    # Refs
    "refs/heads/master",

    # Logs
    "logs/HEAD",
    "logs/refs/heads/master"
]

for file_name in basic_files:
    download_file(url, working_dir, git_dir + file_name)

# Download objects
while True:

    # Perform git checking
    (out, err) = exec_and_cap_output(["git", "fsck"], working_dir)
    SHA1s = find_sha1(out)
    SHA1s = SHA1s + find_sha1(err)

    # for SHA1 in SHA1s:
    #     print "SHA1: %s" % SHA1

    # No missing file
    if len(SHA1s) == 0:
        break

    # Download missing objects
    for SHA1 in SHA1s:
        git_path = os.path.join(".git","objects", SHA1[0:2], SHA1[2:40])
        path = os.path.join(working_dir, git_path)
        if not os.path.isfile(path):
            download_file(url, working_dir, git_path)

print "Downloading complete"

# Checking out the master branch
exec_and_cap_output(["git", "checkout", "master"], working_dir)
