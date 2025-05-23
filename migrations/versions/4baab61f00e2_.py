"""empty message

Revision ID: 4baab61f00e2
Revises: 554b4f515f0a
Create Date: 2025-04-30 18:05:08.861654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4baab61f00e2'
down_revision = '554b4f515f0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('photo')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo', sa.VARCHAR(length=255), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
