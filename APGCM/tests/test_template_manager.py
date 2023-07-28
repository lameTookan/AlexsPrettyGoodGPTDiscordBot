from templates import TemplateSelector, template_sample
import unittest
import exceptions
import logging


class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.tm: TemplateSelector = TemplateSelector(template_dict=template_sample)
        self.tm.logger.set_logging_level(logging.DEBUG)
        self.maxDiff = None
        self.sample_template = template_sample["gpt-4_default"]
        self.sample_template_name = "gpt-4_default"
        self.sample_template_id = 1
        self.sample_template_model = "gpt-4"

    def test_template_manager_init(self):
        """Tests that the template manager initializes correctly"""
        self.assertIsInstance(self.tm, TemplateSelector)
        self.assertEqual(self.tm.default_template_name, "gpt-4_default")

    def test_default_template(self):
        """Tests that the default template is set correctly"""
        self.assertEqual(self.tm.default_template, self.sample_template)

    def test_check_template_exists(self):
        """Tests that the check_template_exists method works as expected"""
        self.assertTrue(self.tm.check_template_exists("gpt-4_default"))

    def test_get_all_template_names(self):
        """Tests that the get_all_template_names method works as expected"""
        self.maxDiff = None
        self.assertEqual(
            set(self.tm.get_all_template_names()), set(template_sample.keys())
        )

    def test_get_template_by_name(self):
        """Tests that the get_template_by_name method works as expected"""
        self.assertEqual(
            self.tm.get_template(self.sample_template_name), self.sample_template
        )

    def test_bad_template_dict(self):
        """Tests that a bad template dict raises a BadTemplateError"""
        with self.assertRaises(exceptions.BadTemplateError):
            TemplateSelector(template_dict="not a dict")

    def test_bad_template(self):
        """Tests that a bad template raises a BadTemplateError"""
        with self.assertRaises(exceptions.BadTemplateError):
            TemplateSelector(template_dict={"bad": "template"})

    def test_bad_template_name(self):
        """Tests that a bad template name raises a TemplateNotFoundError"""
        with self.assertRaises(exceptions.TemplateNotFoundError):
            self.tm.get_template("not a template")

    def test_missing_info_keys(self):
        """Tests that a missing key in the info object raises a BadTemplateError"""
        test_dict = {
            "gpt-4_default": {
                "model": "gpt-4",
                "name": "gpt-4_default",
                "id": 1,
                "info": {"tags": ["gpt-4", "default", "chat"], "description": 23},
                "trim_object": {
                    "model": "gpt-4",
                },
                "chat_completion_wrapper": {
                    "model": "gpt-4",
                },
            },
        }
        with self.assertRaises(exceptions.BadTemplateError):
            TemplateSelector(template_dict=test_dict)

    def test_missing_trim_keys(self):
        """Tests that a missing key in the trim object raises a BadTemplateError"""

        test_dict = {
            "gpt-4_default": {
                "model": "gpt-4",
                "name": "gpt-4_default",
                "id": 1,
                "info": {"tags": ["gpt-4", "default", "chat"], "description": "test"},
                "trim_object": {},
                "chat_completion_wrapper": {
                    "model": "gpt-4",
                },
            }
        }
        with self.assertRaises(exceptions.BadTemplateError):
            TemplateSelector(template_dict=test_dict)

    def test_template_tag_search(self):
        """Tests that the template tag search works as expected"""
        sample_temp = {}
        sample_temp["gpt-4_default"] = self.sample_template
        test_ts = TemplateSelector(template_dict=sample_temp)
        self.assertEqual(test_ts.search_template_by_tag("gpt-4"), ["gpt-4_default"])

    def test_bad_default_template(self):
        """Tests that a bad default template name raises a TemplateNotFoundError"""
        with self.assertRaises(exceptions.TemplateNotFoundError):
            ts = TemplateSelector(
                template_dict=template_sample, default_template_name="not a template"
            )

    def test_good_template_dict(self):
        """Tests that a good template dict does not raise an exception"""
        try:
            ts = TemplateSelector(template_dict=template_sample)
        except:
            self.fail("TemplateSelector raised an exception when it should not have.")

    def test_get_template_info(self):
        """Tests that the get_template_info method works as expected"""
        self.assertEqual(
            self.tm.get_template_info("gpt-4_default"), self.sample_template["info"]
        )

    def tearDown(self) -> None:
        del self.tm


if __name__ == "__main__":
    unittest.main(verbosity=2)
