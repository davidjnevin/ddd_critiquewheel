import sqlalchemy


def insert_member(session, **kwargs):
    stmt = sqlalchemy.text(
        """
        INSERT INTO members (id, username, email, password)
        VALUES (:id, :username, :email, :password)
        """
    )
    params = kwargs
    session.execute(stmt, params)


def get_member_by_id(session, member_id):
    stmt = sqlalchemy.text(
        """
        SELECT id, username, email, password
        FROM members
        WHERE id = :id
        """
    )
    params = {
        "id": member_id,
    }
    result = session.execute(stmt, params)
    row = result.fetchone()
    if row:
        return row._mapping
    else:
        return None
