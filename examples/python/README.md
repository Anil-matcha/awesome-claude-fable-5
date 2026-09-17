# Python examples

Install the official SDK and provide an API key for the live examples:

```bash
python -m pip install -r examples/python/requirements.txt
export TYPESAFE_API_KEY="your-key"
python examples/python/quickstart.py
```

`decision_policies.py` has no TypeSafe dependency. Its confidence gates,
weighted score, and RAG filter are covered by the offline test suite:

```bash
python -m unittest discover -s tests -v
```

`workflows.py` is intended to be imported by an application. Run it from a
package or set `PYTHONPATH=examples/python` when experimenting in a shell.
