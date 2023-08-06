from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='meteorologicalData',
    version='0.1.2',
    license='MIT License',
    author='David Moura, Enzo Sá',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='davidmoura0102@gmail.com, enzosa90@gmail.com',
    description='Um simples pacote para retornar ou visualizar dados meteorológicos de uma determinada cidade',
    packages=['meteorologicalData'],
    install_requires=['folium', 'PyQt5', 'requests'],
)

