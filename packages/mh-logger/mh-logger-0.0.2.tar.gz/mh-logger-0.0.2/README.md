# Logger

## Ideation
This Logging Manager is to be used as a standardized system and structure to enable logging on different product offerings. We intend the logs to not only enable debugging platform exceptions, but to provide visibility, analytics and reporting on the health, engagement and usage of our products and systems.



## Steps to Create and Upload Package
### 1. Create Token (First Time Only)
- Goto `pypi.org` and create your login
- Go to api-tokens and create your API token to securely upload your packages.
- Copy and save your token in a safe place on your disk.

### 2. Install Dependencies
Install following
```
py -m pip install --upgrade build 
py -m pip install --upgrade twine
```

### 3. Build Package

execute following command
```
py -m build
```

Once the process above is completed, a new directory is generated called `dist/` with two files in it. The `.tag.tz` file is the source archive and the `.whl*` file is the built archive. These files represent the distribution archives of our Python package which will be uploaded to the Python Package Index and installed by pip in the following sections.

### 4. Check and Upload Package to PyPi Server 
`twine` is a python package that goes through a checklist of items to see if your distribution/package is compatible for publishing.

Check if your distribution is all set to go .

execute following command to check distributions before upload
```
twine check dist/*
```

execute following command to upload latest distribution
```
twine upload --skip-existing --repository-url https://upload.pypi.org/legacy/ dist/*
```