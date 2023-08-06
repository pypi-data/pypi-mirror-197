from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='superops-talon',
      version='0.4',
      description='Mailgun library to extract message quotations and signatures (talon-1.6.0)',
      long_description=readme(),
      url='https://pypi.org/project/superops-talon/',
      author='Superops',
      author_email='app.integrations@superops.ai',
      license='APACHE2',
      packages=['talon'],
      install_requires=[
          'markdown'
      ],
      zip_safe=False)