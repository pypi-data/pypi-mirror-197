from skbuild import setup  # This line replaces 'from setuptools import setup'

# https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mq_sa",
    version="0.0.7",
    description="Message queue for Interprocess communication",
    author='Yakov Wildfluss <yakov@smashingalpha.com>',
    license="MIT",
    packages=['mq_sa'],
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SmashingAlpha/message-queue'
)
