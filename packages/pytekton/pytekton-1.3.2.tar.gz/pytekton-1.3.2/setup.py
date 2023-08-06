from setuptools import setup
import pypandoc
import os

folder = 'pytekton'
'''
helf_path = os.getcwd() + f'/{folder}/README.md'
count_instances = 0
count_instances = helf_path.count('pip-install')
try:
      if count_instances != 1:
            long_description = pypandoc.convert_file(helf_path, 'md')
      else:
            raise "Coudnt Convert README File"
except(FileNotFoundError):
      # long_description = open('README.md').rt,ead()
      raise "Fail README.md dont exists"
'''
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_kwargs = dict(
      name='pytekton',
      version='1.3.2',
      description='PyFolio Tekton',
      packages=[folder],
      package_data={
            'pytekton': ['LICENSE.txt', 'README.md'],
      },
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
            'pyfolio>=0.9.2'
      ],
      author="Quantopian and Everton Mendes",
      author_email="emendes@tektonfinance.com",
      zip_safe=False,
      include_package_data=True
)

#if count_instances == 0:
#      setup_kwargs['description']=long_description
#      setup_kwargs['long_description'] = long_description

setup(**setup_kwargs)