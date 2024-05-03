# Background
Have you ever been captivated by a story brimming with complex relationships? Stories like the Mahabharata, an ancient Indian epic, weave a spell with a multitude of characters and their intricate connections. These connections - familial bonds, alliances, rivalries - form the very foundation of the narrative, driving the plot and shaping the destinies of its heroes and villains.

It all began with a simple conversation. My wife, engrossed in C. Rajagopalachari's masterful translation of the [Mahabharata](https://www.amazon.in/Mahabharata-C-Rajagopalachari/dp/8172764766), sparked my curiosity about the intricate web of relationships within the epic. The idea of translating these connections into a powerful graph model, leveraging the capabilities of [Neo4j](www.neo4j.com) (a leader in Graph Database Industry), became an irresistible challenge.

![alt text](https://github.com/sidagarwal04/mahabharata-genai/blob/main/images/dall-e-mahabharata.png)

This is when I decided to embark on a fascinating journey to explore the Mahabharata through the lens of graph theory. But this was just the first chapter in my journey. I then decided to unveil an ambitious step forward: a Neo4j-powered chatbot. This innovative tool stems from a desire to make the epic’s complex relationships accessible to everyone, transcending traditional query methods.

Read the two-part blog series (for now) on this project:

+ [Unveiling the Mahabharata’s Web: A Graph Journey using Neo4j — (Part 1)](https://sidagarwal04.medium.com/unveiling-the-mahabharatas-web-a-graph-journey-using-neo4j-from-epic-relationships-to-7be4a7a29b6d)
+ [Bringing the Mahabharata Epic to Life: A Neo4j-Powered Chatbot using Google Gemini — (Part 2)](https://sidagarwal04.medium.com/bringing-the-mahabharata-epic-to-life-a-neo4j-powered-chatbot-using-google-gemini-part-2-6eef8676e757)

## What's next?
I initially integrated Google’s Gemini API for natural language processing to craft an interactive experience that allows users to explore the Mahabharata in a way that’s as engaging as the narratives that inspired this project. But later realized, I need to switch to a code-specific LLM instead of a general-purpose LLM. The current version now uses Langchain and I had updated the LLM model hosted on Google Vertex AI Model Garden earlier from `Gemini 1.0 Pro` to `code-bison@002` for natural language to Cypher conversion and another LLM `text-bison` for output text processing. Next after this, I plan to convert this project to a Knowledge Graph application with additional PDF sources attached to get rich output with more content. Read more about this approach (GraphRAG) [here](https://neo4j.com/developer-blog/knowledge-graph-rag-application/).

## Play with chatbot: [https://mahabharata-chatbot.web.app/](https://mahabharata-chatbot.web.app/)
I would like to thank my friend, [Vrijraj Singh](https://vrijraj.xyz/) for all his support in converting this project from a simple gradio application hosted on HuggingFace to a nice web app with a splendid UI.<br/><br/>
Do share your feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSdradX2oOSBpBGAla01tEroQJGDrA62ZsD8Sa_x7IXbGjkRfg/viewform) to make the Mahabharata chatbot the best resource for exploring this epic tale.
