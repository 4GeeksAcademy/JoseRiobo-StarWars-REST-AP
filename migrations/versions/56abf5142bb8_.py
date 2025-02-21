"""empty message

Revision ID: 56abf5142bb8
Revises: 2789b3ae62d9
Create Date: 2025-02-21 15:51:47.314396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56abf5142bb8'
down_revision = '2789b3ae62d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['character_id'])

    with op.batch_alter_table('favourite_characters', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('favourite_planets', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['planet_id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('favourite_planets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('favourite_characters', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
