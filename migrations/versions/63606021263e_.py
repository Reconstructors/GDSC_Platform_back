"""empty message

Revision ID: 63606021263e
Revises: 
Create Date: 2024-03-06 22:07:21.713168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63606021263e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('start', sa.Date(), nullable=True),
    sa.Column('end', sa.Date(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('contact_info', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('photo_ids', sa.JSON(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('modify_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_project'))
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
    op.create_index(op.f('ix_project_title'), 'project', ['title'], unique=False)
    op.create_table('study',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('contact_info', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('photo_ids', sa.JSON(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('modify_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_study'))
    )
    op.create_index(op.f('ix_study_id'), 'study', ['id'], unique=False)
    op.create_index(op.f('ix_study_title'), 'study', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('cohort', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('links', sa.JSON(), nullable=True),
    sa.Column('skills', sa.JSON(), nullable=True),
    sa.Column('interests', sa.JSON(), nullable=True),
    sa.Column('project_interest', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_index(op.f('ix_user_cohort'), 'user', ['cohort'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_position'), 'user', ['position'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('timeline',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_timeline_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_timeline'))
    )
    op.create_index(op.f('ix_timeline_id'), 'timeline', ['id'], unique=False)
    op.create_index(op.f('ix_timeline_title'), 'timeline', ['title'], unique=False)
    op.create_table('user_project_match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('is_leader', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], name=op.f('fk_user_project_match_project_id_project')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_project_match_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_project_match'))
    )
    op.create_index(op.f('ix_user_project_match_id'), 'user_project_match', ['id'], unique=False)
    op.create_table('user_study_match',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('study_id', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('is_leader', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['study_id'], ['study.id'], name=op.f('fk_user_study_match_study_id_study')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_study_match_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_study_match'))
    )
    op.create_index(op.f('ix_user_study_match_id'), 'user_study_match', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_study_match_id'), table_name='user_study_match')
    op.drop_table('user_study_match')
    op.drop_index(op.f('ix_user_project_match_id'), table_name='user_project_match')
    op.drop_table('user_project_match')
    op.drop_index(op.f('ix_timeline_title'), table_name='timeline')
    op.drop_index(op.f('ix_timeline_id'), table_name='timeline')
    op.drop_table('timeline')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_position'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_cohort'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_study_title'), table_name='study')
    op.drop_index(op.f('ix_study_id'), table_name='study')
    op.drop_table('study')
    op.drop_index(op.f('ix_project_title'), table_name='project')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')
    # ### end Alembic commands ###
