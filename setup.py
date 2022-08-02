from importlib.metadata import entry_points
import setuptools

with open("README.md", "r", encoding="utf-8") as desc_file:
    long_description = desc_file.read()

setuptools.setup(
    name = "Automate LinkedIn",
    version = "0.1.2",
    author = "Selmi Abderrahim",
    author_email = "contact@selmi.tech",
    description = "Automate LinkedIn with Python and Selenium.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/SelmiAbderrahim/automate-linkedin",
    projects_urls = {
        "Bug Tracker": "https://github.com/SelmiAbderrahim/automate-linkedin/issues"
    },
    entry_points = {
        'console_scripts': [
            'autoln=automate_linkedin.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords = "linkedin bot built with Python and Selenium",
    license = "MIT",
    packages = setuptools.find_packages(),
    install_requires = [
        "beautifulsoup4==4.11.1",
        "click==8.1.3",
        "easy-py-selenium==0.1.4",
        "loguru==0.6.0",
        "python-decouple==3.6",
    ]
)   