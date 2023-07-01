#!/bin/bash

# Script for local test of the youtube review script. Make sure that the .env file contains the correct values (valid API key with available quote and valid channel ID)

env $(cat .env) python youtube_get_reviews.py