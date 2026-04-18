class HybridMemory:
    """
    Short-term + Long-term memory
    """

    def __init__(self):
        self.store = {}

    def get(self, thread_id):
        return self.store.get(thread_id, {
            "summary": "",
            "messages": []
        })

    def update(self, thread_id, user_msg, ai_msg):

        data = self.get(thread_id)

        # store messages
        data["messages"].append(("user", user_msg))
        data["messages"].append(("ai", ai_msg))

        # keep only last 2 exchanges (4 entries)
        data["messages"] = data["messages"][-4:]

        # update summary if needed
        if len(data["messages"]) >= 4:
            data["summary"] += f" User asked about {user_msg[:50]}."

        self.store[thread_id] = data