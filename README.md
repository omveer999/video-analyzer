# Video Analyzer

## Overview
The **Video Analyzer** project is a FastAPI-based application that processes video files to perform various analyses, including:

- Extracting audio from videos.
- Transcribing audio into text using the Deepgram API.
- Performing sentiment analysis using OpenAI's GPT-3.
- Detecting harmful content (e.g., toxicity) using the Google Perspective API.

## Features
- **Audio Extraction**: Extracts audio from the uploaded video.
- **Transcription**: Converts the extracted audio into text using the Deepgram API.
- **Sentiment Analysis**: Analyzes the sentiment of the transcribed text using OpenAI GPT-3.
- **Toxicity Detection**: Detects harmful content in the transcribed text using Google Perspective API.

## Technologies Used
- **Backend Framework**: FastAPI
- **Audio & Video Processing**: MoviePy
- **APIs**:
  - Deepgram API (for audio transcription)
  - OpenAI API (for sentiment analysis)
  - Google Perspective API (for toxicity detection)
- **Python Libraries**: requests, os, openai

## Prerequisites
1. Python 3.10+
2. Install [FFmpeg](https://ffmpeg.org/download.html) on your system.
3. API keys for:
   - Deepgram API
   - OpenAI API
   - Google Perspective API

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/video-analyzer.git
cd video-analyzer
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv fastapi-env
source fastapi-env/bin/activate  # On Windows, use `fastapi-env\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root of the project and add the following:
```
DEEPGRAM_API_KEY=your_deepgram_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_PERSPECTIVE_API_KEY=your_google_perspective_api_key
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### 6. Cache Clear
```bash
find . -name "*.pyc" -exec rm -f {} \;
```

## API Endpoints

### 1. **POST** `/api/video/analyze`
Uploads a video file for analysis.

#### Request
- **File**: A video file (e.g., `.mp4`, `.mov`).

#### Response
```json
{
  "message": "Video analysis complete",
  "sentiment_results": [
    {
      "start_time": 3.6799998,
      "sentiment": "Segment: 3.68s - 8.26s\n\nSentiment: Negative\n\nReasoning: The sentiment of this segment is negative as the speaker mentions struggling to get their kids out the door on time, indicating a sense of difficulty and frustration in managing this task. The word \"struggled\" carries a negative connotation, reflecting the challenges the speaker is facing."
    },
    {
      "start_time": 9.5199995,
      "sentiment": "Segment Timestamp: [9.52s - 10.02s]\n\nSentiment Analysis:\n- **Sentiment**: Neutral\n- **Reasoning**: The text \"Yeah.\" itself is a simple and brief response without much emotion or context provided. Therefore, it conveys a neutral sentiment as it does not express either positivity or negativity."
    },
    {
      "start_time": 10.4,
      "sentiment": "Segment at 10.4-11.12: \nSentiment: Neutral\n\nExplanation: The text \"So you know\" is neutral in sentiment as it does not convey a positive or negative emotion. It appears to be a statement providing information without any explicit positivity or negativity."
    },
    {
      "start_time": 11.12,
      "sentiment": "Segment: Right? (11.10s - 11.52s) \n\nSentiment Analysis:\n- Sentiment: Neutral\n- Reasoning: The text \"Right?\" is brief and lacks context, making it difficult to determine a specific sentiment. It seems to be a standalone question mark, which typically does not convey a positive or negative sentiment but rather seeks confirmation or agreement. As there are no clear positive or negative indicators, the sentiment is deemed neutral."
    },
    {
      "start_time": 11.5199995,
      "sentiment": "Timestamp: 11.52 - 12.82\n\nText: \"It's like herding kittens.\"\n\nSentiment: Negative\n\nReasoning: The expression \"herding kittens\" is commonly used to convey a sense of chaos, difficulty, or frustration, as kittens are known to be independent and hard to control. This metaphor typically implies a challenging and unruly situation, suggesting a negative sentiment in the text."
    }
  ],
  "summary": "The text is about a parent who struggles to get their children out the door on time. Despite nagging and attempts to get the children organized, they find themselves constantly running late. The parent recounts a particular chaotic morning where the children were not cooperating, leading to frustration and a realization about accountability. The parent learns the importance of modeling accountability themselves before expecting it from others. This story highlights the challenges of parenting and the importance of personal responsibility in achieving collective goals.",
  "toxicity": [
    {
      "index": 0,
      "is_toxic": false,
      "score": 0.11739369
    }
  ]
}
```

### Response Fields
- **`message`**: Confirmation message.
- **`sentiment_results`**: Sentiment analysis result (e.g., Positive, Negative, Neutral).
- **`toxicity`**: Detailed toxicity analysis result.
- **`summary`**: List of pauses detected in speech (start and end times).

## Key Functions
1. **`extract_audio(file_path)`**:
   Extracts audio from a video file.

2. **`transcribe_audio(audio_path)`**:
   Transcribes audio to text using the Deepgram API.

3. **`analyze_sentiment(transcribed_text)`**:
   Analyzes the sentiment of the text using OpenAI's GPT-3.

4. **`analyze_toxicity(text)`**:
   Analyzes harmful content in text using the Google Perspective API.


## Testing
Use a tool like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to test the endpoints:

```bash
curl -X POST "http://127.0.0.1:8000/api/video/analyze" \
-F "file=@path_to_your_video_file.mp4"
```

## Known Issues
- Ensure FFmpeg is installed and accessible in your system path.
- Large video files may cause performance issues; optimize the video size before uploading.

## Future Improvements
- Add support for multiple languages in transcription.
- Enhance the toxicity analysis with additional attributes.
- Integrate with a database for storing analysis results.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please submit a pull request or raise an issue to discuss potential changes.

## Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Deepgram](https://deepgram.com/)
- [OpenAI](https://openai.com/)
- [Google Perspective API](https://www.perspectiveapi.com/)

