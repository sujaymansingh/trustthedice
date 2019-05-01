from setuptools import setup

setup(
    name="trustthedice",
    version="0.0.1",
    py_modules=["trustthedice"],
    install_requires=[
        "attrs==19.1.0",
        "Click==7.0",
    ],
    entry_points="""
        [console_scripts]
        trustthedice=trustthedice:cli.main
    """,
)
