## **Agent Orchestrator**

In this section we build the workflow that assembles all the agents together.

1.  **The Order (Input)**: The user requests a quiz on "Italian Cheeses."
2.  **Research (Agent 1)**: The request goes to **Professor Stilton**. He searches for 5 key facts about Pecorino, Parmesan, Mozzarella, etc.
3.  **Creation (Agent 2)**: The facts are passed to **Brie**. She crafts 5 multiple-choice questions based on the facts.
4.  **Verification (Agent 3)**: The draft quiz is sent to **Cheddar**. He flags one question as potentially confusing and sends it back to Brie with a note. Brie revises it and sends it back to Cheddar, who now approves the whole set.
5.  **Formatting (Agent 4)**: The final, approved quiz goes to **Ricotta**, who formats it into structured JSON.
6.  **Delivery (Output)**: The final, polished quiz is presented to the user.
