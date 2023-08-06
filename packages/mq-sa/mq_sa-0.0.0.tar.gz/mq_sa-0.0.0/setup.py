from skbuild import setup  # This line replaces 'from setuptools import setup'
setup(
    name="mq_sa",
    version="0.0.0",
    description="Message queue for Interprocess communication",
    author='Yakov Wildfluss <yakov@smashingalpha.com>',
    license="MIT",
    packages=['mq_sa'],
    python_requires=">=3.7",
)
