from auth.auth_db import Base,engine
from auth import auth_models


Base.metadata.create_all(bind=engine)