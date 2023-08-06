import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.3'
DESCRIPTION = 'a reinforce learning library, support both win and linux'
LONG_DESCRIPTION = 'Life is a library for reinforce learning, support both win and linux, including:' \
                   'Sarsa,multi-Sarsa,Q-Learning,Dyna-Q,DQN,Double-DQN,Dueling-DQN,REINFORCE' \
                   ',Actor-Critic,PPO,DDPG,SAC,BC,GAIL,CQL'

# Setting up
setup(
    name="rllife",
    version=VERSION,
    author="Yuhang Zhou",
    author_email="neutjuzyh@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'pytorch', 'reinforce learning', 'deep learning', 'DQN', 'QLearning', 'DDPG', 'algorithm'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
