from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='socianAuthPyTest',
    version='0.1.7',
    description='socianAuthPyTest test publish.',
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='socian',
    author_email='socian@socian.ai',
)

install_requires=[
    "requests >= 2.27.1"
]
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)

