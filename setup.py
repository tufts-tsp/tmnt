from setuptools import setup

setup(name='bang_pytm',
      version='0.0.0',
      description='Not PyTM',
      author='Tufts Security & Privacy Lab',
      packages=['bang_pytm',
                'bang_pytm.core',
                'bang_pytm.engine',
                'bang_pytm.util',
                'bang_pytm.visual'],
      package_data={
          "bang_pytm.util":[
              "reference_data/cwe.xml",
              "reference_data/capec.xml",
              "reference_data/asvs.xml",
              "reference_data/asvs_ref.json",
          ]
      }
      )