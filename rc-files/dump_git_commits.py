#!/usr/bin/python3
import argparse
from builtins import print
import getpass
import logging

import git

from offboard_base.misc_utils import get_source_root

logger = logging.getLogger(__name__)

def _process(args):
  repo = git.Repo(get_source_root())
  for commit in repo.iter_commits(author=args.author_name):
    for msg_line in commit.message.split('\n'):
      if msg_line.startswith('Differential Revision: '):
        cr = msg_line.replace('Differential Revision: ', '')
        break
    else:
      logger.error('No CR found in %s', commit.summary)
      continue
    if cr == 'http://cr.intra.xiaojukeji.com/{}'.format(args.last_cr):
      break
    print('%s (%s)' % (commit.summary, cr))

def main():
  logging.basicConfig(level=logging.INFO)
  parser = argparse.ArgumentParser('Dump git commits')
  parser.add_argument(
      'last_cr', help='Last CR to stop the iteration, e.g. D180340')
  parser.add_argument(
      '--author-name', default=getpass.getuser(), help='Git author name')
  parser.set_defaults(func=_process)
  args = parser.parse_args()
  args.func(args)


if __name__ == '__main__':
  main()