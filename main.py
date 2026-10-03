from agent import PersonalAssistant


def main():

    assistant = PersonalAssistant()

    print("===================================")
    print("        PersonalAI v0.2")
    print("===================================")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        assistant.run(user_input)


if __name__ == "__main__":
    main()