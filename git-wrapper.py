import psutil
import sys
import os
from subprocess import PIPE
from subprocess import call
import time
import glob

#handle = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'handle64.exe')
handle = 'handle64.exe'

# Get paths from command line
paths = list(filter(lambda x: os.path.isdir(x), glob.glob(os.path.join(os.path.abspath(os.getcwd()), '*'))))
argv = sys.argv[1:]
for arg in argv:
  if os.path.isdir(arg):
    paths.append(os.path.abspath(arg))

# Look for open files in paths, and loop until closed
done = 1
count = 0
while done != 0 or count > 10:
  sys.stdout.flush()
  done = 0
  for path in paths:
    p = psutil.Popen([handle, "-nobanner", path], stdout=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    result = p.wait()
    if result == 0: 
      print(stdout, file=sys.stderr)
      done = done+1
  if done:
    time.sleep(1)
  count = count + 1

sys.stdout.flush()
sys.stderr.flush()

# Run git
argv.insert(0,"git.exe")
p = psutil.Popen(argv, stderr=sys.stderr, stdout=sys.stdout)
p.communicate()
sys.exit(p.wait())
