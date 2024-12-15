import os
import requests
import openai
from fastapi import APIRouter, UploadFile, File, HTTPException
from moviepy import VideoFileClip
from app.core.config import settings
import logging
import json
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the lowest level of logs to capture (DEBUG captures all logs)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log format
    handlers=[
        logging.StreamHandler()  # Log to the console by default
    ]
)


router = APIRouter()

# 1. Extract Audio from Video
def extract_audio(file_path):
    video = VideoFileClip(file_path)
    audio = video.audio
    audio_path = "temp/audio.wav"
    audio.write_audiofile(audio_path)
    return audio_path

# 2. Transcribe Audio
def transcribe_audio(audio_path):
    """
    Transcribes audio using the Deepgram API with curl-style headers and POST request.

    Args:
        audio_path (str): The path to the audio file to transcribe.

    Returns:
        dict: JSON response from the API containing the transcription.
    """
    # Your audio file and API key
    api_key = settings.DEEPGRAM_API_KEY
    url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/wav"  # Ensure the content type matches the audio file format
    }
    
    # Open the audio file in binary mode
    with open(audio_path, "rb") as audio_file:
        response = requests.post(url, headers=headers, data=audio_file)

    # Handle the response from the API
    if response.status_code == 200:
        print("Transcription Successful!")
        return response.json()  # Return the transcription result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        raise Exception(f"Error transcribing audio: {response.text}")
    
    
