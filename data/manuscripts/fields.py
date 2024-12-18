import data.db_connect as dbc

TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
REFEREES = 'referees'


FIELDS_COLLECTION = 'fields'
client = dbc.connect_db()

def get_flds() -> dict:
    return dbc.read_dict(FIELDS_COLLECTION, 'field_name')

def get_fld_names() -> list:
    return list(get_flds().keys())

def get_disp_name(fld_nm: str) -> str:
    field = dbc.get_one(FIELDS_COLLECTION, {'field_name': fld_nm})
    if field:
        return field.get('disp_name', 'Unknown Field')
    return 'Unknown Field'

def is_field_valid(field_name: str) -> bool:
    return dbc.get_one(FIELDS_COLLECTION, {'field_name': field_name}) is not None

def add_field(field_name: str, display_name: str) -> bool:
    if is_field_valid(field_name):
        return False
    dbc.create(FIELDS_COLLECTION, {'field_name': field_name, 'disp_name': display_name})
    return True

def update_field(field_name: str, new_display_name: str) -> bool:
    if not is_field_valid(field_name):
        return False
    dbc.update_doc(FIELDS_COLLECTION, {'field_name': field_name}, {'disp_name': new_display_name})
    return True

def del_field(field_name: str) -> bool:
    return dbc.del_one(FIELDS_COLLECTION, {'field_name': field_name}) > 0

def main():
    print(f'Fields: {get_flds()}')
    print(f'Field names: {get_fld_names()}')
    print(f'Display name for "title": {get_disp_name("title")}')
    print(f'Is "title" valid? {is_field_valid("title")}')
    print(f'Adding new field: {add_field("new_field", "New Field")}')
    print(f'Fields after adding: {get_flds()}')
    print(f'Updating "title" display name: {update_field("title", "Updated Title")}')
    print(f'Fields after updating: {get_flds()}')
    print(f'Removing "new_field": {del_field("new_field")}')
    print(f'Fields after deleting: {get_flds()}')

if __name__ == '__main__':
    main()
