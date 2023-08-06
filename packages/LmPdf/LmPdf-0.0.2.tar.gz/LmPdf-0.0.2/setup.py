from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='LmPdf',
    version='0.0.2',
    license='MIT License',
    author='Francisco Aparicio & Pedro Tercio',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pooiiufpi@gmail.com',
    keywords='Pdf',
    description=u'Traduzir paginas de um pdf e leitura do arquivo com voz do sistema',
    packages=['LmPdf'],
    install_requires=["requests", "pyttsx3", "PyPDF2", "pdfplumber", "googletrans"],)