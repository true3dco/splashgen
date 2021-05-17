SplashGen Prototype

Needs python3

```
# Install deps
pip install jinja query_string urlexpander
# Build the ZenWeb site
python -m splashgen.cli zenweb.py
# Serve it
python -m http.server --directory build
```
