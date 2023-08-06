"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
import unittest
from unittest.mock import MagicMock, patch

from sungai.sungai import DirectoryRater, depth_set, get_r2_ln, nested_sum


class TestUtils(unittest.TestCase):
    """Test sungai utils."""

    def test_get_r2_ln(self):
        """Test linear regression."""
        assert round(get_r2_ln([17, 7, 4, 3])[2], 5) == 0.94668
        assert get_r2_ln([1, 0])[2] == 1.0
        assert get_r2_ln([0, 0])[2] == 0.0
        assert get_r2_ln([2, 2, 2, 2, 2])[2] == 0.0

    def test_nested_sum(self):
        """Test sum of nested list."""
        assert nested_sum([3, [4, 4, 2, 0], 0, 2, [3, [4, 2]]]) == 24
        assert nested_sum([3, 4, 5]) == 12

    def depth_set(self):
        """Test depth_set."""
        assert depth_set(
            [],
            0,
            1,
        ) == [1]

        assert depth_set(
            [[], 0, 3],
            1,
            2,
        ) == [[2], 0, 3]

        assert depth_set(
            [[2], 3, 0],
            1,
            0,
        ) == [[0, 2], 3, 0]

        assert depth_set(
            [[[], 2, 0], 3, 0],
            2,
            2,
        ) == [[[[2], 2, 0], 3, 0], 3, 0]


class TestDirectoryRater(unittest.TestCase):
    """Test DirectoryRater."""

    def setUp(self):
        """Set up test fixtures.

        tests/directory_tree/
        ├── 1.cpp
        ├── 2.cpp
        ├── 3.cpp
        ├── 4.cpp
        ├── 5.cpp
        ├── 6.cpp
        ├── blahA
        │   ├── 1.js
        │   ├── 1.md
        │   ├── 1.py
        │   ├── blah1
        │   │   ├── 1
        │   │   │   ├── 1.txt
        │   │   │   └── 4.py
        │   │   ├── 2.py
        │   │   └── 3.py
        │   ├── blah2
        │   │   └── 1
        │   │       ├── 1
        │   │       │   ├── 2.txt
        │   │       │   ├── 3.txt
        │   │       │   ├── 4.txt
        │   │       │   ├── 5.txt
        │   │       │   └── 6.txt
        │   │       ├── 2
        │   │       │   └── 2.js
        │   │       └── 3.js
        │   └── blah3
        │       ├── 1
        │       │   └── empty
        │       ├── 10.py
        │       ├── 10.txt
        │       ├── 11.py
        │       ├── 11.txt
        │       ├── 12.py
        │       ├── 13.py
        │       ├── 14.py
        │       ├── 15.py
        │       ├── 16.py
        │       ├── 5.py
        │       ├── 6.py
        │       ├── 7.py
        │       ├── 7.txt
        │       ├── 8.py
        │       ├── 8.txt
        │       ├── 9.py
        │       └── 9.txt
        ├── blahB
        │   ├── 1
        │   │   ├── 1
        │   │   │   ├── 1
        │   │   │   │   └── empty
        │   │   │   └── 2
        │   │   │       └── 10.cpp
        │   │   ├── 42.cpp
        │   │   └── 43.cpp
        │   ├── 2
        │   │   ├── 11.cpp
        │   │   └── 12.cpp
        │   ├── 3
        │   │   └── 13.cpp
        │   └── 9.cpp
        └── blahC
            ├── 7.cpp
            └── 8.cpp

        """
        self.mock_os_walk = MagicMock()

        self.patcher = patch('os.walk', self.mock_os_walk)
        self.patcher.start()

        self.mock_os_walk.return_value = [
            (
                'tests/directory_tree',
                ['blahA', 'blahB', 'blahC'],
                [f'{i}.txt' for i in range(6)],
            ),
            (
                'tests/directory_tree/blahA',
                ['blah1', 'blah2', 'blah3'],
                [f'{i}.txt' for i in range(3)],
            ),
            (
                'tests/directory_tree/blahA/blah1',
                ['1'],
                [f'{i}.txt' for i in range(2)],
            ),
            (
                'tests/directory_tree/blahA/blah1/1',
                [],
                [f'{i}.txt' for i in range(2)],
            ),
            (
                'tests/directory_tree/blahA/blah2',
                ['1'],
                [],
            ),
            (
                'tests/directory_tree/blahA/blah2/1',
                ['1', '2'],
                [f'{i}.txt' for i in range(1)],
            ),
            (
                'tests/directory_tree/blahA/blah2/1/1',
                [],
                [f'{i}.txt' for i in range(5)],
            ),
            (
                'tests/directory_tree/blahA/blah2/1/2',
                [],
                [f'{i}.txt' for i in range(1)],
            ),
            (
                'tests/directory_tree/blahA/blah3',
                [],
                [f'{i}.txt' for i in range(17)],
            ),
            (
                'tests/directory_tree/blahB',
                ['1', '2', '3'],
                [f'{i}.txt' for i in range(1)],
            ),
            (
                'tests/directory_tree/blahB/1',
                ['1'],
                [f'{i}.txt' for i in range(2)],
            ),
            (
                'tests/directory_tree/blahB/1/1',
                ['2'],
                [],
            ),
            (
                'tests/directory_tree/blahB/1/1/2',
                [],
                [f'{i}.txt' for i in range(1)],
            ),
            (
                'tests/directory_tree/blahB/2',
                [],
                [f'{i}.txt' for i in range(2)],
            ),
            (
                'tests/directory_tree/blahB/3',
                [],
                [f'{i}.txt' for i in range(1)],
            ),
            (
                'tests/directory_tree/blahC/',
                [],
                [f'{i}.txt' for i in range(2)],
            ),
        ]

    def tearDown(self):
        """Tear down test fixtures."""
        self.patcher.stop()

    def test_get_structure(self):
        """Test get_structure method."""
        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        directory_rater.run(False, 1.0, quiet=True)

        correct_structure = [31, 7, 6, 2, 0]
        assert directory_rater.structure == correct_structure

    def test_score_nodes(self):
        """Test score_nodes method."""

    def test_run(self):
        """Test sungai output."""
        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        assert directory_rater.run(False, 0.8786859111811026, quiet=True) == 0

        directory_rater = DirectoryRater(
            "tests/directory_tree",
        )
        assert directory_rater.run(False, 1.0, quiet=True) == 1

        nodes = [
            [2, 0],
            [2, 2, 0],
            [5, 0],
            [1, 0],
            [5, 1, 1, 0],
            [7, 0, 0],
            [17, 0, 0],
            [17, 7, 4, 3, 0],
            [1, 0],
            [1, 0, 0],
            [2, 1, 0],
            [2, 0, 0],
            [1, 0],
            [3, 2, 1, 1, 0],
            [2, 0],
            [31, 7, 6, 2, 0],
        ]

        for i, node in enumerate(directory_rater.get_nodes()):
            assert node[1] == sum(nodes[i])
