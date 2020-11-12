import sys
from os.path import abspath, dirname, join

src_path = abspath(join(dirname(dirname(__file__)), "src"))
sys.path.insert(1, src_path)