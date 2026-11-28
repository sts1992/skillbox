"""Offline checks for the GitHub review helper's authentication and file scope."""
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

PATH = Path(__file__).resolve().parents[1] / "review-pr/scripts/resolve_spec_context.py"
spec = importlib.util.spec_from_file_location("resolve_spec_context", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReviewBoundaries(unittest.TestCase):
    def test_repository_slug(self):
        self.assertEqual(mod._repository_slug("owner/repo.name"), ("owner", "repo.name"))
        for invalid in ("owner/another/repo", "owner/..", "owner/repo?ref=x"):
            with self.subTest(invalid=invalid), self.assertRaises(SystemExit):
                mod._repository_slug(invalid)

    def test_requires_explicit_absolute_workspace(self):
        with patch.dict(os.environ, {"OZ_REPO_ROOT": "relative"}):
            with self.assertRaises(SystemExit):
                mod._workspace_from_env()
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"OZ_REPO_ROOT": temp}):
            self.assertEqual(mod._workspace_from_env(), Path(temp).resolve())

    def test_valid_request_has_scoped_credential_and_timeout(self):
        with patch.object(mod._API_OPENER, "open") as open_request:
            response = open_request.return_value.__enter__.return_value
            response.status, response.headers = 200, {}
            response.read.return_value = b"[]"
            self.assertEqual(mod._gh_json("/repos/owner/repo/pulls", token="test-only")[1], [])
            request = open_request.call_args.args[0]
            self.assertEqual(request.full_url, "https://api.github.com/repos/owner/repo/pulls")
            self.assertEqual(request.unredirected_hdrs["Authorization"], "Bearer test-only")
            self.assertNotIn("Authorization", request.headers)
            self.assertEqual(open_request.call_args.kwargs["timeout"], 20)

    def test_refuses_non_api_destination_before_open(self):
        with patch.object(mod._API_OPENER, "open") as open_request:
            with self.assertRaises(SystemExit):
                mod._gh_request("https://example.invalid/", token="test-only")
            open_request.assert_not_called()

    def test_redirects_are_not_followed_and_are_not_returned_as_data(self):
        handler = next(h for h in mod._API_OPENER.handlers if isinstance(h, mod._RejectRedirects))
        self.assertIsNone(handler.redirect_request(None, None, 302, "", {}, "https://example.invalid/"))
        error = HTTPError(mod.API_ROOT, 302, "", {}, io.BytesIO())
        with patch.object(mod._API_OPENER, "open", side_effect=error):
            with self.assertRaisesRegex(SystemExit, "redirect refused"):
                mod._gh_request("/repos/owner/repo", token="test-only", allow_http_error=True)

    def test_pagination_scope(self):
        expected = "https://api.github.com/repos/owner/repo/pulls?page=2"
        self.assertEqual(mod._parse_next_link(f'<{expected}>; rel="next"'), expected)
        with self.assertRaises(SystemExit):
            mod._parse_next_link('<https://example.invalid/>; rel="next"')

    def test_local_spec_regular_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "specs/GH1"
            folder.mkdir(parents=True)
            (folder / "product.md").write_text("synthetic design", encoding="utf-8")
            self.assertEqual(mod.read_local_spec_files(root, 1), [("specs/GH1/product.md", "synthetic design")])

    def test_local_spec_disallows_link(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "specs/GH1"
            folder.mkdir(parents=True)
            target = folder / "fixture.md"
            target.write_text("synthetic design", encoding="utf-8")
            try:
                (folder / "product.md").symlink_to(target)
            except OSError as exc:
                self.skipTest(f"symlink unavailable: {exc}")
            with self.assertRaises(SystemExit):
                mod.read_local_spec_files(root, 1)


if __name__ == "__main__":
    unittest.main()
