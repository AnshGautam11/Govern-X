import os
import tempfile

# Must run before the app or database modules are imported.
_tmp_dir = tempfile.mkdtemp(prefix="governx_test_")
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp_dir, "test.db").replace("\\", "/")

from database.db import Base, engine  # noqa: E402
import database.models  # noqa: E402,F401

Base.metadata.create_all(bind=engine)
