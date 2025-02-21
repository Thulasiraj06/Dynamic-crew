import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from crew_manager import CrewManager
from crew_factory import create_crew
from pathlib import Path
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Ensure the API key is available
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found. Ensure it is set in the environment or .env file.")

# Initialize CrewManager
crew_manager = CrewManager()

@app.get("/api/run-crew/{crew_id}")
async def run_crew(
    crew_id: str,
    topic: str = Query(..., min_length=1, description="The topic for the crew to process")
):
    """
    Endpoint to trigger a Crew process based on crew_id and return a formatted result.
    """
    try:
        # Log the request
        logger.info(f"Received request to run crew {crew_id} with topic: {topic}")

        # Get the appropriate crew configuration
        crew_config = crew_manager.crews.get(crew_id)
        if not crew_config:
            raise HTTPException(status_code=404, detail=f"Crew ID {crew_id} not found")

        print(crew_config)
        # Create the crew instance using the factory
        crew_instance = create_crew(crew_config)

        # Run the crew process with the topic
        inputs = {"topic": topic}
        result = crew_instance.kickoff(inputs=inputs)

        # Format the result for better readability
        formatted_output = {
            "crew_id": crew_id,
            "topic": topic,
            "result": result  # Assuming `result` is JSON-serializable
        }

        # Log the successful execution
        logger.info(f"Crew {crew_id} executed successfully for topic: {topic}")
        return {"success": True, "data": formatted_output}

    except ValueError as e:
        logger.error(f"ValueError occurred: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")