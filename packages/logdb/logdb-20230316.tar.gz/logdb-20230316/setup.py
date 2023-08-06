import time
import glob
from distutils.core import setup

setup(
  name = 'logdb',
  packages = ['logdb'],
  version = time.strftime('%Y%m%d'),
  description = 'A simple queue - with only append/tail operations.',
  long_description = 'It uses Paxos for replication. Leaderless and highly available. Uses mTLS for privacy, authentication and autorization',
  author = 'Bhupendra Singh',
  author_email = 'bhsingh@gmail.com',
  url = 'https://github.com/magicray/logdb',
  keywords = ['queue', 'paxos', 'pubsub', 'mtls']
)
