## **Meet the Agents: The Guild Members**

In this section we build the core agents required for our multi-agent system. Giving our agents distinct personas will make them more specialized in their roles.

#### 🧐 **Professor Stilton, the Fact-Finder**
This agent's primary job is to take the user's topic and use a **search tool** to find interesting, verifiable facts.

#### 🌱 **Cashew, the Plant-Based Pro**
Cashew supplements Professor Stilton's research with up to three additional facts when the topic involves vegan or plant-based cheese.

#### ✍️ **Brie, the Creative Wordsmith**
The Brie Agent takes the raw facts from Professor Stilton and transforms them into engaging quiz questions (multiple choice, true/false, etc.). She's the core "creative" LLM.

#### 🧀 **Cheddar, the Sharp Critic**
Cheddar Agent reviews the questions and answers created by Brie. He checks them against Stilton's original facts for accuracy. He also ensures the questions are clear and not too easy or impossibly hard.

#### 🎨 **Mozzarella, the Master Formatter**
The Mozzarella Agent takes a quiz that is approved by Cheddar and converts it to Markdown format.

#### 🎨 **Ricotta, the Schema Scribe**
Ricotta takes a quiz that is approved by Cheddar and converts it into strict JSON.
