import setuptools
import template_update_get

setuptools.setup(
    name='django-template-update-get',
    version=template_update_get.__version__,
    author='Interaction Consortium',
    author_email='studio@interaction.net.au',
    url='https://github.com/ixc/django-template-update-get',
    description='Adds an `update_GET` template tag that allows you to substitute parameters into the current '
                'request\'s GET parameters',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
)
