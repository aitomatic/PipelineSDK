import setuptools

setuptools.setup(
    name="pipeline_sdk",
    version="0.0.1",
    author="An Phan",
    author_email="anphan@aitomatic.com",
    description="Arimo Pipeline SDK",
    url="https://github.com/adatao/PipelineSDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': 'pipeline=sdk.pipeline'
    },
    python_requires='>=3.6',
)
