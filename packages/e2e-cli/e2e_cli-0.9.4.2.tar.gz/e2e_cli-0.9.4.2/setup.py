import subprocess
try:
  from setuptools import setup
except ImportError:
  subprocess.call["pip","install","setuptools"]
  from setuptools import setup

setup(
    name='e2e_cli',
    version='0.9.4.2',
    description="This a E2E CLI tool for myAccount",
    author="Sajal&Aman@E2E_Networks_Ltd",
    packages=["e2e_cli", "e2e_cli.config", "e2e_cli.node", "e2e_cli.node.node_crud", "e2e_cli.node.node_actions", "e2e_cli.core", "e2e_cli.loadbalancer", "e2e_cli.bucket_store", "e2e_cli.dbaas"],
    install_requires=['prettytable', 'requests', 'setuptools'],

    entry_points={
        'console_scripts': [
            'e2e_cli=e2e_cli.main:run_main_class'
        ]
    },
)

from  install_man import runcls
runcls().run()