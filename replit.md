# Reddit Scraper Application

## Overview

This is a Reddit scraping application built with Streamlit that allows users to extract and export subreddit posts with filtering options. The application provides a web-based interface for scraping Reddit data using the PRAW (Python Reddit API Wrapper) library and presents the results in a user-friendly dashboard.

## User Preferences

Preferred communication style: Simple, everyday language.
Language: Turkish (Türkçe) - User prefers responses in Turkish.
GitHub Integration: User wants to upload project to GitHub with proper documentation.

## System Architecture

The application follows a simple two-tier architecture:

### Frontend Layer
- **Streamlit Web Application**: Provides an interactive web interface for user input and data visualization
- **Session State Management**: Maintains application state across user interactions
- **Real-time Updates**: Live feedback during scraping operations

### Backend Layer
- **Reddit API Integration**: Uses PRAW library for authenticated Reddit API access
- **Data Processing**: Pandas for data manipulation and export functionality
- **Error Handling**: Graceful degradation when API credentials are unavailable

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Primary Streamlit application entry point
- **Features**:
  - Page configuration and layout setup
  - Session state initialization for scraper instance and data
  - User interface components (sidebar configuration, main dashboard)
  - Input handling for subreddit selection and filtering options

### 2. Reddit Scraper Module (reddit_scraper.py)
- **Purpose**: Core scraping functionality and Reddit API interaction
- **Features**:
  - Reddit client initialization with environment variable configuration
  - API status checking and connection validation
  - Fallback mechanisms for demo mode when credentials are unavailable
  - Data extraction and processing methods

### 3. Configuration Management
- **Environment Variables**: API credentials stored securely outside codebase
- **Fallback Values**: Default values for development and demo purposes
- **User Agent Configuration**: Proper API identification for Reddit compliance

## Data Flow

1. **User Input**: User configures scraping parameters via Streamlit sidebar
2. **API Connection**: Application establishes connection to Reddit API using PRAW
3. **Data Extraction**: Scraper retrieves posts based on user-specified filters
4. **Data Processing**: Raw Reddit data is cleaned and structured using Pandas
5. **Data Presentation**: Results displayed in Streamlit interface with export options
6. **Session Persistence**: Scraped data maintained in session state for user interaction

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **PRAW (Python Reddit API Wrapper)**: Official Reddit API client
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP library for API communications

### Reddit API Integration
- **Authentication**: OAuth2-based authentication using client credentials
- **Rate Limiting**: Built-in PRAW rate limiting compliance
- **API Endpoints**: Access to subreddit posts, comments, and metadata

### Environment Configuration
- **REDDIT_CLIENT_ID**: Reddit application client identifier
- **REDDIT_CLIENT_SECRET**: Reddit application secret key
- **REDDIT_USER_AGENT**: Application identification string for Reddit API

## Deployment Strategy

### Development Environment
- **Local Development**: Direct execution with environment variables
- **Dependency Management**: Requirements file for package installation
- **Configuration**: Environment-based credential management

### Production Considerations
- **Environment Variables**: Secure credential storage
- **Error Handling**: Graceful degradation for missing credentials
- **Rate Limiting**: Compliance with Reddit API usage policies
- **Data Export**: File download capabilities for extracted data

### Architecture Benefits
- **Separation of Concerns**: Clear division between UI and scraping logic
- **Scalability**: Modular design allows for easy feature additions
- **Security**: Credential isolation through environment variables
- **User Experience**: Interactive web interface with real-time feedback
- **Flexibility**: Support for multiple post types and filtering options

### Future Enhancements
- **Database Integration**: Potential for data persistence using SQL databases
- **Advanced Filtering**: Additional post filtering and search capabilities
- **Batch Processing**: Support for multiple subreddit scraping
- **Data Visualization**: Enhanced charts and analytics features