# flight-management



## Requirements

`pip install -r requirements.txt`

## Usage

Run:

`python3 main.py`

## Setting descriptions
As these tables use foreign keys, you can choose what behaviour to have when you try to delete a record. The default is: RESTRICT

- **CASCADE**: if a record is deleted if it's still in use in another table, the records that use it will also get deleted.
- **SET NULL**: a record can be delete if it's still in use in another table but the reference will be set to null.
- **RESTRICT**: a record can't be deleted if it's still in use in another table.

