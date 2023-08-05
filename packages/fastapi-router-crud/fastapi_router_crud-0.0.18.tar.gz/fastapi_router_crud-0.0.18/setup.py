from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="fastapi_router_crud",
    version="0.0.18",
    description="FastAPI API router that generates model based routes(CRUD operations) automatically.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milanchanstveni/fastapi-crud-router",
    author="Milan Pantelic",
    author_email="milanpantelic95@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Framework :: FastAPI",
        "Topic :: Database"
    ],
    install_requires=["fastapi", "tortoise-orm[all]"],
    extras_require={
        "dev": ["pytest", "twine"],
    },
    python_requires=">=3.10",
)
