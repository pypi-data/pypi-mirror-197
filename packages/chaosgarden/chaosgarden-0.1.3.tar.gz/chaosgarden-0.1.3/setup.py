import os

import setuptools

own_dir = os.path.abspath(os.path.dirname(__file__))


def version():
    with open(os.path.join(own_dir, 'VERSION')) as file:
        return file.read().strip()


def readme():
    with open(os.path.join(own_dir, 'README.md'), encoding='utf-8') as file:
        return file.read()


def packages():
    return setuptools.find_packages()


def modules():
    return [os.path.basename(os.path.splitext(module)[0]) for module in os.scandir(path = own_dir) if module.is_file() and module.name.endswith('.py')]


def requirements():
    with open(os.path.join(own_dir, 'requirements.txt')) as file:
        for line in file.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            yield line


setuptools.setup(
    # https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#metadata
    name                          = 'chaosgarden',
    version                       = version(),
    url                           = 'https://github.com/gardener/chaos-engineering',
    author                        = 'SAP SE',
    license                       = 'License :: OSI Approved :: Apache Software License', # https://pypi.org/classifiers
    description                   = 'Generic cloud provider zone outage and Kubernetes pod disruption simulations with specific support for https://github.com/gardener',
    long_description              = 'This package provides [Gardener](https://github.com/gardener/gardener)-independent [`chaostoolkit`](https://chaostoolkit.org) modules to simulate *compute* and *network* outages for various cloud providers as well as *pods disruptions* in Kubernetes clusters.\n\n' +
                                    '![Open Source](https://github.com/gardener/gardener/blob/master/logo/gardener.svg) [Gardener](https://github.com/gardener/gardener) users benefit from an additional module that leverages the generic modules, but hides the configuration differences from the end user (no need to specify cloud provider or cluster credentials, filters, and everything else is retrieved securely and computed automatically).\n\n' +
                                    'Please check out the original repo [README](https://github.com/gardener/chaos-engineering/blob/main/readme.md) for more information.',
    long_description_content_type = 'text/markdown',
    keywords                      = ['chaostoolkit', 'kubernetes', 'gardener'],

    # https://setuptools.pypa.io/en/latest/userguide/declarative_config.html#options
    platforms                     = ['AWS', 'Azure', 'GCP', 'OpenStack', 'vSphere', 'Kubernetes', 'Gardener'],
    install_requires              = list(requirements()),
    python_requires               = '>= 3.9',
    entry_points                  = {},
    packages                      = packages(),
    package_data                  = {},
    py_modules                    = modules(),
    data_files                    = [('chaosgarden/k8s/probe/resources', ['chaosgarden/k8s/probe/resources/templated_resources.yaml'])]
)
