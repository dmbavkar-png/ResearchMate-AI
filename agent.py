import requests

from memory import Memory
from tools.email_tool import MockEmailTool


class PersonalAssistant:

    def __init__(self):

        self.memory = Memory()

        # Mock email system
        self.email_tool = MockEmailTool()

        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"

    # --------------------------------------------------
    # EMAIL COMMAND HANDLER
    # --------------------------------------------------

    def handle_email_command(self, user_input):

        text = user_input.lower().strip()

        # ----------------------------------------------
        # SHOW EMAILS
        # ----------------------------------------------

        if (
            "show my emails" in text
            or "list my emails" in text
            or "show emails" in text
        ):

            emails = self.email_tool.list_emails()

            print("\n========== EMAILS ==========")

            for email in emails:
                print(
                    f"{email['id']}. "
                    f"{email['from']} | "
                    f"{email['subject']}"
                )

            print("============================\n")

            return True

        # ----------------------------------------------
        # FIND EMAILS
        # ----------------------------------------------

        if "find emails about" in text:

            keyword = text.split("find emails about", 1)[1].strip()

            emails = self.email_tool.search_emails(keyword)

            print(f"\n========== SEARCH: {keyword} ==========")

            if not emails:
                print("No matching emails found.")

            else:

                for email in emails:
                    print(
                        f"{email['id']}. "
                        f"{email['from']} | "
                        f"{email['subject']}"
                    )

            print("========================================\n")

            return True

        # ----------------------------------------------
        # READ EMAIL
        # ----------------------------------------------

        if text.startswith("read email"):

            parts = text.split()

            try:
                email_id = int(parts[-1])
            except ValueError:
                print("Please provide an email number.")
                return True

            email = self.email_tool.read_email(email_id)

            if email is None:

                print("Email not found.")

            else:

                print("\n========== EMAIL ==========")
                print(f"From: {email['from']}")
                print(f"To: {email['to']}")
                print(f"Subject: {email['subject']}")
                print("\n" + email["body"])
                print("===========================\n")

            return True

        # ----------------------------------------------
        # DRAFT EMAIL
        # ----------------------------------------------

        if "draft an email to dr. sharma" in text:

            draft = self.email_tool.draft_email(
                to="dr.sharma@university.edu",
                subject="Research Meeting",
                body=(
                    "Dear Dr. Sharma,\n\n"
                    "I would like to discuss our research work "
                    "and schedule a meeting at a convenient time.\n\n"
                    "Please let me know your availability.\n\n"
                    "Regards,\n"
                    "Dr. Dnyaneshwar Bavkar"
                )
            )

            print("\n========== EMAIL DRAFT ==========")
            print(f"To: {draft['to']}")
            print(f"Subject: {draft['subject']}")
            print("\n" + draft["body"])
            print("=================================\n")

            return True

        # ----------------------------------------------
        # SEND EMAIL
        # ----------------------------------------------

        if text == "send this email":

            result = self.email_tool.send_email()

            print(result)

            return True

        return False

    # --------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------

    def ask_ollama(self, prompt):

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.ollama_url,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    # --------------------------------------------------
    # MAIN RUN METHOD
    # --------------------------------------------------

    def run(self, user_input):

        # First check whether this is an email command
        handled = self.handle_email_command(user_input)

        if handled:
            return

        # Otherwise use normal AI assistant
        context = self.memory.get_context()

        prompt = f"""
You are PersonalAI, a helpful personal assistant.

Previous conversation:
{context}

User:
{user_input}

Answer naturally and helpfully.
"""

        answer = self.ask_ollama(prompt)

        print("\nPersonalAI:", answer)

        # Save conversation
        self.memory.save_message(
            "user",
            user_input
        )

        self.memory.save_message(
            "assistant",
            answer
        )