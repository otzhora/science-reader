"""Rename table and add many2many

Revision ID: 49bba1d21269
Revises: 3af3add9d5db
Create Date: 2021-08-22 18:33:05.292659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49bba1d21269'
down_revision = '3af3add9d5db'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2048), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_id'), 'articles', ['id'], unique=False)
    op.create_table('articleTag',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    op.add_column('tags', sa.Column('article_id', sa.Integer(), nullable=True))
    op.drop_constraint('tags_paper_id_fkey', 'tags', type_='foreignkey')
    op.create_foreign_key(None, 'tags', 'articles', ['article_id'], ['id'])
    op.drop_column('tags', 'paper_id')
    op.drop_index('ix_papers_id', table_name='papers')
    op.drop_table('papers')


def downgrade():
    op.create_table('papers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('content', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], name='papers_section_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='papers_pkey')
    )
    op.add_column('tags', sa.Column('paper_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tags', type_='foreignkey')
    op.create_foreign_key('tags_paper_id_fkey', 'tags', 'papers', ['paper_id'], ['id'])
    op.drop_column('tags', 'article_id')
    op.create_index('ix_papers_id', 'papers', ['id'], unique=False)
    op.drop_table('articleTag')
    op.drop_index(op.f('ix_articles_id'), table_name='articles')
    op.drop_table('articles')
