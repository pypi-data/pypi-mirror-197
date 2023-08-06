import setuptools

setuptools.setup(
  name = 'id4eo-scim-client',
  version = '1.0.1',
  author = 'ID4EO',
  author_email = 'joao.matos@elecnor.es',
  description = 'Python library to interact with SCIM protocol',
  url = 'https://stash.elecnor-deimos.com/projects/GSC4EO/repos/id4eo/browse/src/scim-client',
  packages=setuptools.find_packages(),
  license='apache-2.0',
  keywords = ['SCIM', 'Client', 'ID4EO','user','management'],
  classifiers=[
    'Development Status :: 3 - Alpha',                      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
  ],
  python_requires='>=3.6',
)