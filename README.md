# NeuroCourier WhatsApp Integration

**NeuroCourier** is a local‑first AI assistant that integrates WhatsApp with a locally running Large Language Model (LLM) using Ollama. This system allows users to chat with your local AI directly through WhatsApp, while keeping inference private and under your control.

This document explains everything from initial setup to full system architecture, including Meta developer setup, webhook configuration, tunneling, backend development, and LLM integration.
<p align="center">
<img src="https://github.com/user-attachments/assets/6e9a2912-05c1-4fa5-ac95-840a01242c3e" width="300"/>
</p>

# Table of Contents

1. Overview
2. What We Achieved
3. System Architecture
4. Technologies Used
5. Prerequisites
6. Step 1 - Meta Developer Account Setup
7. Step 2 - Create WhatsApp App
8. Step 3 - Configure WhatsApp API
9. Step 4 - Add Test Phone Numbers
10. Step 5 - Backend Server Creation (FastAPI)
11. Step 6 - Ollama LLM Integration
12. Step 7 - Exposing Local Server to Internet (Cloudflare Tunnel)
13. Step 8 - Webhook Configuration
14. Step 9 - Enable Message Subscription
15. Step 10 - Message Processing Flow
16. Step 11 - Access Token Management
17. Step 12 - Running the System
18. Step 13 - Full Execution Flow
19. Step 14 - Project Structure
20. Step 15 - Commands Used
21. Step 16 - Troubleshooting Guide
22. Step 17 - Development vs Production Mode
23. Step 18 - Current Limitations
24. Step 19 - Future Improvements
25. Summary

# Overview

This project connects WhatsApp with a locally running AI model using the official WhatsApp Cloud API.

Users send messages on WhatsApp → NeuroCourier receives them → processes using Ollama → replies automatically.

All AI inference runs locally.

No external AI API required.

# What We Achieved

We successfully built a complete working pipeline:

* Receive WhatsApp messages
* Process messages using local LLM
* Generate AI responses locally
* Send replies back to WhatsApp
* Handle multiple users
* Maintain full privacy

This system functions like a production chatbot backend.

# System Architecture

```
WhatsApp User
     ↓
Meta WhatsApp Cloud API
     ↓
Cloudflare Tunnel
     ↓
FastAPI Webhook Server (Local Machine)
     ↓
Ollama Local LLM
     ↓
FastAPI sends reply via WhatsApp API
     ↓
User receives response
```

# Technologies Used

## Messaging Platform

* WhatsApp Cloud API
* Meta Developer Platform

## Backend

* Python
* FastAPI
* Requests library

## AI Engine

* Ollama
* Model: qwen3-vl:2b

## Networking

* Cloudflare Tunnel

## Operating Environment

* Linux
* Local machine deployment

# Prerequisites

Required software:

* Python 3.10+
* Ollama installed
* Meta developer account
* WhatsApp account
* Cloudflare tunnel installed

# Step 1 - Meta Developer Account Setup

Go to:

