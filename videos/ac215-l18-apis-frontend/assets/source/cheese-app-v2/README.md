# Cheese App - APIs & Frontend

In this tutorial we run the whole Cheese App on our laptop, in four containers on one Docker network:

| Folder | Container | On your laptop | What it is |
| --- | --- | --- | --- |
| `src/vector-db/` | `cheese-app-vector-db` | http://localhost:8000 | Chroma, the vector database for RAG |
| `src/vector-db/` | `cheese-app-vector-db-cli` | none | A command-line tool that loads the cheese books into Chroma |
| `src/api-service/` | `cheese-app-api-service` | http://localhost:9000 | FastAPI: content, and chat with Gemini, a CNN and RAG |
| `src/frontend-react/` | `cheese-app-frontend-react` | http://localhost:3000 | React + Vite in development, nginx in production |


## Prerequisites
* Docker, with ports 3000, 8000 and 9000 free
* A Google Cloud project with the Vertex AI API enabled
* The `ml-workflow.json` service account key from the `ml-workflow` tutorial. The account needs the
  **Vertex AI User** role.
* About 10 GB of free disk space. The API's image holds TensorFlow.

## Tutorial: Environment Setup

### Clone the github repository
- Clone or download from [here](https://github.com/dlops-io/cheese-app-v2)

### Create the local folders

We never put secrets in Git, so they live outside the repository. Next to the `cheese-app-v2` folder,
create two folders:

- **secrets**, with your `ml-workflow.json` in it
- **persistent-folder**, which keeps the chat history and the trained CNN model

Your folder structure should look like this:
```
   |-cheese-app-v2
     |-docs
     |-images
     |-src
       |---api-service
       |---frontend-react
       |---vector-db
   |-secrets
     |---ml-workflow.json
   |-persistent-folder
```

### Set your Google Cloud project
Change `GCP_PROJECT` to your own project ID at the top of both of these files:
- `src/api-service/docker-shell.sh`
- `src/vector-db/docker-shell.sh`

## Tutorial: Vector DB for RAG Setup
We load the cheese books into Chroma, so the assistant can answer from them. This is the
Retrieval Augmented Generation (RAG) step.

1. Build and run the container:
```bash
cd src/vector-db
```

```bash
./docker-shell.sh
```

2. Load the database. Run this inside the container:
```bash
python cli.py --download --load --chunk_type recursive-split
```

This downloads the text chunks and embeddings we made for you and loads them into Chroma, which takes
about a minute. `--chunk --embed` make the same files from scratch, if you want to see those steps.

3. Try a question through retrieval and Gemini:
```bash
python cli.py --chat --chunk_type recursive-split
```

4. Leave with `exit`. Chroma keeps running in the background, with its data in
`src/vector-db/docker-volumes/chromadb`.

## Tutorial: Backend APIs
We run a FastAPI service for everything the frontend needs.

### Start the API
1. In a new terminal, from the `cheese-app-v2` folder, build and run the container. The first build
   takes a few minutes, because of TensorFlow:
```bash
cd src/api-service
```

```bash
./docker-shell.sh
```

2. Start the server inside the container:
```bash
api_server
```

3. Check that it is up:
- http://localhost:9000/healthz says the process is running
- http://localhost:9000/readyz says it is ready. The first time, this answers `503` until the CNN model
  has downloaded and loaded, and it needs Chroma to be running.

### Create a demo route
Open `api/service.py`, add this after `get_status`, and save. `api_server` reloads by itself.
```python
@app.get("/api/square_root")
def square_root(x: float = 1, y: float = 2):
    z = x**2 + y**2
    return z**0.5
```

- Go to http://localhost:9000/api/square_root. Do you see the result in your browser?
- Go to http://localhost:9000/api/square_root?x=3&y=4. Do you see `5.0`?

### View API docs
FastAPI gives us interactive API documentation for free.
- Go to http://localhost:9000/api/docs
- Try `GET /api/newsletters`

### Review the code
| File | What it does |
| --- | --- |
| `api/service.py` | Creates the app and adds the routers |
| `api/settings.py` | Every setting the API reads. To change the Gemini model, this is the one place |
| `api/routers/newsletter.py`, `podcast.py` | The content routes |
| `api/routers/chat.py` | The chat routes, the same for each mode |
| `api/utils/llm_utils.py` | **Ask** mode: chat with Gemini |
| `api/utils/llm_cnn_utils.py` | **Identify** mode: the CNN names the cheese, and Gemini answers after |
| `api/utils/llm_rag_utils.py` | **Cheese books** mode: Gemini answers from chunks that Chroma finds |
| `api/utils/chat_utils.py` | Saves chats as files in `/persistent` |

Two things to notice in `routers/chat.py`:
- Each message rebuilds the conversation from the saved history. Nothing about a chat stays in
  memory, so any copy of the API can answer it. We need that when we scale in `cheese-app-v3`.
- The routes are plain `def`, not `async def`. Gemini, Chroma and the CNN are blocking calls. FastAPI
  runs a `def` route in a thread, so one slow answer does not stop the API.

Run the tests inside the container:
```bash
pytest
```

Keep this container running.

## Tutorial: React Frontend Setup

### Start the frontend
1. In a new terminal, from the `cheese-app-v2` folder, build and run the container:
```bash
cd src/frontend-react
```

```bash
./docker-shell.sh
```

2. Start the development server inside the container:
```bash
npm run dev
```

3. Open http://localhost:3000

### Review the app
- **Home:** type a question, or use the camera button to add a photo
- **Podcasts and Newsletters:** these load through the API
- **Chat:**
  - **Ask:** a question for Gemini
  - **Identify:** add a photo, then ask about the cheese
  - **Cheese books:** try "How is Tolminc cheese made?"

Your chats appear under **Recent**, and they are still there after you reload the page.

### Review the code
| File | What it does |
| --- | --- |
| `vite.config.js` | Forwards `/api` to the API container |
| `src/main.jsx` | The pages and their URLs |
| `src/lib/api.js` | Every call to the API, and the session ID |
| `src/routes/` | One component per page |
| `src/routes/Chat.jsx` | The chat page: sending a message, loading chats, the three modes |
| `src/components/` | Pieces used on several pages |
| `src/styles.css` | Colors and fonts. The rest of the styling is Tailwind classes in the components |

Check your code before you commit:
```bash
npm run check
```

## Tutorial: Setup & Run Cheese App
Instead of three terminals, one command builds and starts the whole app.

1. Do the [Environment Setup](#tutorial-environment-setup) first, then change `GCP_PROJECT` to your
   own project ID in `src/docker-compose.yml`. It appears twice.

2. If any of the containers above are still running, stop them: Ctrl-C and `exit` in their terminals,
   and `docker compose down` in `src/vector-db`.

3. From the `cheese-app-v2` folder:
```bash
cd src
```

```bash
docker compose up --build
```

The first run takes a few minutes to build the images and load the books. Later runs reuse the
images and skip the load, because the books are already in Chroma.

4. Open http://localhost:3000. and http://localhost:900/api/docs.

The code is still mounted, so the API and the frontend reload when you save. To open a shell in a
running container, for example to run `pytest`, run its `docker-shell.sh` as before.

5. Stop everything with Ctrl-C, then:
```bash
docker compose down
```

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `/readyz` answers `503` with `CNN model is loading` | Wait. The first run downloads the model |
| `/readyz` answers `503` with `Chroma: ...`, or Cheese books says the same | Chroma is not running. Run `docker compose up -d chromadb` in `src/vector-db` |
| Cheese books says `The vector DB is empty` | Load it: step 2 of the Vector DB section |
| Ask says `Gemini: 403` or `PERMISSION_DENIED` | Check `GCP_PROJECT`, the Vertex AI API and the service account's role |
| Ask says `Gemini: 404` | Google retired the model. Change `GENERATIVE_MODEL` in `api/settings.py` |
| Pages load with no content | The API container is not running, or `api_server` is not started |
| `port is already allocated` | Another container is using that port. Stop it, or run `docker ps` to find it |

## Docker Cleanup

Stop the API and frontend containers with Ctrl-C and `exit`, then stop Chroma from `src/vector-db`:
```bash
docker compose down
```

The next command removes images and containers you are not using, across all your projects, so check
the list it shows you first:
```bash
docker system prune
```
