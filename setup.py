from setuptools import setup

setup(name='tmnt_dsl',
      version='0.0.0',
      description='Not PyTM',
      author='Tufts Security & Privacy Lab',
      packages=['tmnt_dsl',
                'tmnt_dsl.core',
                'tmnt_dsl.engine',
                'tmnt_dsl.util',
                'tmnt_dsl.visual'],
      package_data={
          "tmnt_dsl.util":[
              "reference_data/cwe.xml",
              "reference_data/capec.xml",
              "reference_data/asvs.xml",
              "reference_data/asvs_ref.json",
          ]
      }
      )
