# ...existing code...
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='AIOdriver',
    version='0.1.6',
    author='Abhishek Ramawat',
    author_email='ramawatabhishek22@gmail.com',
    description='All in one driver',

    url='https://github.com/abhishake99/AIOdriver',
    project_urls = {
        "Bug Tracker": "https://github.com/abhishake99/AIOdriver/issues"
    },
    license='MIT',
    packages=['AIOdriver'],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.10.0",
        "requests>=2.28.0",
        "selenium-wire>=5.1.0",
        "undetected-chromedriver>=3.4.0"
    ],
     long_description=long_description,
     long_description_content_type="text/markdown"
 )
# ...existing code...