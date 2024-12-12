
TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
REFEREES = 'referees'

TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> str:
    fld = FIELDS.get(fld_nm, {})
    return fld.get(DISP_NAME, 'Unknown Field')


def is_field_valid(field_name: str) -> bool:
    return field_name in FIELDS


def add_field(field_name: str, display_name: str) -> bool:
    if field_name in FIELDS:
        return False
    FIELDS[field_name] = {DISP_NAME: display_name}
    return True


def update_field(field_name: str, new_display_name: str) -> bool:
    if field_name not in FIELDS:
        return False
    FIELDS[field_name][DISP_NAME] = new_display_name
    return True


def del_field(field_name: str) -> bool:
    if field_name not in FIELDS:
        return False
    del FIELDS[field_name]
    return True


def main():
    print(f'{get_flds()=}')
    print(f'Field names: {get_fld_names()}')
    print(f'Display name for "{TITLE}": {get_disp_name(TITLE)}')
    print(f'Is "{TITLE}" valid? {is_field_valid(TITLE)}')

    # Add a new field
    print(f'Adding new field: {add_field("new_field", "New Field")}')
    print(f'Fields after adding: {get_flds()}')

    # Update a field's display name
    print(f'Updating "{TITLE}" display name: {update_field(TITLE, "Updated Title")}')
    print(f'Fields after updating: {get_flds()}')

    # Delete a field
    print(f'Removing "new_field": {del_field("new_field")}')
    print(f'Fields after deleting: {get_flds()}')


if __name__ == '__main__':
    main()
