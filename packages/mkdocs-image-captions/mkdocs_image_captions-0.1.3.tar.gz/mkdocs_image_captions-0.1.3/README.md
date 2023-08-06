# MkDocs ImageCaptions Plugin

Plugin for [MkDocs](https://www.mkdocs.org) that converts markdown encoded images to HTML <figure> element with captions.

## Example

Input MD Template:

```
![Informative image caption](/docs/assets/images/image.png)
```

Output:

```html
<figure class="figure-image">
  <img src="/docs/assets/images/image.png" alt="Informative image caption">
  <figcaption>Informative image caption</figcaption>
</figure>
```

## Plugin installation


To enable the plugin, add the following line to your `mkdocs` config file `mkdocs.yml`:

```yaml
plugins:
    - mkdocs-image-captions
```

## Local development

### Dependencies installation

The package requires Python >= 3.8 and Poetry >= 1.4.0.  

### Project installation

Install required packages 

```
poetry install
```

Now you can activate Poetry and make your changes:

```
poetry shell
```

### Run tests

Activate virtualenv:

```
poetry shell
```

Run tests:

```
python tests/test_plugin.py
```

### Update package on PyPI with poetry

Build new package version

```
poetry build
```

Push to PyPI

```
poetry build
```

**Note:** to push packages into PyPI you need to provide auth token:

```
export POETRY_PYPI_TOKEN_PYPI=<your token>
```
