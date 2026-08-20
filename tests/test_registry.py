import unittest
from pathlib import Path
from pluginos.registry import Registry

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = Registry.from_directory(Path(__file__).parent)

    def test_registry_resolves_all_provider_capabilities(self):
        self.assertEqual(len(self.registry.providers), 12)
        self.assertEqual(len(self.registry.capabilities), 36)
        self.assertEqual(len(self.registry.policies), 5)
        for provider in self.registry.providers:
            for capability in provider.capabilities:
                self.assertIn(capability, self.registry.capability_by_id)

    def test_duplicate_provider_ids_are_rejected(self):
        p = list(self.registry.providers)
        with self.assertRaisesRegex(ValueError, "duplicate provider id"):
            Registry(p + [p[0]], list(self.registry.capabilities), list(self.registry.policies))

if __name__ == '__main__': unittest.main()
