from tools.gmail_tool import GmailTool


print("Starting Gmail test...")

gmail = GmailTool()

try:
    print("\nAuthenticating with Google...")

    gmail.authenticate()

    print("Authentication successful!")

    print("\nReading latest inbox emails...\n")

    emails = gmail.list_emails(max_results=5)

    if not emails:
        print("No emails found in inbox.")

    else:
        for number, email in enumerate(emails, start=1):

            print(f"{number}. {email['subject']}")
            print(f"   From: {email['from']}")
            print(f"   Date: {email['date']}")
            print()

except Exception as e:
    print("\nERROR:")
    print(e)