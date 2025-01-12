# LLM CTF Evaluation Framework

## Overview
This project aims to evaluate Language Learning Models' (LLMs) capabilities in solving Capture The Flag (CTF) security challenges. By systematically testing different models against security tasks, we can better understand their potential in security testing and vulnerability discovery.

## Project Goals

### Primary Objectives
1. Evaluate LLMs' ability to:
   - Identify security vulnerabilities
   - Develop exploitation strategies
   - Execute successful attacks
   - Learn from failed attempts

2. Compare performance across:
   - Different LLM models
   - Various prompting strategies
   - Different types of security challenges

3. Collect meaningful metrics on:
   - Success rates
   - Time to solution
   - Resource utilization (tokens/cost)
   - Strategy effectiveness

## System Architecture

### Core Components

1. **Target Environment**
   - Vulnerable applications for testing
   - Containerized for isolation and reproducibility
   - Configurable difficulty levels
   - Current implementation: Simple Flask app with SQL injection vulnerability

2. **Agent System**
   - LLM integration via LiteLLM
   - Action execution capabilities
   - Memory and context management
   - Strategy development and execution

3. **Evaluation Framework**
   - Metrics collection
   - Performance logging
   - Results analysis
   - Cross-model comparison

## Current Basic Implementation

### Vulnerable Application -login app (Done)
- Flask-based web application
- Simple login endpoint
- Known SQL injection vulnerability
- Docker containerization for easy deployment

### Testing Agent (To Do)
- Model-agnostic design (using LiteLLM)
- Iterative attack strategy
- Built-in logging and metrics
- Thought process documentation

## Metrics and Evaluation

### Key Metrics
1. Success Rate
   - Percentage of successful exploits
   - Number of attempts needed

2. Efficiency
   - Time to solution
   - Token usage
   - Number of API calls

3. Strategy Analysis
   - Types of attempts made
   - Learning pattern
   - Adaptation to failed attempts


