import io, json, tempfile, unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from pluginos.cli import main

class CliTests(unittest.TestCase):
    @property
    def data_dir(self): return str(Path(__file__).parent)

    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(['--data-dir', self.data_dir, *args])
        return rc, out.getvalue(), err.getvalue()

    def test_validate_command(self):
        rc, out, err = self.call('validate')
        self.assertEqual(rc, 0)
        self.assertIn('OK: 12 providers, 36 capabilities, 5 policies', out)
        self.assertEqual(err, '')

    def test_route_json_never_implies_authorization(self):
        rc, out, _ = self.call('route', 'media.image.upscale', '--policy', 'quality-first', '--json')
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload['selected'], 'magnific')
        self.assertFalse(payload['authorization_implied'])

    def test_lock_command_writes_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'lock.json'
            rc, out, _ = self.call('lock', '--output', str(path))
            self.assertEqual(rc, 0)
            self.assertTrue(path.exists())
            self.assertEqual(json.loads(path.read_text())['schema'], 'pluginos.lock.v1')

    def test_scan_json_reports_inventory(self):
        rc, out, _ = self.call('scan', '--json')
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload['providers'], 12)
        self.assertEqual(payload['status_counts']['degraded'], 1)

    def test_overlaps_finds_multi_provider_capability(self):
        rc, out, _ = self.call('overlaps', '--json')
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload['media.image.upscale'], ['magnific','cloudinary','local-upscaler'])

    def test_benchmark_accepts_domain_suite(self):
        rc, out, _ = self.call('benchmark', 'media', '--policy', 'quality-first', '--json')
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload['mode'], 'metadata_snapshot')
        self.assertEqual(payload['results']['media.image.upscale'][0]['provider'], 'magnific')

    def test_export_site_writes_compiled_dataset(self):
        with tempfile.TemporaryDirectory() as td:
            rc, out, _ = self.call('export-site', td)
            self.assertEqual(rc, 0)
            self.assertTrue((Path(td)/'compiled.json').exists())
            self.assertEqual(json.loads((Path(td)/'providers.json').read_text())['version'], '0.2.0')

if __name__ == '__main__': unittest.main()
