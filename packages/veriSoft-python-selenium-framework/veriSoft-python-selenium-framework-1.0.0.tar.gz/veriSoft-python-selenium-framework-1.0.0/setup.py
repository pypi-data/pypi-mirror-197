from setuptools import setup, find_packages

setup(
    name='veriSoft-python-selenium-framework',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'pytest',
        'webdriver_manager',
        'jproperties',
        'PyYAML',
        'numpy',
        'pyautogui',
        'opencv-python',
        'auto-metamask',
        'requests'
    ],
    author='Efrat Cohen',
    author_email='efrat.cohen@verisoft.co',
    description='A package of Selenium Python Framework',
    url='https://gitlab.com/DcentraLab/automation-qa-infra',
)
