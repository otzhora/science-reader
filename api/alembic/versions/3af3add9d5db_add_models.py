"""Add models

Revision ID: 3af3add9d5db
Revises: 88aaf2151eab
Create Date: 2021-08-20 00:22:07.555055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3af3add9d5db'
down_revision = '88aaf2151eab'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('moderated', sa.Boolean(), nullable=True),
    sa.Column('premium', sa.Boolean(), nullable=True),
    sa.Column('subsection_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subsection_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=False)

    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('responses_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['responses_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)

    op.create_table('moderators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moderators_id'), 'moderators', ['id'], unique=False)

    op.create_table('papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2048), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_papers_id'), 'papers', ['id'], unique=False)

    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('paper_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_papers_id'), table_name='papers')
    op.drop_table('papers')
    op.drop_index(op.f('ix_moderators_id'), table_name='moderators')
    op.drop_table('moderators')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_table('sections')
