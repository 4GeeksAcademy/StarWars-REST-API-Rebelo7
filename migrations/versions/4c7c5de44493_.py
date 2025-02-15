"""empty message

Revision ID: 4c7c5de44493
Revises: 86d2a99f2625
Create Date: 2024-01-03 21:19:30.388262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c7c5de44493'
down_revision = '86d2a99f2625'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(length=120), nullable=False),
    sa.Column('Height', sa.String(length=80), nullable=False),
    sa.Column('Mass', sa.String(length=80), nullable=False),
    sa.Column('Hair_Color', sa.String(length=80), nullable=False),
    sa.Column('Skin_Color', sa.String(length=80), nullable=False),
    sa.Column('Eye_Color', sa.String(length=80), nullable=False),
    sa.Column('Birth_Year', sa.String(length=80), nullable=False),
    sa.Column('Gender', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    # ### end Alembic commands ###
