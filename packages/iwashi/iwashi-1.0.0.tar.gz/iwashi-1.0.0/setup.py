from setuptools import setup, find_packages

with open('README.rst', mode='r', encoding='utf-8') as f:
    long_description = f.read()

author = 'am230'
name = 'iwashi'
py_modules = [name]

setup(
    name=name,
    version="1.0.0",
    keywords=("generator"),
    description="Link Tree Generator",
    long_description=long_description,
    install_requires=["Flask", "pytohtml", "py2js", "bs4", "yt-dlp"],
    license="MIT Licence",
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    url=f"https://github.com/{author}/{name}",
    author=author,
    author_email="am.230@outlook.jp",
    py_modules=py_modules,
    platforms="any",
)
