import unittest
from pathlib import Path
from pluginos.compile import compile_registry
from pluginos.registry import Registry

class CompileTests(unittest.TestCase):
    def test_compiler_emits_route_projection_for_every_capability_and_policy(self):
        registry = Registry.from_directory(Path(__file__).parent)
        compiled = compile_registry(registry)
        self.assertEqual(compiled['schema'], 'pluginos.compiled.v1')
        self.assertEqual(set(compiled['routes']), set(registry.capability_by_id))
        for policy_map in compiled['routes'].values():
            self.assertEqual(set(policy_map), set(registry.policy_by_id))
        self.assertEqual(compiled['routes']['media.image.upscale']['quality-first']['selected'], 'magnific')

if __name__ == '__main__': unittest.main()
