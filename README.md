# MUSIX MATCH

## Music Streaming Social Web Application

### Overview

The project is a music collaboration social media application built on Django, utilizing the Spotify API. Users can log in with their Spotify accounts, create and join rooms, and collaborate on music playback.

This project is designed to foster collaboration and create a vibrant community of music lovers. Here's what makes it fun:

- **Spotify Integration:** Users can connect their Spotify accounts, enabling them to play and share songs within the application.

- **Room Creation and Joining:** Users can create public or private rooms, each with a unique room code. Public rooms can be discovered in a dedicated section, while private rooms require a specific code for access.

- **Voting System:** Participants in a room can vote to skip the currently playing song. If the required votes are met, the song changes.

- **Premium Features:** Certain functionalities, such as joining spotify play-pause, may require a Spotify Premium account.

## File Structure

Briefly describe the purpose of each major file in your project.

- **`/backend`**: Django backend code and configurations.
- **`/frontend`**: React frontend code for the user interface.
- **`/static`**: Static files such as CSS, JavaScript, and images.
- **`/templates`**: HTML templates for rendering views.

### Complexity

The project distinguishes itself by:

- **Social Collaboration:** Fosters collaboration among users by allowing them to create and join rooms for shared music experiences.

- **Spotify API Integration:** Leverages the Spotify API to access user playlists, play songs, and enable a seamless music-sharing experience.

- **Voting System:** Implements a voting system for song skipping, enhancing user interaction and control over the collaborative playlist.

- **Room Privacy Settings:** Provides flexibility with public and private room options, enhancing user control over their collaborative spaces.

## Python Packages

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

and require other packages like django djangorestframework dj-database-url django-browser-reload python-dotenv jinja2 gunicorn Pillow psycopg2

### How to Run

Follow these steps to run the application:

- Clone the repository: git clone `https://github.com/yourusername/your-repo.git`
- Navigate to the project directory: cd your-repo
- Create a virtual environment (optional but recommended): python -m venv venv
- Activate the virtual environment:
- On Windows: venv\Scripts\activate
- On Unix or MacOS: source venv/bin/activate
- Install dependencies: pip install -r requirements.txt
- Run migrations: python manage.py migrate
- Start the development server: python manage.py runserver
- Open your web browser and go to `http://localhost:8000`

Additional Instructions:
Spotify API Credentials:
Obtain your Spotify API credentials by creating a Spotify Developer account.
Create a .env file in the project root and add the following variables:

```bash
#.env

SPOTIFY_CLIENT_ID = your-client-id
SPOTIFY_CLIENT_SECRET = your-client-secret
REDIRECT_URI = "http://localhost:8000/spotify/redirect"
```

## Spotify API Credentials

- Obtain your Spotify API credentials by creating a Spotify Developer account.
- Create a .env file in the project root and add your Spotify API credentials.
- Make sure to replace redirect-uri, your-client-id, and your-client-secret with your actual redirect-uri and Spotify API credentials.

## Spotify Authentication Process and API Calls

Here's a visual representation of the Spotify authentication process and API calls:

