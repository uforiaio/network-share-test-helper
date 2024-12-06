import os

# Create main directories
dirs = [
    'src',
    'src/analyzers',
    'src/metrics',
    'src/detectors',
    'src/utils',
    'src/utils/version',
    'scripts',
    'tests',
    'tests/test_analyzers',
    'tests/test_metrics',
    'tests/test_detectors',
    'tests/test_utils'
]

# Create directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)
    init_file = os.path.join(dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('"""Module initialization."""\n')
