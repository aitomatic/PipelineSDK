import setuptools

setuptools.setup(
    name="arimo_pipeline_sdk",
    version="0.0.1",
    author="An Phan",
    author_email="anphan@arimo.com",
    description="Arimo Pipeline SDK",
    url="https://github.com/adatao/PipelineSDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': 'pipeline=arimo.pipeline'
    },
    python_requires='>=3.6',
)
