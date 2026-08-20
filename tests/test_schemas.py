import json, unittest
from pathlib import Path

class SchemaTests(unittest.TestCase):
    def test_all_schema_files_are_valid_json_and_have_schema_marker(self):
        root = Path(__file__).parents[1] / 'schemas'
        files = sorted(root.glob('*.schema.json'))
        self.assertGreaterEqual(len(files), 7)
        for path in files:
            payload = json.loads(path.read_text())
            self.assertEqual(payload['$schema'], 'https://json-schema.org/draft/2020-12/schema')
            self.assertEqual(payload['type'], 'object')

if __name__ == '__main__': unittest.main()
