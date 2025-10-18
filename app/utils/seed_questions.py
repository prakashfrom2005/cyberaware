from app import create_app, db
from app.models import Question

app = create_app()
app.app_context().push()

sample_questions = [
    {
        "module_id": 1,
        "question_text": "What is the most secure way to store passwords?",
        "option_a": "Plaintext",
        "option_b": "Encrypted with reversible encryption",
        "option_c": "Hashed with salt",
        "option_d": "Written on paper",
        "correct_option": "C"
    },
    {
        "module_id": 1,
        "question_text": "What does a strong password include?",
        "option_a": "Only lowercase letters",
        "option_b": "Your name and birthdate",
        "option_c": "At least 12 characters with mix of types",
        "option_d": "Repeated numbers",
        "correct_option": "C"
    },
    {
        "module_id": 2,
        "question_text": "Which of the following is a sign of a phishing email?",
        "option_a": "It comes from your known contacts",
        "option_b": "It asks for urgent password reset with link",
        "option_c": "It greets you by full name",
        "option_d": "It has company branding",
        "correct_option": "B"
    }
]

for q in sample_questions:
    question = Question(**q)
    db.session.add(question)

db.session.commit()
print("✅ Inserted sample quiz questions.")
