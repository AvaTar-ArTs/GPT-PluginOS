import unittest
from pathlib import Path
from pluginos.registry import Registry
from pluginos.router import Router

class RouterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = Registry.from_directory(Path(__file__).parent)
        cls.router = Router(cls.registry)

    def test_quality_first_prefers_magnific_for_upscale(self):
        result = self.router.route('media.image.upscale', 'quality-first')
        self.assertIsNone(result.diagnostic)
        self.assertEqual(result.selected.provider.id, 'magnific')

    def test_private_local_never_widens_to_remote_provider(self):
        result = self.router.route('media.image.upscale', 'private-local')
        self.assertEqual(result.selected.provider.id, 'local-upscaler')
        self.assertTrue(all(c.provider.kind in {'local', 'first_party'} for c in result.candidates))

    def test_regulated_excludes_degraded_semrush(self):
        result = self.router.route('research.seo.keyword', 'regulated')
        self.assertIsNone(result.selected)
        self.assertIn('no eligible provider', result.diagnostic)

    def test_unknown_capability_returns_structured_diagnostic(self):
        result = self.router.route('does.not.exist', 'balanced')
        self.assertIsNone(result.selected)
        self.assertEqual(result.diagnostic, 'unknown capability: does.not.exist')

if __name__ == '__main__': unittest.main()
