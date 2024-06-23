# Introduction
Mahabharata Chatbot is a sophisticated chatbot designed to provide detailed insights and answer questions related to the epic Mahabharata. Leveraging advanced NLP techniques and deep learning models, the bot offers a unique interactive experience, bringing the ancient text to life.

## Background
Have you ever been captivated by a story brimming with complex relationships? Stories like the Mahabharata, an ancient Indian epic, weave a spell with a multitude of characters and their intricate connections. These connections - familial bonds, alliances, rivalries - form the very foundation of the narrative, driving the plot and shaping the destinies of its heroes and villains.

It all began with a simple conversation. My wife, engrossed in C. Rajagopalachari's masterful translation of the [Mahabharata](https://www.amazon.in/Mahabharata-C-Rajagopalachari/dp/8172764766), sparked my curiosity about the intricate web of relationships within the epic. The idea of translating these connections into a powerful graph model, leveraging the capabilities of [Neo4j](www.neo4j.com) (a leader in Graph Database Industry), became an irresistible challenge.

![alt text](https://github.com/sidagarwal04/mahabharata-genai/blob/main/images/dall-e-mahabharata.png)

This is when I decided to embark on a fascinating journey to explore the Mahabharata through the lens of graph theory. But this was just the first chapter in my journey. I then decided to unveil an ambitious step forward: a Neo4j-powered chatbot. This innovative tool stems from a desire to make the epic’s complex relationships accessible to everyone, transcending traditional query methods.

Read the three-part blog series on this project:

+ [Unveiling the Mahabharata’s Web: A Graph Journey using Neo4j — (Part 1)](https://sidagarwal04.medium.com/unveiling-the-mahabharatas-web-a-graph-journey-using-neo4j-from-epic-relationships-to-7be4a7a29b6d)
+ [Bringing the Mahabharata Epic to Life: A Neo4j-Powered Chatbot using Google Gemini — (Part 2)](https://sidagarwal04.medium.com/bringing-the-mahabharata-epic-to-life-a-neo4j-powered-chatbot-using-google-gemini-part-2-6eef8676e757)
+ [From Ancient Epic to Modern Marvel: Demystifying the Mahabharata Chatbot with GraphRAG (Part 3)](https://medium.com/@sidagarwal04/from-ancient-epic-to-modern-marvel-demystifying-the-mahabharata-chatbot-with-graphrag-part-3-5942260a9560)

Read more about GraphRAG here: [Building a GraphRAG application](https://neo4j.com/developer-blog/knowledge-graph-rag-application/)

## Features
+ **Contextual Understanding:** Provides answers based on the context of the Mahabharata.
+ **Interactive Q&A:** Users can ask questions and get detailed answers.
+ **Relationship Mapping:** Visualizes and explains relationships between characters.
+ **Deployment Ready:** Easily deployable on platforms like Firebase.

## Architecture

The Mahabharata Chatbot is built using:

+ **Backend:** Python, Google Vertex AI (Google Gemini API), Gradio
+ **Frontend:** Nuxt.js
+ **Database:** Neo4j
+ **Deployment:** Hugging Face Space, Firebase

## Configuration
### Environment Variables
Make sure to add following  environment variables in your Hugging Face project and follow the instructions in setup.md file:

```
BOB
NEO4J_USERNAME
NEO4J_URI
NEO4J_PASSWORD
PROJECT_ID
LOCATION
```

### Database Setup
1. Start Neo4j Database:

Follow the official [Neo4j installation guide](https://neo4j.com/developer/) to set up your database.

2. Load Data:
Use provided [scripts](mahabharata-genai/blob/main/mahabharata-db-setup.cypher) to load Mahabharata data into Neo4j.

## Play with chatbot: [https://mahabharata-chatbot.web.app/](https://mahabharata-chatbot.web.app/)

## Contributing
Do share your feedback [here](https://docs.google.com/forms/d/e/1FAIpQLSdradX2oOSBpBGAla01tEroQJGDrA62ZsD8Sa_x7IXbGjkRfg/viewform) to make the Mahabharata chatbot the best resource for exploring this epic tale. I am welcoming contributions! Please follow these steps:

+ Fork the repository.
+ Create a new branch: `git checkout -b feature/YourFeature`
+ Make your changes and commit them: `git commit -m 'Add some feature'`.
+ Push to the branch: `git push origin feature/YourFeature`.
+ Create a pull request.

## License
This project is licensed under the [Apache License](mahabharata-genai/blob/main/LICENSE).

## Acknowledgements
Special thanks to my friend, [Vrijraj Singh](https://vrijraj.xyz/) for all his support in building web design for this app, [LLM Graph Builder Tool](https://neo4j.com/labs/genai-ecosystem/llm-graph-builder/) for converting external PDF sources into Knowledge Graph and the open-source community for their valuable resources and support.
