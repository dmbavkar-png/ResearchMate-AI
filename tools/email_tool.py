# tools/email_tool.py

class MockEmailTool:

    def __init__(self):
        self.emails = [
            {
                "id": 1,
                "from": "research@university.edu",
                "to": "dnyaneshwar@example.com",
                "subject": "Research Collaboration Meeting",
                "body": "Dear Professor, let us discuss the upcoming research collaboration meeting."
            },
            {
                "id": 2,
                "from": "dr.sharma@university.edu",
                "to": "dnyaneshwar@example.com",
                "subject": "Research Meeting",
                "body": "Dear Professor Bavkar, can we schedule a meeting to discuss our research work?"
            },
            {
                "id": 3,
                "from": "conference@example.org",
                "to": "dnyaneshwar@example.com",
                "subject": "Conference Paper Submission",
                "body": "Your paper submission deadline is approaching."
            }
        ]

        self.draft = None

    def list_emails(self):
        return self.emails

    def search_emails(self, keyword):
        keyword = keyword.lower()

        results = []

        for email in self.emails:
            text = (
                email["subject"]
                + " "
                + email["body"]
                + " "
                + email["from"]
            ).lower()

            if keyword in text:
                results.append(email)

        return results

    def read_email(self, email_id):
        for email in self.emails:
            if email["id"] == email_id:
                return email

        return None

    def draft_email(self, to, subject, body):

        self.draft = {
            "to": to,
            "subject": subject,
            "body": body
        }

        return self.draft

    def send_email(self):

        if not self.draft:
            return "There is no email draft to send."

        print("\n========== EMAIL APPROVAL ==========")
        print(f"To: {self.draft['to']}")
        print(f"Subject: {self.draft['subject']}")
        print("\n" + self.draft["body"])
        print("====================================")

        approval = input("\nSend this email? (yes/no): ")

        if approval.lower() == "yes":
            print("\n[MOCK EMAIL] Email sent successfully.")
            return "Email sent successfully."

        print("\n[MOCK EMAIL] Email was NOT sent.")
        return "Email sending cancelled."