from setuptools import setup
import versioneer


setup(name='jobrun',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='Jason Rudy',
      author_email='jcrudy@gmail.com',
      url='https://github.com/jcrudy/jobrun',
      packages=['oreader'],
      install_requires=['networkx', 'scikit-learn'],
      tests_require=['nose']
     )