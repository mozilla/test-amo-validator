from setuptools import setup, find_packages


setup(
    name='test-amo-validator',
    version='0.1',
    description='Functional tests for the amo-validator.',
    long_description=open('README.rst').read(),
    author='Matt Basta',
    author_email='me@mattbasta.com',
    url='http://github.com/mozilla/test-amo-validator',
    license='BSD',
    packages=find_packages(exclude=['addons']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[p.strip() for p in open('./requirements.txt') if
                      not p.startswith(('#', '-e'))],
)
