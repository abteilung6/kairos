# Usage

Export environment variables.

```
export AWS_ACCESS_KEY_ID="changeme"
export AWS_SECRET_ACCESS_KEY="changeme"
export DEFAULT_AWS_REGION="changeme"
export BUCKET_NAME="changeme"
export SQLALCHEMY_DATABASE_URL="sqlite:///./sqlite_changeme.db"
```

Run demo

```
python demo.py
```

Run API server
```
uvicorn main:app --reload
```

# Development


## Lint and formatting

Run `ruff check .` in order to lint.

Run `ruff check . --fix` in order to fix lint errors.

See [Ruff docs](https://docs.astral.sh/ruff/)

## Testing

Run tests with `pytest`

See

- [Pytest docs](https://docs.pytest.org/en/7.4.x/)
