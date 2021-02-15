import sys
from os.path import abspath, dirname, join

paths = (
    abspath(join(dirname(dirname(__file__)), "src/services")),
    abspath(join(dirname(dirname(__file__)),
                    "src/services/text_preprocessor")),
    abspath(join(dirname(dirname(__file__)),
                    "src/services/t5_large_encoder")),
    abspath(join(dirname(dirname(__file__)),
                    "src/services/t5_large_summarizer")),
    abspath(join(dirname(dirname(__file__)),
                    "src/services/text_postprocessor"))
)

for p in paths:
    sys.path.insert(1, p)