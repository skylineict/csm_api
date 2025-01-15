"""added fir

Revision ID: 17b41c76e3cc
Revises: 84798ddd307f
Create Date: 2024-12-16 22:05:11.244859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '17b41c76e3cc'
down_revision: Union[str, None] = '84798ddd307f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_id_2', table_name='otprecords', mysql_length={'user_id': 250})
    op.create_foreign_key(None, 'otprecords', 'user', ['user_id'], ['id'])
    op.drop_index('created_by_2', table_name='todolist', mysql_length={'created_by': 250})
    op.create_foreign_key(None, 'todolist', 'user', ['created_by'], ['id'])
    op.alter_column('user', 'first_name',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_name',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
    op.alter_column('user', 'first_name',
               existing_type=mysql.VARCHAR(length=200),
               nullable=False)
    op.drop_constraint(None, 'todolist', type_='foreignkey')
    op.create_index('created_by_2', 'todolist', ['created_by'], unique=False, mysql_length={'created_by': 250})
    op.drop_constraint(None, 'otprecords', type_='foreignkey')
    op.create_index('user_id_2', 'otprecords', ['user_id'], unique=False, mysql_length={'user_id': 250})
    # ### end Alembic commands ###
