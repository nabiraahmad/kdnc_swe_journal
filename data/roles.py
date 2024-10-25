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


def main():
    print(get_roles())


if __name__ == '__main__':
    main()