![Spotify Authentication Process](https://example.com/path/to/spotify_auth_process.png)

For more detailed information about Spotify APIs, you can refer to the official Spotify documentation:

- [Spotify Authorization Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
- [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api/reference/)
- [Spotify Web API Tutorials](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)

## Code

### Backend API handling ( main app )

#### models

- The *RoomCode* function generates unique room codes.
- The *get_default_playlist* function provides a default playlist.
- The *User* model extends the default Django AbstractUser.
- The *RoomPrivate* model defines the structure for private rooms.

#### serializer

- **RoomSerializer** serializes RoomPrivate model instances.
- **CreateRoomSerializer** is used for creating new rooms.
- **EditRoomSerializer** is used for editing existing rooms.

#### urls

- `/room` maps to the RoomView class-based view.
- `/create-room` maps to the CreateRoomView class-based view.
- `/get-room` maps to the GetRoom class-based view.
- `/join-room` maps to the JoinRoom class-based view.
- `/in-room` maps to the InRoom class-based view.
- `/leave-room` maps to the LeaveRoom class-based view.
- `/edit-room` maps to the EditRoom class-based view.

#### views

- The **GetRoom** class-based view retrieves details about a specific private room based on the provided room code.
- The **CreateRoomView** class-based view handles the creation of a new private room.
-The **InRoom** class-based view checks if the user is in a room and returns the room code.
- The **JoinRoom** class-based view handles user joining a private room.
- The **LeaveRoom** class-based view handles a user leaving a private room.
- The **EditRoom** class-based view handles editing details of a private room.

### Spotify API handling ( spotify app )

#### Get Authentication URL

Endpoint: `/get-auth-url`
View: AuthURL.as_view()
Purpose: Generates the Spotify authentication URL.

#### Spotify Callback

Endpoint: `/redirect`
View: spotify_callback
Purpose: Handles the callback from Spotify, retrieves tokens, and updates or creates user tokens.

#### Check Authentication Status

Endpoint: `/is-authenticated`
View: IsAuthenticated.as_view()
Purpose: Checks if the Spotify user is authenticated.

#### Get Current Song

Endpoint: `/current-song`
View: CurrentSong.as_view()
Purpose: Retrieves information about the current song being played.

#### Get User Profile

Endpoint: `/user-profile`
View: UserProfile.as_view()
Purpose: Retrieves information about the Spotify user's profile.

#### Pause Song

Endpoint: `/pause`
View: PauseSong.as_view()
Purpose: Pauses the currently playing song.

#### Play Song

Endpoint: `/play`
View: PlaySong.as_view()
Purpose: Resumes or plays the currently selected song.

#### Skip Song

Endpoint: `/skip`
View: SkipSong.as_view()
Purpose: Skips the currently playing song.

#### Get Playlists

Endpoint: `/playlists`
View: Playlist.as_view()
Purpose: Retrieves a list of Spotify playlists for the authenticated user.

#### Play Playlist

Endpoint: `/play/<playlist_id>`
View: PlayPlaylist.as_view()
Purpose: Plays a specific Spotify playlist.

### Frontend UI using ReactJS ( frontend app )

#### Views

- `index`: Renders the main index page.

#### URLs

- `/`: Renders the main index page.
- `/join/`: Renders the join page.
- `/profile/`: Renders the user profile page.
- `/room/<str:roomCode>`: Renders a specific room page.
- `/create/`: Renders the create room page.

#### Components

- `Room`: Renders a room page.
- `JoinRoom`: Renders the join room page.
- `CreateRoom`: Renders the create room page.
- `Profile`: Renders the user profile page.
- `MusicPlayer`: Renders the music player component.
- `HomePage`: Renders the main index page.

## Key Components used in room.js for example

### State Variables

- roomData: Holds information about the current room, fetched from the server.
- roomCode: Extracted from the URL parameters using useParams() from React Router.
- roomFound: Indicates whether the room with the specified code was found.
- settingsShow: Manages the visibility of the settings for creating/editing a room.
- loading: Indicates whether data is still being fetched.
- showInfo: Toggles the display of additional information about the room.

### Effect Hooks

#### Initial Fetch

- Uses useEffect to fetch room data when the component mounts or when roomCode changes.
- Navigates to the home page if the room is not found.

#### Playlists Fetch

Fetches playlists from the server using the Spotify API.

#### CSRF Token

Uses a function (getCsrfToken) to retrieve the CSRF token from the document cookie.

#### Leave Room Function

Sends a POST request to leave the current room.

#### Start Playing Function

Sends a POST request to start playing a selected playlist.

#### Conditional Rendering

Renders different components based on whether the settings are shown or if the room is still loading.

#### MusicPlayer Component

Renders a MusicPlayer component, passing the song state and a function to set the song.

#### Conditional Styles

Uses conditional rendering to show/hide and style elements based on certain conditions.

#### Spotify Authentication

There are commented-out sections related to Spotify authentication. It seems like authentication is part of the functionality, but some parts are currently commented out.

#### Additional Information

Displays additional information about the room, such as votes needed to skip and whether guests are allowed to pause.

## Future Plans

As the project evolves, the following features are planned for implementation:

### Continuous Music Playback

Random songs from other users' playlists will be played continuously for the logged-in user, creating a dynamic and engaging music streaming experience.

### Like System

Users can like songs, earning points for the playlist owner. The next song from the same playlist will be played until a dislike is registered.

### Like-to-Dislike Ratio

Display the like-to-dislike ratio of the user's playlist songs as a percentage in the user's profile.

### Leaderboard

Introduce a leaderboard showcasing users based on their percentage of likes, fostering healthy competition among the community.

### Daily Votes

Implement a daily voting system to determine whose playlist will be streamed in a room. Users can cast votes based on the like-dislike concept mentioned above, with the winner changing daily.

### Playlist Voting

Select two playlists for votes in the room, while the previously selected playlist plays. The community decides which playlists will be featured next.

## Additional Notes on Production and Deployment

In addition to the core functionality, the project includes code snippets related to production and deployment. These snippets may include settings for production databases, static file serving, and other considerations that are not necessary for local development.

If you are running the project locally, you can safely ignore these snippets. However, if you plan to deploy the project in a production environment, please carefully review and configure these settings according to your deployment platform.

## Tutorials

For developers interested in the technologies used in this project, here are some helpful tutorials:

### Django Tailwind

[Django Tailwind Documentation](https://django-tailwind.readthedocs.io/en/latest/installation.html)

Learn how to integrate Tailwind CSS with Django using the `django-tailwind` package. Tailwind provides a utility-first CSS framework for building modern and responsive user interfaces.

### React on Django Projects

[Using React with Django](https://www.digitalocean.com/community/tutorial_series/build-a-to-do-application-with-django-and-react)
