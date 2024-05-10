from setuptools import setup

setup(name='tmnt_dsl',
      version='0.0.0',
      description='DSL for the Threat Modeling Naturally Tool',
      author='Tufts Security & Privacy Lab',
      packages=['tmnt_dsl',
                'tmnt_dsl.core',
                'tmnt_dsl.util',
                'tmnt_dsl.visual'],
      )
