"""extended folder path max lenfth

Revision ID: 388a5b02701c
Revises: b4624263be3b
Create Date: 2024-07-13 13:47:41.009684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '388a5b02701c'
down_revision = 'b4624263be3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folder', schema=None) as batch_op:
        batch_op.alter_column('path',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folder', schema=None) as batch_op:
        batch_op.alter_column('path',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    # ### end Alembic commands ###
