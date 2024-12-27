import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='AIOdriver',
    version='0.1.2',
    author='Abhishek Ramawat',
    author_email='ramawatabhishek22@gmail.com',
    description='All in one driver',

    url='https://github.com/abhishake99/AIOdriver',
    project_urls = {
        "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    },
    license='MIT',
    packages=['AIOdriver'],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