def analyze_sentiment_segment(transcribed_text):
    """
    Analyzes the sentiment of the given transcribed text using OpenAI's GPT-3.5-turbo model.
    Logs detailed information and handles errors gracefully.
    """
    api_key =settings.OPENAI_API_KEY
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    data = {
        "model": "gpt-3.5-turbo",
       "messages": [
        {"role": "system", "content": "You are an assistant skilled in text analysis and sentiment interpretation."},
        {
        "role": "user",
        "content": f"Please analyze the sentiment of the following transcribed text with timestamps. "
                    f"For each timestamped segment, identify the sentiment (positive, negative, or neutral) "
                    f"and explain the reasoning. Ensure the analysis is clear, concise, and directly correlates "
                    f"with the corresponding text and timestamp: \n\n{ transcribed_text}"
        }
        ],
        "max_tokens": 200
    }

    try:
        logging.info("Sending request to OpenAI API...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            logging.info("Request successful. Parsing response...")
            result = response.json()["choices"][0]["message"]["content"].strip()
            logging.info(f"Sentiment Analysis Result: {result}")
            return result
        else:
            # Log and raise specific errors for non-200 status codes
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to OpenAI API failed: {e}")
        raise RuntimeError(f"API request error: {e}")
    
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        raise RuntimeError(f"JSON parsing error: {e}")
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise RuntimeError(f"Unexpected error: {e}")
    

def summarizeTranscribe(transcribed_text):
    """
    Analyzes the sentiment of the given transcribed text using OpenAI's GPT-3.5-turbo model.
    Logs detailed information and handles errors gracefully.
    """
    api_key =settings.OPENAI_API_KEY
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    data = {
        "model": "gpt-3.5-turbo",
       "messages": [
        {"role": "system", "content": "You are an assistant skilled in text analysis and sentiment interpretation."},
        {
        "role": "user",
        "content": f"Please summarize of the following transcribed text: \n\n{ transcribed_text}"
        }
        ],
        "max_tokens": 200
    }

    try:
        logging.info("Sending request to OpenAI API...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            logging.info("Request successful. Parsing response...")
            result = response.json()["choices"][0]["message"]["content"].strip()
            logging.info(f"Sentiment Analysis Result: {result}")
            return result
        else:
            # Log and raise specific errors for non-200 status codes
            logging.error(f"Request failed with status code {response.status_code}: {response.text}")
            response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to OpenAI API failed: {e}")
        raise RuntimeError(f"API request error: {e}")
    
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        raise RuntimeError(f"JSON parsing error: {e}")
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise RuntimeError(f"Unexpected error: {e}")
    
   
    
# 4. Analyze Toxicity (using Google Perspective API)
def analyze_toxicity(text):
    api_key = settings.GOOGLE_PERSPECTIVE_API_KEY
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    params = {"key": api_key}
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()  # Ensure errors are caught
    return response.json()

# 5. Detect Pauses in Speech
def detect_pauses(timestamps):
    pauses = []
    for i in range(1, len(timestamps)):
        if timestamps[i] - timestamps[i-1] > 2.0:  # Pauses longer than 2 seconds
            pauses.append((timestamps[i-1], timestamps[i]))
    return pauses

def segment_transcription(transcription):
    try:
        #print(transcription["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0]["sentences"])
        # Log the start of the segmentation process
        logging.info("Starting segmentation of transcription.")
        
        sentences = transcription["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"][0]["sentences"]
        
        # Ensure the words list is available
        if not sentences:
            logging.warning("No Sentences found in the transcription result.")
            return []
        
        segments = sentences
        logging.info(f"Segmentation complete. Total segments: {len(segments)}")
        print(segments)
        return segments
    
    except Exception as e:
        logging.error(f"An error occurred while segmenting the transcription: {e}")
        return []  # Return an empty list if error occurs



def check_toxicity_and_store_results(toxicity_data_list, threshold=0.5):
    """
    Check toxicity for multiple inputs and store the results in an array.

    Parameters:
    - toxicity_data_list (list of dict | dict): A list of JSON-like dictionaries or a single dictionary containing toxicity analysis.
    - threshold (float): The probability threshold for determining toxicity.

    Returns:
    - list: A list of dictionaries with `is_toxic` and `score` results for each input.
    """
    # Ensure the input is a list
    if isinstance(toxicity_data_list, dict):
        toxicity_data_list = [toxicity_data_list]

    results = []
    for idx, toxicity_data in enumerate(toxicity_data_list):
        try:
            # Extract the summary score
            toxicity_score = toxicity_data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
            # Check if it exceeds the threshold
            is_toxic = toxicity_score >= threshold

            # Append result to the array
            results.append({
                "index": idx,
                "is_toxic": is_toxic,
                "score": toxicity_score
            })
        except KeyError:
            # Handle cases where the required data is missing
            results.append({
                "index": idx,
                "error": "Invalid data format: TOXICITY summaryScore not found."
            })
    return results

@router.post("/analyze")
async def analyze_video_endpoint(file: UploadFile = File(...)):
    try:
        # Save the uploaded video
        os.makedirs("temp", exist_ok=True)
        file_location = os.path.join("temp", file.filename)

        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Extract audio from the video
        audio_path = extract_audio(file_location)

        # Transcribe audio to text
        transcription = transcribe_audio(audio_path)
       
        transcribe_text=transcription["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(f"Transcribe : {transcribe_text}")
        
        
        
        summary=summarizeTranscribe(transcribe_text)
        print(f"Summary Results: {summary}")
          # Segment the transcription into 5-second intervals
        segments = segment_transcription(transcription)

       
        # Analyze sentiment for each segment
        sentiment_results = [
            {
                'start_time': segment['start'],  # The start time of the first word in the segment
                'sentiment': analyze_sentiment_segment(segment)
            }
            for segment in segments
        ]
        
        # sentiment_results=analyze_sentiment_segment(segments)
        print(f"Sentiment Results: {sentiment_results}")

        # Detect harmful content (toxicity, hate speech, etc.)
        toxicity = analyze_toxicity(transcribe_text)
        print(f"Toxic data: {toxicity}")
        toxicityThreshold = 0.5
        toxicResult= check_toxicity_and_store_results(toxicity, toxicityThreshold)
        print(f"Toxic: {toxicResult}")

        print(f"{toxicity}")
         
        #toxicity=[]

        # Detect pauses in speech based on timestamps
        # timestamps = transcription["results"]["channels"][0]["alternatives"][0]["words"]
        # #pauses = detect_pauses([word["start_time"] for word in timestamps])
        # pauses=[]
        # Clean up temporary files
        os.remove(file_location)
        os.remove(audio_path)

        return {
            "message": "Video analysis complete",
            "sentiment_results": sentiment_results,
            "summary" : summary,
            "toxicity": toxicResult
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
