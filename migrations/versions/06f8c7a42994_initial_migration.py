"""Initial migration

Revision ID: 06f8c7a42994
Revises: 
Create Date: 2025-04-06 23:31:50.992517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '06f8c7a42994'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=6), nullable=False),
    sa.Column('method', sa.String(length=10), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=256), nullable=False))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=15),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.drop_column('code_expiration')
        batch_op.drop_column('last_login')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('name')
        batch_op.drop_column('verified')
        batch_op.drop_column('verification_code')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_code', mysql.VARCHAR(length=6), nullable=True))
        batch_op.add_column(sa.Column('verified', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=100), nullable=False))
        batch_op.add_column(sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False))
        batch_op.add_column(sa.Column('last_login', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('code_expiration', mysql.DATETIME(), nullable=True))
        batch_op.alter_column('phone',
               existing_type=sa.String(length=20),
               type_=mysql.VARCHAR(length=15),
               existing_nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=80),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('password')
        batch_op.drop_column('full_name')

    op.drop_table('verifications')
    # ### end Alembic commands ###
