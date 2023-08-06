from setuptools import setup, find_packages

with open('README.rst', mode='r', encoding='utf-8') as f:
    long_description = f.read()

author = 'am230'
name = 'pytohtml'
py_modules = [name]

setup(
    name=name,
    version="1.2.5",
    keywords=("html", "pythonic"),
    description="Write HTML with Pythonic Code",
    long_description=long_description,
    requires=["strbuilder", "Flask", "libsass"],
    license="MIT Licence",
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    url=f"https://github.com/{author}/py2html",
    author=author,
    author_email="am.230@outlook.jp",
    py_modules=py_modules,
    platforms="any",
)
