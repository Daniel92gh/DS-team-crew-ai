# 🤖 CrewAI Data Science Team

A multi-agent data science workflow automation system using CrewAI that performs end-to-end regression analysis with intelligent code generation and execution.

## 📋 Overview

This project demonstrates an automated data science pipeline where AI agents collaborate to perform regression analysis on supplement sales data. The system uses CrewAI to orchestrate three specialized agents that plan, preprocess, and model data autonomously by generating and executing Python code.

## ✨ Features

- 🤝 **Multi-Agent Collaboration**: Three specialized AI agents working together
- 🔄 **Automated Code Generation**: Agents write and execute Python code dynamically
- 🚀 **End-to-End ML Pipeline**: From data inspection to model evaluation
- 🧠 **Intelligent Planning**: Strategic approach to regression analysis
- ⚡ **Real-time Execution**: Code execution with immediate feedback
- 📊 **Comprehensive Evaluation**: Multiple regression metrics and feature importance analysis

## 🏗️ Architecture

### 🤖 Agents

#### 1. **Lead Data Scientist and Planner**
- Creates strategic plan for regression analysis
- Defines objectives for each pipeline step
- Coordinates overall workflow

#### 2. **Data Analysis and Preprocessing Expert**
- Performs data inspection and cleaning
- Handles feature engineering and encoding
- Creates train/test splits
- Uses NotebookCodeExecutor tool

#### 3. **Machine Learning Modeler and Evaluator**
- Trains RandomForest regression model
- Evaluates model performance
- Analyzes feature importance
- Uses NotebookCodeExecutor tool

### 🔄 Workflow

```mermaid
graph LR
    A[Planning] --> B[Data Analysis & Preprocessing]
    B --> C[Modeling & Evaluation]
 
## ✨ Installation  
```bash
uv add  crewai langchain-openai pandas scikit-learn python-dotenv ipython


## ⚙️ Setup 

### 1. **Create environment file**
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

### 2. **Prepare data file**
Ensure Supplement_Sales_Weekly.csv is in the project directory

### 3. **Required modules**
Make sure you have the notebookExecutor.py module available


## 🔄 Automated Process

The system will automatically:

1. 📊 Load and inspect the supplement sales data
2. 🔧 Preprocess features (date handling, encoding, splitting)
3. 🤖 Train a RandomForest regression model
4. 📈 Evaluate performance with multiple metrics
5. 🏆 Display feature importance rankings