[https://developers.facebook.com/](https://developers.facebook.com/)

Create developer account.

Verify identity.

# Step 2 - Create WhatsApp App

<img width="965" height="564" alt="step 2" src="https://github.com/user-attachments/assets/ec53ad7c-2f8a-44de-bb15-de5978184e7b" />

Steps:

1. Click "My Apps"
2. Click "Create App"
3. Select "Business"
4. Enter:

```
App Name: NeuroCourier
App Type: Business
```

Create app.

# Step 3 - Add WhatsApp Product

Inside app dashboard:

Click:

```
Add Product → WhatsApp → Setup
```

Meta provides:

* Phone Number ID
* WhatsApp test number
* Temporary access token

Save these values.

# Step 4 - Add Test Phone Numbers

<img width="1920" height="1080" alt="step4" src="https://github.com/user-attachments/assets/7d13ad47-a7ac-49d0-996f-ef80f9792a34" />

In development mode, only approved numbers can interact.

Steps:

```
WhatsApp → API Setup
↓
Add phone number
↓
Verify number
```

Now these users can interact with the bot.

# Step 5 - Backend Server Creation (FastAPI)

Created file:

```
whatsapp_server.py
```

This server performs:

* Webhook verification
* Message reception
* AI processing
* Reply sending

and then run the Server:

<img width="1920" height="1080" alt="Screenshot from 2026-02-18 23-01-42" src="https://github.com/user-attachments/assets/8efe9684-20cb-4fd0-971d-741f335c2afb" />

# Step 6 - Ollama LLM Integration

Installed Ollama:

```
curl -fsSL https://ollama.com/install.sh | sh
```

Pulled model:

```
ollama pull qwen3-vl:2b
```

Test:

```
ollama run qwen3-vl:2b
```

# Step 7 - Exposing Local Server to Internet

Meta requires public URL.

Localhost cannot be accessed.

Solution: Cloudflare Tunnel

Install:

```
sudo snap install cloudflared
```
<img width="1920" height="1080" alt="Screenshot from 2026-02-18 23-01-59" src="https://github.com/user-attachments/assets/c0f585cc-eb81-4d6f-a3e5-6a95ccc73080" />

Run tunnel:

```
cloudflared tunnel --url http://localhost:8000
```

Example generated URL:

```
https://hawk-lance-sufficiently-miss.trycloudflare.com
```

This forwards internet traffic to local server.

# Step 8 - Webhook Configuration

<img width="1920" height="1080" alt="step 8" src="https://github.com/user-attachments/assets/4928dadf-51f4-420b-9b18-001d104be69b" />

In Meta dashboard:

```
WhatsApp → Configuration
```

Enter:

Callback URL:

```
https://your-cloudflare-url/webhook
```

Verify Token:

```
guha_verify_token
```

Click:

```
Verify and Save
```

Webhook now connected.

# Step 9 - Enable Message Subscription

<img width="1920" height="1080" alt="step9" src="https://github.com/user-attachments/assets/24410196-851a-4a5b-8d9b-84827e06c838" />

Enable field:

```
messages
```

This allows Meta to send incoming messages to webhook.

# Step 10 - Message Processing Flow

Incoming message arrives as JSON:

```
POST /webhook
```

Backend extracts:

* Sender number
* Message text

Then:

```
Send to Ollama
Generate reply
Send reply using WhatsApp API
```

# Step 11 - Access Token Management

Temporary tokens expire.

Generate new token from:

```
WhatsApp → API Setup
```

Use permanent token for production.

# Step 12 - Running the System

Start backend:

```
uvicorn whatsapp_server:app --host 0.0.0.0 --port 8000
```

Start tunnel:

```
cloudflared tunnel --url http://localhost:8000
```

System ready.

# Step 13 - Full Execution Flow

1. User sends WhatsApp message
2. Meta receives message
3. Meta forwards to webhook
4. FastAPI receives message
5. FastAPI sends message to Ollama
6. Ollama generates reply
7. FastAPI sends reply via WhatsApp API
8. User receives reply

# Step 14 - Project Structure

```
NeuroCourier/
│
├── whatsapp_server.py
├── requirements.txt
├── README.md
```

# Step 15 - Commands Used

Start server:

```
uvicorn whatsapp_server:app --host 0.0.0.0 --port 8000
```

Start tunnel:

```
cloudflared tunnel --url http://localhost:8000
```

Pull model:

```
ollama pull qwen3-vl:2b
```

# Step 16 - Troubleshooting

## Token expired

Generate new access token.

## No webhook response

Ensure tunnel running.

## Webhook verification failed

Check verify token matches.

## No reply

Ensure:

* Access token valid
* messages subscription enabled

# Step 17 - Development vs Production Mode

Development mode:

* Only test users allowed

Production mode:

* Public users allowed
* Requires business verification

# Step 18 - Current Limitations

* Only test users can access
* Temporary access tokens expire
* Tunnel must remain active

# Step 19 - Future Improvements

* Permanent deployment
* Public WhatsApp access
* Database integration
* Conversation memory
* GPU acceleration

# Summary

We successfully built a complete WhatsApp AI chatbot using:

* Meta WhatsApp Cloud API
* FastAPI backend
* Cloudflare tunnel
* Ollama local LLM

This system allows WhatsApp users to interact with a locally running AI assistant securely and privately.

NeuroCourier now functions as a full AI messaging backend.
