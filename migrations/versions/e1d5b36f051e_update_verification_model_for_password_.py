"""Update Verification model for password reset

Revision ID: e1d5b36f051e
Revises: 0ed7caca83f0
Create Date: 2025-04-15 14:11:25.496440

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e1d5b36f051e'
down_revision = '0ed7caca83f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('verifications', schema=None) as batch_op:
        batch_op.alter_column('method',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('verifications', schema=None) as batch_op:
        batch_op.alter_column('method',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=False)

    # ### end Alembic commands ###
