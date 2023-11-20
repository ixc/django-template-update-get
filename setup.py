import setuptools
import template_update_get

setuptools.setup(
    name='django-template-update-get',
    version=template_update_get.__version__,
    author='Interaction Consortium',
    author_email='studio@interaction.net.au',
    url='https://github.com/ixc/django-template-update-get',
    description='Adds an `update_GET` template tag that allows you to '
                'substitute parameters into the current '
                'request\'s GET parameters',
    long_description='Documentation at https://github.com/ixc/django-template-update-get',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.0',
    requires=['django (>=3.0)'],
)
