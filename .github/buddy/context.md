# FlexTrading Implementation Context

## Verified Facts
- Python 3.13.12 installed via Homebrew at `/opt/homebrew/bin/python3.13`
- Virtual environment at `.venv` with Python 3.13.12
- All project + test dependencies installed via `uv sync --group test`
- Project uses: FastAPI, SQLAlchemy, Alembic, Pydantic v2, pytest, pytest-asyncio
- Architecture: API layer (snake_case) → BusOrder → Mapper → Volue models (camelCase)

## Design Constraint
- User explicitly stated: "I do not want you to import from maid.market.volue.datamodels.v2.volue_models import StrategyQuantityLimitPairModel. it's not a good design. create a similar object in the api. please respect the api naming convention."
- Solution: Created API-specific `FlexBand` model with snake_case naming; mapper layer handles conversion to camelCase Volue models.

## Infrastructure Dependencies
- PostgreSQL database: Required for test_dao, test_market_limit/integration, test_api tests
- RabbitMQ: Required for test_rabbitmq_clients
- Neither available locally - these test failures are pre-existing infrastructure issues
