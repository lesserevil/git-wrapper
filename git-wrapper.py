import psutil
import sys
import os
from subprocess import PIPE
from subprocess import call
import time
import glob

MAX_COUNT=5

argv = sys.argv[1:]
argv.insert(0,"git.exe")

count = 0
result = 1
while result != 0 and count < MAX_COUNT:
  p = psutil.Popen(argv, stderr=sys.stderr, stdout=sys.stdout)
  p.communicate()
  result = p.wait()

  sys.stdout.flush()
  sys.stderr.flush()

  if result:
    if count < MAX_COUNT - 1:
      print("\ngit.exe failed with result %d, retrying...\n" % result , file=sys.stderr)
      sys.stderr.flush()
    time.sleep(3)
  count = count + 1

sys.exit(result)
