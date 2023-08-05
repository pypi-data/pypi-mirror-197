from setuptools import setup, find_packages

setup(
    name            ="generic_analysis_scripts",
    version         ='0.0.7',
    description     ='Generic utilities for data analysis',
    long_description='Private package, if you do not know what this is, it is useless for you, keep moving',
    pymodules       = ['plot', 'fitter', 'atr_mgr'],
    package_dir     = {'' : 'src'},
    install_requires= ['sympy', 'mplhep', 'hist', 'pandas', 'tensorflow-cpu==2.11', 'zfit', 'dill', 'awkward']
)

