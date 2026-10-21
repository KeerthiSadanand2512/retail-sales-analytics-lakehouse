# Shared transformation source

The first implementation keeps shared PySpark functions in `../notebooks/00_transformations.py` so the beginner workflow can use relative `%run` without package installation. Both execution and synthetic checks use these same functions. A Python package can be introduced later when the notebook workflow is validated.
