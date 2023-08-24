# Throwaway test file for testing ORM functionality

import pytest
from critique_wheel.domain.models.work import Work

@pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
def test_create_and_retrieve_work(session, valid_work):
    # Arrange
    new_work = valid_work

    # Act
    session.add(new_work)
    session.commit()
    retrieved_work = session.query(Work).filter_by(title="Test Title").one()

    # Assert
    assert retrieved_work.id == new_work.id
    assert retrieved_work.title == "Test Title"
    assert retrieved_work.content == "Test content"


