# StudyLink

StudyLink is a platform designed for tech students to share and discover study materials, connect with peers in the same courses, and integrate with social media profiles and GitHub, fostering a collaborative learning community.

## Features

- **Resource Sharing**: Users can upload and share study materials such as notes, tutorials, and videos.
- **Peer Connections**: Connect with peers who are studying the same courses to discuss and collaborate.
- **Social Integration**: Follow and connect with peers' social media profiles and GitHub accounts directly from the platform.
- **User Profiles**: Customize profiles with personal information, including websites, Twitter handles, and GitHub usernames.
- **Review and Comment**: Users can leave reviews and comments on shared resources, facilitating feedback and discussion.
- **Save Resources**: Bookmark resources for later reference.

## Technologies Used

- **Flask**: Web framework used for backend development.
- **SQLAlchemy**: ORM (Object-Relational Mapping) used for database management.
- **Flask-Login**: Provides user session management and authentication.
- **Flask-Bcrypt**: Used for hashing passwords securely.
- **Flask-Migrate**: Facilitates database migrations.
- **Flask-Moment**: Provides support for displaying timestamps.
- **Google YouTube API**: Used for fetching video details from YouTube URLs.
- **Bootstrap**: Frontend framework for responsive design.
- **HTML/CSS**: Used for frontend development and styling.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd StudyLink

   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
    pip install -r requirements.txt
   ```  

4. Set up environment variables:
Create a .env file in the root directory with the following variables:
   ```
    SECRET_KEY=your_secret_key_here
    DATABASE_URI=your_database_uri_here
    YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

5. Initialize the database:
   ```
    flask db upgrade
   ```

6. Run the application:
   ```
    flask run
   ```  

7. Access the application in your web browser at `http://localhost:5000`.

## Usage

  <ul>
    <li><strong>Register</strong>: Create a new account to start using StudyLink.</li>
    <li><strong>Login</strong>: Log in with your credentials to access your personalized dashboard.</li>
    <li><strong>Explore</strong>: Discover study materials shared by others or connect with peers.</li>
    <li><strong>Upload</strong>: Share your study resources or save resources for future reference.</li>
    <li><strong>Interact</strong>: Leave reviews, comments, and follow peers' social profiles.</li>
    <li><strong>Edit Profile</strong>: Customize your profile with additional information.</li>
  </ul>


## Contributing
   ```
    Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
   ```
