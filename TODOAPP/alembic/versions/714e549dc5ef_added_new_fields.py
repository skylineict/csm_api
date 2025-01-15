"""added new fields

Revision ID: 714e549dc5ef
Revises: 99cc55fa6037
Create Date: 2024-12-09 07:16:42.201248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '714e549dc5ef'
down_revision: Union[str, None] = '99cc55fa6037'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('user_id_2', table_name='otprecords', mysql_length={'user_id': 250})
    op.create_foreign_key(None, 'otprecords', 'user', ['user_id'], ['id'])
    op.add_column('todolist', sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_foreign_key(None, 'todolist', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todolist', type_='foreignkey')
    op.drop_column('todolist', 'created_by')
    op.drop_constraint(None, 'otprecords', type_='foreignkey')
    op.create_index('user_id_2', 'otprecords', ['user_id'], unique=False, mysql_length={'user_id': 250})
    # ### end Alembic commands ###
