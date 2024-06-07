import unittest

from tmnt.util.parsers import OSCALParser
from tmnt.dsl.control import Control, Part, ControlCatalog, Metadata


class TestOSCALParser(unittest.TestCase):
    def setUp(self):
        self.parser = OSCALParser()
        self.example_data = {
            "catalog": {
                "id": "uuid-5678",
                "metadata": {
                    "title": "Complex Catalog",
                    "published": "2021-01-01T12:00:00Z",
                    "last-modified": "2021-01-02T12:00:00Z",
                    "version": "2.0",
                    "oscal-version": "1.0.0",
                },
                "groups": [
                    {
                        "id": "grp1",
                        "title": "Top Group",
                        "props": [{"name": "priority", "value": "high"}],
                        "groups": [
                            {
                                "id": "grp1.1",
                                "title": "Nested Group",
                                "props": [
                                    {"name": "importance", "value": "critical"}
                                ],
                                "controls": [
                                    {
                                        "id": "ctrl1.1",
                                        "title": "Nested Control",
                                        "props": [
                                            {
                                                "name": "security_level",
                                                "value": "high",
                                            }
                                        ],
                                        "parts": [
                                            {
                                                "id": "part1.1",
                                                "name": "statement",
                                                "prose": "Statement of the nested control.",
                                            },
                                            {
                                                "id": "part1.2",
                                                "name": "fake_name",
                                                "prose": "Guidance for the nested control.",
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                        "controls": [
                            {
                                "id": "ctrl1",
                                "title": "Top Control",
                                "props": [
                                    {
                                        "name": "security_level",
                                        "value": "medium",
                                    }
                                ],
                                "parts": [
                                    {
                                        "id": "part1",
                                        "name": "statement",
                                        "prose": "Ensure compliance with policy.",
                                    },
                                    {
                                        "id": "part2",
                                        "name": "guidance",
                                        "prose": "Guidance on compliance.",
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        }
        return super().setUp()

    def test_parse_metadata(self):
        metadata_data = self.example_data["catalog"]["metadata"]
        metadata = self.parser.parse_metadata(metadata_data)
        title = metadata.title
        published = metadata.published
        last_modified = metadata.last_modified
        version = metadata.version
        oscal_version_text = metadata.oscal_version

        self.assertEqual(title, "Complex Catalog")
        self.assertEqual(published, "2021-01-01T12:00:00Z")
        self.assertEqual(last_modified, "2021-01-02T12:00:00Z")
        self.assertEqual(version, "2.0")
        self.assertEqual(oscal_version_text, "1.0.0")

    def test_parse_part(self):
        good_part_data = self.example_data["catalog"]["groups"][0]["groups"][
            0
        ]["controls"][0]["parts"][0]
        faulty_part_data = self.example_data["catalog"]["groups"][0]["groups"][
            0
        ]["controls"][0]["parts"][1]

        print("Part Data: " + str(good_part_data))
        print("Faulty Part Data: " + str(faulty_part_data))

        good_part = self.parser.parse_part(good_part_data)

        good_part_name = good_part.part_name
        good_part_id = good_part.part_id
        good_part_prose = good_part.part_prose

        self.assertEqual(good_part_name, "statement")
        self.assertEqual(good_part_id, "part1.1")
        self.assertEqual(good_part_prose, "Statement of the nested control.")

        # does not have a valid name
        with self.assertRaises(ValueError):
            faulty_part = self.parser.parse_part(faulty_part_data)

    # def test_parse_control(self):

    #     control_data = self.example_data["catalog"]["groups"][0]["controls"][0]
    #     control = self.parser.parse_control(control_data)

    #     control_id = control.id
    #     control_title = control.title
    #     control_props = control.prop
    #     control_parts = control.parts

    #     statement_part, guidance_part = control_parts[0], control_parts[1]

    #     self.assertEqual(control_id, "ctrl1")
    #     self.assertEqual(control_title, "Top Control")

    #     self.assertEqual(control_props["security_level"], "medium")

    #     self.assertEqual(statement_part.part_name, "statement")
    #     self.assertEqual(statement_part.part_id, "part1")
    #     self.assertEqual(statement_part.part_prose, "Ensure compliance with policy.")

    #     self.assertEqual(guidance_part.part_name, "guidance")
    #     self.assertEqual(guidance_part.part_id, "part2")
    #     self.assertEqual(guidance_part.part_prose, "Guidance on compliance.")

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
