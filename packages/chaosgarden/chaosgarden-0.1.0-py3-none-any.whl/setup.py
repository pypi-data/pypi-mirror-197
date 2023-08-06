import os

import setuptools

own_dir = os.path.abspath(os.path.dirname(__file__))


def version():
    with open(os.path.join(own_dir, 'VERSION')) as file:
        return file.read().strip()


def modules():
    return [os.path.basename(os.path.splitext(module)[0]) for module in os.scandir(path = own_dir) if module.is_file() and module.name.endswith('.py')]


def packages():
    return setuptools.find_packages()


def requirements():
    with open(os.path.join(own_dir, 'requirements.txt')) as file:
        for line in file.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            yield line


setuptools.setup(
    name='chaosgarden',
    version=version(),
    description='Chaos engineering tools for Gardener-managed clusters',
    python_requires='>=3.9',
    py_modules=modules(),
    packages=packages(),
    package_data={},
    data_files=[('chaosgarden/k8s/probe/resources', ['chaosgarden/k8s/probe/resources/templated_resources.yaml'])],
    install_requires=list(requirements()),
    entry_points={},
    license='License :: OSI Approved :: Apache Software License' # https://pypi.org/classifiers
)
