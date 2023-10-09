# ------------------ Database related functions ------------------
import os

project_root = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(project_root, 'database_SkinAI.db')
print(f"Database path: {DATABASE}")
