import unittest
from pathlib import Path
from pluginos.lockfile import build_lock, diff_locks
from pluginos.registry import Registry

class LockfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.from_directory(Path(__file__).parent)

    def test_graph_hash_is_deterministic(self):
        a = build_lock(self.registry)
        b = build_lock(self.registry)
        self.assertEqual(a['graph_sha256'], b['graph_sha256'])
        self.assertEqual(a['provider_count'], 12)
        self.assertEqual(a['capability_count'], 36)

    def test_diff_reports_only_changed_fields(self):
        diff = diff_locks({'a': 1, 'b': 2}, {'a': 1, 'b': 3, 'c': 4})
        self.assertEqual(diff, {'b': {'from': 2, 'to': 3}, 'c': {'from': None, 'to': 4}})

if __name__ == '__main__': unittest.main()
