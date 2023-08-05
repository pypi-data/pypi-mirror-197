import setuptools


setuptools.setup(
    name="ke_ranking_package",
    version="0.0.11",
    description="Useful Functions for search & ranking",
    py_modules=["helpers", "paths", "visualize", "elastic_client"],
    install_requires=[
        "clickhouse-driver~=0.2.4",
        "elasticsearch~=8.4.1"],
    package_dir={"": "src"},
    packages = setuptools.find_packages(where="src"),
    url = "https://github.com/KazanExpress/ke_ranking_package"
)
