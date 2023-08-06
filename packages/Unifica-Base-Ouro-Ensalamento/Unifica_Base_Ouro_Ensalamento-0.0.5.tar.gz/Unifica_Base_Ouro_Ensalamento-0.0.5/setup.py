from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='Unifica_Base_Ouro_Ensalamento',
    version='0.0.5',
    author='Matheus Henrique Rosa',
    author_email='m.rosa1@pucpr.br',
    packages=['Unifica_base_ouro_ensalamento', 'API_magister'],
    description='Unifica bases e envia via API para o magister',
    long_description=readme,
    license='MIT',
    keywords='Unifica bases e envia via API para o magister',

)
