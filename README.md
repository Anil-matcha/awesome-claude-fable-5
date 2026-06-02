# Veo 4 API: Python Wrapper for Google DeepMind's AI Video Generator

[![PyPI version](https://img.shields.io/pypi/v/veo-4-api.svg)](https://pypi.org/project/veo-4-api/)
[![GitHub stars](https://img.shields.io/github/stars/Anil-matcha/Veo-4-API.svg)](https://github.com/Anil-matcha/Veo-4-API/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

The most comprehensive Python wrapper for the **Veo 4 API** (developed by Google DeepMind), delivered via [muapi.ai](https://muapi.ai). Generate native 4K AI videos up to 30 seconds with integrated audio, character consistency, and advanced camera controls — Google's most powerful video generation model.

Join subreddit [Veo4](https://www.reddit.com/r/Veo4_/) for discussion

> 🌊 **Also explore these top AI video models:**
> - [Seedance 2.0 API](https://github.com/Anil-matcha/Seedance-2.0-API) — ByteDance's cinematic 2K video model with character sheets & omni-reference
> - [HappyHorse 1.0 API](https://github.com/Anil-matcha/HappyHorse-1.0-API) — Alibaba's #1 ranked model (1392 Elo I2V) with native 1080p & integrated audio

## Related Projects

- [veo4-video-generator](https://github.com/SamurAIGPT/veo4-video-generator) — Ready-made Next.js SaaS built on Veo 4
- [veo3.1-comfyui](https://github.com/Anil-matcha/veo3.1-comfyui) — Run Veo 3.1 inside ComfyUI

## 🚀 Why Use Veo 4 API?

Veo 4 is Google DeepMind's latest state-of-the-art AI video generation model, featuring a 3x larger Transformer architecture than Veo 3, native 4K output, and advanced character anchoring technology.

- **Native 4K Output**: Every pixel generated from scratch — not upscaled.
- **Up to 30 Seconds**: Longer clips than any previous Veo model.
- **Integrated Audio**: Jointly generates synchronized dialogue, ambient sound, and music in one pass (building on Veo 3's audio breakthrough).
- **Character Consistency**: Advanced anchoring technology keeps faces, clothing, and features consistent across all frames and camera angles.
- **Advanced Camera Controls**: Pan, zoom, orbit, tracking shots — precise cinematic control.
- **Developer-First**: Simple Python SDK via MuAPI infrastructure.

## 🌟 Key Features of Veo 4 API

- ✅ **Veo 4 Text-to-Video (T2V)**: Transform descriptive prompts into stunning native 4K video clips up to 30 seconds.
- ✅ **Veo 4 Image-to-Video (I2V)**: Animate static images with precise motion and camera control using `images_list`.
- ✅ **Integrated Audio-Video Generation**: Jointly generate synchronized audio and video in one pass — include sound cues in your prompt.
- ✅ **Character Consistency**: `character_video()` anchors on reference photos to keep identity consistent across scenes.
- ✅ **Advanced Camera Controls**: Specify `camera_control` for cinematic movements — pan, zoom, orbit, tracking shots.
- ✅ **Video Extension**: Extend existing Veo 4 clips up to 30 seconds total.
- ✅ **Video Edit**: Edit existing videos using natural language prompts.
- ✅ **File Upload**: Upload local images and videos directly via `upload_file()`.
- ✅ **Flexible Aspect Ratios**: Optimized for `16:9`, `9:16` (TikTok/Reels), and `1:1`.
- ✅ **Quality Tiers**: `1080p` and `4k` (native) output.

---

## 🛠 Installation

### Via Pip (Recommended)
```bash
pip install veo-4-api
```

### From Source
```bash
git clone https://github.com/Anil-matcha/Veo-4-API.git
cd Veo-4-API
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the root directory and add your [MuAPI](https://muapi.ai) API key:
```env
MUAPI_API_KEY=your_muapi_api_key_here
```

---

## 🤖 Veo 4 MCP Server

Use Veo 4 as an **MCP (Model Context Protocol)** server, allowing AI assistants like Claude Desktop or Cursor to directly invoke Veo 4 generation tools.

### Running the MCP Server
1. Ensure `MUAPI_API_KEY` is set in your environment.
2. Run the server:
   ```bash
   python3 mcp_server.py
   ```
3. To test with the MCP Inspector:
   ```bash
   npx -y @modelcontextprotocol/inspector python3 mcp_server.py
   ```

---

## 💻 Quick Start with Veo 4 API (Python)

```python
from veo4_api import Veo4API

# Initialize the Veo 4 client
api = Veo4API()

# Generate Video from Text (T2V)
print("Generating AI Video using Veo 4...")
submission = api.text_to_video(
    prompt="A cinematic tracking shot through a lush rainforest, sunlight filtering through the canopy, birds calling",
    aspect_ratio="16:9",
    duration=8,
    quality="4k",
    camera_control="tracking shot"
)

# Wait for completion
result = api.wait_for_completion(submission['request_id'])
print(f"Success! View your Veo 4 video here: {result['outputs'][0]}")
```

---

## 🎵 Audio-Video Generation

Veo 4 jointly generates synchronized video and audio in a single pass — include sound cues in your prompt for best results.

```python
from veo4_api import Veo4API

api = Veo4API()

# Text-to-video with audio
submission = api.text_to_video_with_audio(
    prompt="A street musician playing violin in Paris, rain on cobblestones, distant traffic, melancholic melody",
    aspect_ratio="16:9",
    duration=15,
    quality="4k"
)
result = api.wait_for_completion(submission['request_id'])
print(f"Video with audio: {result['outputs'][0]}")

# Image-to-video with audio
submission = api.image_to_video_with_audio(
    prompt="@image1 comes alive — waves crashing, seagulls calling, ocean breeze rustling palm trees",
    images_list=["https://example.com/beach.jpg"],
    duration=10,
)
result = api.wait_for_completion(submission['request_id'])
print(f"Animated with audio: {result['outputs'][0]}")
```

> **Tip**: Include explicit sound cues (e.g. "thunder rumbling", "crowd cheering", "piano melody") for richer, more accurate audio generation.

---

## 🎭 Character Consistency

Veo 4's character anchoring keeps faces and identity consistent across all frames.

```python
from veo4_api import Veo4API

api = Veo4API()

# Anchor on a reference photo
submission = api.character_video(
    prompt="@image1 walks confidently through a neon-lit Tokyo street at night",
    character_images=["https://example.com/person.jpg"],
    aspect_ratio="16:9",
    duration=8,
    quality="4k",
    with_audio=True,
)
result = api.wait_for_completion(submission['request_id'])
print(f"Character video: {result['outputs'][0]}")
```

---

## 🎬 Camera Controls

Specify cinematic camera movements with the `camera_control` parameter.

```python
# Zoom in dramatically
submission = api.text_to_video(
    prompt="A lone lighthouse on a rocky cliff at dusk, storm approaching",
    aspect_ratio="16:9",
    duration=10,
    quality="4k",
    camera_control="slow zoom in"
)

# Orbit around a subject
submission = api.text_to_video(
    prompt="A marble statue in a sunlit museum courtyard",
    aspect_ratio="16:9",
    duration=8,
    camera_control="orbit"
)
```

---

## 📡 API Endpoints & Reference

### 1. Veo 4 Text-to-Video (T2V)
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-t2v`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-t2v" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "A majestic eagle soaring over snow-capped mountains at sunrise",
      "aspect_ratio": "16:9",
      "duration": 8,
      "quality": "4k",
      "camera_control": "pan right"
  }'
```

### 2. Veo 4 Image-to-Video (I2V)
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-i2v`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-i2v" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "@image1 — the clouds drift slowly, light shifts from golden to dusk",
      "images_list": ["https://example.com/landscape.jpg"],
      "aspect_ratio": "16:9",
      "duration": 8,
      "quality": "4k"
  }'
```

### 3. Veo 4 T2V with Audio
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-t2v-audio`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-t2v-audio" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "A busy Tokyo street at night, neon signs, rain, jazz music drifting from a bar",
      "aspect_ratio": "16:9",
      "duration": 15,
      "quality": "4k"
  }'
```

### 4. Veo 4 I2V with Audio
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-i2v-audio`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-i2v-audio" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "@image1 — waves begin to crash, seagulls cry in the distance, wind howling",
      "images_list": ["https://example.com/ocean.jpg"],
      "aspect_ratio": "16:9",
      "duration": 10,
      "quality": "4k"
  }'
```

### 5. Veo 4 Character Video
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-character`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-character" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "@image1 walks confidently through a neon-lit Tokyo street",
      "images_list": ["https://example.com/person.jpg"],
      "aspect_ratio": "16:9",
      "duration": 8,
      "quality": "4k"
  }'
```

### 6. Video Extension
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-extend`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-extend" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "request_id": "your-completed-request-id",
      "prompt": "The eagle lands on a mountain peak, surveying the valley below",
      "duration": 10,
      "quality": "4k"
  }'
```

### 7. Video Edit
**Endpoint**: `POST https://api.muapi.ai/api/v1/veo-4-video-edit`

```bash
curl --location --request POST "https://api.muapi.ai/api/v1/veo-4-video-edit" \
  --header "Content-Type: application/json" \
  --header "x-api-key: YOUR_API_KEY" \
  --data-raw '{
      "prompt": "Change the weather to a dramatic thunderstorm",
      "video_urls": ["https://example.com/video.mp4"],
      "aspect_ratio": "16:9",
      "quality": "4k"
  }'
```

---

## 📖 API Method Reference

| Method | Parameters | Description |
| :--- | :--- | :--- |
| `text_to_video` | `prompt`, `aspect_ratio`, `duration`, `quality`, `with_audio`, `camera_control` | Generate native 4K video from text. |
| `image_to_video` | `prompt`, `images_list`, `aspect_ratio`, `duration`, `quality`, `with_audio`, `camera_control` | Animate images into 4K video. |
| `text_to_video_with_audio` | `prompt`, `aspect_ratio`, `duration`, `quality`, `camera_control` | T2V with jointly generated audio. |
| `image_to_video_with_audio` | `prompt`, `images_list`, `aspect_ratio`, `duration`, `quality`, `camera_control` | I2V with jointly generated audio. |
| `character_video` | `prompt`, `character_images`, `aspect_ratio`, `duration`, `quality`, `with_audio` | Consistent character identity across frames. |
| `extend_video` | `request_id`, `prompt`, `duration`, `quality` | Extend an existing Veo 4 video segment. |
| `video_edit` | `prompt`, `video_urls`, `images_list`, `aspect_ratio`, `quality` | Edit existing videos with natural language. |
| `upload_file` | `file_path` | Upload a local file (image or video) to MuAPI. |
| `get_result` | `request_id` | Check task status and retrieve outputs. |
| `wait_for_completion` | `request_id`, `poll_interval`, `timeout` | Blocking helper — polls until generation completes. |

---

## 🔗 Official Resources
- **API Provider**: [MuAPI.ai](https://muapi.ai)

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Keywords**: Veo 4 API, Google Veo 4, Google DeepMind Video, AI Video Generator, Text-to-Video AI, Image-to-Video API, Veo 4 Python SDK, Google Video AI, Audio Video Generation, 4K AI Video, Character Consistency AI, Camera Control Video, MuAPI, Video Generation API, Native 4K Video, AI Video Creation, Veo 4 API Documentation, Veo 4 I2V, Veo 4 T2V, Python Video API.
