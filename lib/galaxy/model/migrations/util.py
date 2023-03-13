import logging
from typing import List

from alembic import (
    context,
    op,
)
from sqlalchemy import inspect

log = logging.getLogger(__name__)


def drop_column(table_name, column_name):
    if context.is_offline_mode():
        return _handle_offline_mode(f"drop_column({table_name}, {column_name})", None)

    with op.batch_alter_table(table_name) as batch_op:
        batch_op.drop_column(column_name)


def add_unique_constraint(index_name: str, table_name: str, columns: List[str]):
    if _is_sqlite():
        with op.batch_alter_table(table_name) as batch_op:
            batch_op.create_unique_constraint(index_name, columns)
    else:
        op.create_unique_constraint(index_name, table_name, columns)


def drop_unique_constraint(index_name: str, table_name: str):
    if _is_sqlite():
        with op.batch_alter_table(table_name) as batch_op:
            batch_op.drop_constraint(index_name)
    else:
        op.drop_constraint(index_name, table_name)


def column_exists(table_name, column_name):
    if context.is_offline_mode():
        return _handle_offline_mode(f"column_exists({table_name}, {column_name})", False)

    bind = op.get_context().bind
    insp = inspect(bind)
    columns = insp.get_columns(table_name)
    return any(c["name"] == column_name for c in columns)


def _handle_offline_mode(code, return_value):
    msg = (
        "This script is being executed in offline mode and cannot connect to the database. "
        f"Therefore, `{code}` returns `{return_value}` by default."
    )
    log.info(msg)
    return return_value


def _is_sqlite() -> bool:
    bind = op.get_context().bind
    return bool(bind and bind.engine.name == "sqlite")
