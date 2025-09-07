# alembic/env.py
from __future__ import annotations
from logging.config import fileConfig
import sys
import pathlib
from alembic import context
from sqlalchemy import engine_from_config, pool

# Add project root to sys.path
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.core.settings import settings
from app.database import Base
# IMPORTANT: import models so tables & relationships are registered
from app.models import user_model, note_model  # noqa: F401

config = context.config
fileConfig(config.config_file_name)

# Inject DB URL from settings (so we don’t hardcode it in alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
