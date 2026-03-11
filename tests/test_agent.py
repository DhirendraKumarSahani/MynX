from app.agents.react_agent import ReactAgentBuilder


def test_agent():

    agent = ReactAgentBuilder()

    thread_id = "user_1"

    result1 = agent.run(
        "What is SpaceX?",
        thread_id=thread_id
    )

    print("\nFirst Response:\n")
    print(result1["messages"][-1].content)

    result2 = agent.run(
        "Who founded it?",
        thread_id=thread_id
    )

    print("\nSecond Response (memory aware):\n")
    print(result2["messages"][-1].content)


if __name__ == "__main__":
    test_agent()