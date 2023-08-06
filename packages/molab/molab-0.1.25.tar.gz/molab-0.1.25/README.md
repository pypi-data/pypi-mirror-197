# molab

This module is for use in conjuction with the Terraform deployments of the Morpheus training labs.

# Rebuild and install locally for testing
```
python3 setup.py sdist bdist_wheel
python3 -m pip install ./
```

# Upload
```
python3 -m twine check dist/*
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload dist/*
```