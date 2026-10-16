import unittest

from app import app


class TestDashboardApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_loads_and_links_css(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"/static/style.css", response.data)
        self.assertIn(b"/static/dashboard.js", response.data)

    def test_static_files_are_served(self):
        css = self.client.get("/static/style.css")
        js = self.client.get("/static/dashboard.js")
        self.assertEqual(css.status_code, 200)
        self.assertEqual(css.mimetype, "text/css")
        self.assertEqual(js.status_code, 200)
        css.close()
        js.close()

    def test_invalid_severity_is_ignored(self):
        response = self.client.get("/?severity=nonsense")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
