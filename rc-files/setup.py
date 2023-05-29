#!/usr/bin/python

"""
Replace existing rc-files with soft links according to the mapping in FILE_TUPLES.
"""

import os
import shutil

# Tuple of file in local directory (link target) and link source
FILE_TUPLES = [
    ('bashrc', '~/.bashrc'),
    ('sshconfig', '~/.ssh/config'),
    ('vimrc', '~/.vimrc'),
    ('magicbook.txt', '~/magicbook.txt'),
    ('gitconfig', '~/.gitconfig'),
]

for target, source in FILE_TUPLES:

    # So that the script can run from other places.
    target=os.path.join(os.path.dirname(__file__), target)
    if not os.path.isfile(target):
        raise RuntimeError("Missing source file: {}".format(target))

    # To replace "~" with home directory.
    source = os.path.expanduser(source)
    if os.path.isfile(source):
        print "Moving %s to /tmp" % source
        shutil.move(source, "/tmp")

    os.system("cd {source_dir}; ln -s {target} {name}".format(
        source_dir=os.path.dirname(source),
        target=os.path.abspath(target),
        name=os.path.basename(source)))

print "Done"
