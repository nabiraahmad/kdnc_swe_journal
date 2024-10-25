"""
This module manages the roles a person can have for the journal
"""

ROLES = {
    'AU': 'Author',
    'ED': 'Editor',
    'RE': 'Referee',
}


def get_roles():
    return ROLES


