import os
from setuptools import setup

branch = os.getenv("CI_COMMIT_REF_NAME", None)


def read(file_to_read):
    with open(file_to_read, 'r') as f:
        return f.read()


version = '0.1'

if branch == "develop" or branch == "master":
    version += f".dev{os.getenv('CI_BUILD_ID', None)}"

setup(name='3p-flask-restful-swagger-3',
      version=version,
      url='https://gitlab.com/john-ull/framework/flask-restful-swagger-3',
      zip_safe=False,
      packages=['flask_restful_swagger_3'],
      package_data={
        'flask_restful_swagger_3': [
        ]
      },
      description='Extract swagger specs from your flask-restful project.'
                  ' Project based on flask-restful-swagger-2 by Soeren Wegener.',
      author='Jonathan ULLINDAH',
      license='MIT',
      long_description=read('README.rst'),
      install_requires=['Flask-RESTful>=0.3.7']
      )
