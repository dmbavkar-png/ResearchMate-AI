from router import ToolRouter


router = ToolRouter()


tests = [
    "Show my inbox",
    "Do I have emails about research?",
    "Open email 2",
    "Draft an email to Dr. Sharma about research",
    "Send this email",
    "Explain artificial intelligence"
]


for test in tests:

    print("\nUSER:")
    print(test)

    result = router.route(test)

    print("ROUTER:")
    print(result)