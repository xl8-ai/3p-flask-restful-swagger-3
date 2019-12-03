from setuptools import setup


def read(file_to_read):
    with open(file_to_read, 'r') as f:
        return f.read()


setup(name='flask-restful-swagger-3',
      version='0.1',
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
      long_description=read('README.md'),
      install_requires=['Flask-RESTful>=0.3.7'],
      tests_require=['nose'],
      test_suite='nose.collector'
      )
