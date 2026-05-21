from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="sppg_management",
    version="1.0.0",
    description="SPPG / MBG Operations Management System for ERPNext",
    author="SPPG Dev Team",
    author_email="dev@sppgmanagement.id",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
