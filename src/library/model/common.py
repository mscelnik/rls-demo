""" Common SQL database components.
"""

from sqlalchemy.types import TypeDecorator, CHAR


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, for other systems uses CHAR(32), storing as
    stringified hex values.

    Reference:
        - https://docs.sqlalchemy.org/en/13/core/custom_types.html#backend-agnostic-guid-type
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        from sqlalchemy.types import CHAR
        from sqlalchemy.dialects.postgresql import UUID
        from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        elif dialect.name == 'mssql':
            return dialect.type_descriptor(UNIQUEIDENTIFIER())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        import uuid
        if value is None:
            return value
        elif dialect.name in ('postgresql', 'mssql'):
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        import uuid
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
