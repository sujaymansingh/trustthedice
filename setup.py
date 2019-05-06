from setuptools import find_packages, setup


setup(
    name="trustthedice",
    version="0.0.2",
    py_modules=["trustthedice"],
    author="Sujay Mansingh",
    author_email="info@sujaymansingh.com",
    description="Let random numbers rule your life!",
    url="https://github.com/sujaymansingh/trustthedice",
    install_requires=["attrs==19.1.0", "black==19.3b0", "Click==7.0", "pytest==4.4.1"],
    entry_points="""
        [console_scripts]
        trustthedice=trustthedice.cli:main
    """,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
