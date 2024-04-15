import unittest

from bang_pytm.util.oscal_parser import OSCALParser
from bang_pytm.core.control import Control, Part, ControlCatalog, Metadata

class TestOSCALParser(unittest.TestCase):

    def setUp(self):

        self.parser = OSCALParser()
        self.example_data = {
            "catalog": {
                "id": "uuid-5678",
                "metadata": {
                    "title": "Catalog Test",
                    "published": "2021-01-01T12:00:00Z",
                    "last-modified": "2021-01-02T12:00:00Z",
                    "version": "2.0",
                    "oscal-version": "1.0.0"
                },
                "groups": [{
                    "id": "grp1",
                    "title": "Top Group",
                    "groups": [{  # nested group
                        "id": "grp1.1",
                        "title": "Nested Group",
                        "controls": [{
                            "id": "ctrl1.1",
                            "title": "Nested Control",
                            "parts": [{
                                "id": "part1.1",
                                "name": "statement",
                                "prose": "Statement of the nested control."
                            }, {
                                "id": "part1.2",
                                "name": "guidance",
                                "prose": "Guidance for the nested control."
                            }]
                        }]
                    }],
                    "controls": [{  # controls in the top group
                        "id": "ctrl1",
                        "title": "Top Control",
                        "parts": [{
                            "id": "part1",
                            "name": "statement",
                            "prose": "Ensure compliance with policy."
                        }, {
                            "id": "part2",
                            "name": "guidance",
                            "prose": "Guidance on compliance."
                        }]
                    }]
                }]
            }
        }
        
    
    def test_parse_metadata(self):

        metadata_data = self.example_data["catalog"]["metadata"]
        metadata = self.parser.parse_metadata(metadata_data)
        title = metadata.get_title()
        published = metadata.get_published()
        last_modified = metadata.get_last_modified()
        version = metadata.get_version()
        oscal_version_text = metadata.get_oscal_version()

        self.assertEqual(title, "Catalog Test")
        self.assertEqual(published, "2021-01-01T12:00:00Z")
        self.assertEqual(last_modified, "2021-01-02T12:00:00Z")
        self.assertEqual(version, "2.0")
        self.assertEqual(oscal_version_text, "1.0.0")
    
    def test_parse_part(self):
        pass