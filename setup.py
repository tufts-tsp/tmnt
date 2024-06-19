from setuptools import setup

setup(
    name="tmnpy",
    version="0.0.0",
    description="Threat Modeling Naturally in Python",
    author="Tufts Security & Privacy Lab",
    packages=[
        "tmnpy",
        "tmnpy.dsl",
        "tmnpy.kb",
        "tmnpy.engines",
        "tmnpy.util",
    ],
    package_data={
        "tmnpy.kb": [
            "reference_data/cwe.xml",
            "reference_data/capec.xml",
            "reference_data/asvs.xml",
            "reference_data/asvs_ref.json",
            "reference_data/pytm_threatlib.json",
            "reference_data/catalog.yaml",
        ]
    },
)
