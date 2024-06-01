from setuptools import setup

setup(
    name="tmnt",
    version="0.0.0",
    description="Threat Modeling Naturally Tool",
    author="Tufts Security & Privacy Lab",
    packages=["tmnt","tmnt.dsl", "tmnt.dsl.core", "tmnt.dsl.util", "tmnt.dsl.visual","tmnt.kb","tmnt.engines"],
    package_data={
        "tmnt.kb": [
            "reference_data/cwe.xml",
            "reference_data/capec.xml",
            "reference_data/asvs.xml",
            "reference_data/asvs_ref.json",
            "reference_data/pytm_threatlib.json",
        ]
    },
)
