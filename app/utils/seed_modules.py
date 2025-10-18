from app import create_app, db
from app.models import Module

def seed():
    app = create_app()
    app.app_context().push()

    modules = [
        "Password Security",
        "Phishing Awareness",
        "Social Engineering",
        "Two-Factor Authentication",
        "Safe Browsing",
        "Email Security",
        "Software Updates",
        "Wi-Fi Safety",
        "Device Security",
        "Cyberbullying & Reporting"
    ]

    for title in modules:
        mod = Module(title=title, description=f"Learn about {title} best practices.")
        db.session.add(mod)

    db.session.commit()
    print("✅ Inserted modules.")

if __name__ == "__main__":
    seed()
