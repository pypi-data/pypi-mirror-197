from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf-8') as f:
    long_description = '\n'.join(map(str.strip, f.readlines()))

author = 'am230'
name = 'strbuilder'

setup(
    name=name,
    version="1.1.3",
    keywords=("builder"),
    description="A simple string builder",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT Licence",
    url=f"https://github.com/{author}/{name}",
    author=author,
    author_email="am.230@outlook.jp",
    py_modules=['strbuilder'],
    platforms="any",
    packages=find_packages()
)