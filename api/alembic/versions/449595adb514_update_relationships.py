"""update relationships

Revision ID: 449595adb514
Revises: 1818c843b51b
Create Date: 2021-08-22 22:13:42.539010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '449595adb514'
down_revision = '1818c843b51b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('response_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'comments', ['response_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'response_id')
    # ### end Alembic commands ###