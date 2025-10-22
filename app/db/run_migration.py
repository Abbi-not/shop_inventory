from alembic import command
from alembic.config import Config
import os

def run_migrations_sync():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
    alembic_ini_path = os.path.join(base_dir, "alembic.ini")

    if not os.path.exists(alembic_ini_path):
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")

    alembic_cfg = Config(alembic_ini_path)
    print('alemtic cfg', alembic_cfg)
    command.upgrade(alembic_cfg, "head")  # ✅ no await