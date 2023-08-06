from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='nanologic',
    version='0.1',
    description='Simple package for simple logical operations',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Alexander Isaychikov',
    author_email='alipheesa@gmail.com',
    keywords=['nanologic', 'logic'],
    url='https://github.com/alipheesa/nanologic',
    download_url='https://pypi.org/project/nanologic/'
)

install_requires = [
    'math',
    'itertools',
    'numpy'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)