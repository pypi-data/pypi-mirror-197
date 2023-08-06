from setuptools import setup

setup(
    name="preserves",
    version="0.17.3",
    author="Tony Garnock-Jones",
    author_email="tonyg@leastfixedpoint.com",
    license="Apache Software License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    packages=["preserves"],
    url="https://preserves.dev/",
    description="Experimental data serialization format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    python_requires=">=3.6, <4",
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)
