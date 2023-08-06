from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='socianAuthPySDK',
    version='0.1.8',
    description='socianAuthPySDK test publish.',
    long_description=README,
    license='MIT',
    packages=["socianAuthPySDK"],
    author='socian',
    author_email='contact@socian.ai',
)

install_requires=[
    "requests >= 2.27.1"
]
if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)

