from setuptools import setup

setup(
    name='ShapeChecker',
    version='0.2.0',
    description='ShapeChecker assist you when doing tensors manipulation',
    url='https://github.com/Etienne-Meunier/ShapeChecker',
    author='Etienne Meunier',
    author_email='etiennemeunier@live.fr',
    license='BSD 2-clause',
    packages=['ShapeChecker'],
    install_requires=['einops',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
