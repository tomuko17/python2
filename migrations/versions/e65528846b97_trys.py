"""'trys'

Revision ID: e65528846b97
Revises: 4235ad1c57f4
Create Date: 2022-02-26 12:43:56.248906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e65528846b97'
down_revision = '4235ad1c57f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('masina',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gamintojas', sa.String(length=50), nullable=False),
    sa.Column('modelis', sa.String(length=50), nullable=True),
    sa.Column('metai', sa.String(length=8), nullable=True),
    sa.Column('variklis', sa.String(length=50), nullable=True),
    sa.Column('valst_nr', sa.String(length=8), nullable=True),
    sa.Column('reg_nr', sa.String(length=30), nullable=False),
    sa.Column('vartotojas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vartotojas_id'], ['vartotojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('irasas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Sukurta', sa.DateTime(), nullable=True),
    sa.Column('statusas', sa.String(length=50), nullable=False),
    sa.Column('problema', sa.String(length=200), nullable=False),
    sa.Column('Suma', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('masina_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['masina_id'], ['masina.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('masinos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('masinos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('gamintojas', sa.VARCHAR(length=50), nullable=False),
    sa.Column('modelis', sa.VARCHAR(length=50), nullable=True),
    sa.Column('metai', sa.VARCHAR(length=8), nullable=True),
    sa.Column('variklis', sa.VARCHAR(length=50), nullable=True),
    sa.Column('valst_nr', sa.VARCHAR(length=8), nullable=True),
    sa.Column('reg_nr', sa.VARCHAR(length=30), nullable=False),
    sa.Column('vartotojas_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['vartotojas_id'], ['vartotojas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('irasas')
    op.drop_table('masina')
    # ### end Alembic commands ###
