'''Sets up required dependencies to run the bot'''


from setuptools import setup, find_packages

setup(
    name="beam-client-python",
    version="0.1.0",
    url="https://github.com/WatchBeam/beam-client-python",
    author="Connor Peet, 2Cubed (@2CubedTech)",
    author_email="connor@connorpeet.com",
    description="Simple chat bot framework for Beam.",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests", "tornado"]
)
