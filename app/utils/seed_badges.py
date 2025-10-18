from app import create_app, db
from app.models import Badge

app = create_app()
app.app_context().push()

badges = [
    {"name": "Cyber Rookie", "description": "Score 50%+ in a quiz", "criteria": "score>=50"},
    {"name": "Cyber Pro", "description": "Score 80%+ in a quiz", "criteria": "score>=80"}
]

for b in badges:
    badge = Badge(**b)
    db.session.add(badge)

db.session.commit()
print("✅ Badges inserted.")
