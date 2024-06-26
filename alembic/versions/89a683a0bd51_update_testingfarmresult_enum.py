"""Update TestingFarmResult enum

Revision ID: 89a683a0bd51
Revises: 2ad985cecd79
Create Date: 2024-04-23 09:18:17.039681

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "89a683a0bd51"
down_revision = "2ad985cecd79"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # 'cancel-requested' is missing from 'testingfarmresult'
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE testingfarmresult ADD VALUE 'cancel-requested'")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
