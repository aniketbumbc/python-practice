from auth_db import Base,engine
import auth_models


Base.metadata.create_all(bind=engine)