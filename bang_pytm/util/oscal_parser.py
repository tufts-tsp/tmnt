import yaml
from bang_pytm.core.control import Control, ControlCatalog, Part

class OSCALParser:
    
    # CREATE CONTROL CATALOG

    # get metadata for control catalog
    def parse_metadata(data):
        return ControlCatalog.Metadata(
            title=data['title'],
            published=data['published'],
            last_modified=data['last_modified'],
            version=data['version'],
            oscal_version=['oscal_version']
        )

