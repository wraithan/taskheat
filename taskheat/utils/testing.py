from django.utils.unittest import TestCase
import mock


cursor_wrapper = mock.Mock()
cursor_wrapper.side_effect = RuntimeError("No touching the database!")


@mock.patch("django.db.backends.util.CursorWrapper", cursor_wrapper)
class NoDBTestCase(TestCase):
    """Will blow up if you database."""
