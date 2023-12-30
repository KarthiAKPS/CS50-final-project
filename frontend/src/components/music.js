import React, { useState, useEffect } from 'react';
import { render } from 'react-dom';

export default function MusicPlayer(authenticate) {
    const [auth, setAuth] = useState(authenticate)
    const [song, setSong] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const togglePlayPause = () => {
        setIsPlaying(!isPlaying);
    };

    const handleProgressChange = (event) => {
        setProgress(event.target.value);
    };

    const pauseSong = () => {
        togglePlayPause();
        console.log('pause clicked!')
        fetch("/spotify/pause", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
          }).catch(error => {
            console.log(error);
            alert('You cannot pause');
        });
      };
    
    const playSong = () => {
        togglePlayPause();
        console.log('play clicked!')
        fetch("/spotify/play", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
            }).catch(error => {
                console.log(error);
                alert('You cannot play');
        });
    };

    useEffect(() => {
        const fetchSong = () => {
            if (auth) {
                fetch('/spotify/current-song')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.text();
                    })
                    .then(data => {
                        if (data) {
                            const jsonData = JSON.parse(data);
                            setSong(jsonData);
                            setIsPlaying(jsonData.is_playing);
                            console.log(jsonData);
                        }
                    })
                    .catch(error => {
                        console.error('There was an error!', error);
                    });
            };
        };

        // Call fetchSong immediately
        if (auth) {
            fetchSong();

            // Then call fetchSong every second
            const intervalId = setInterval(fetchSong, 1000);

            // Clear interval on component unmount
            return () => clearInterval(intervalId);
        }
    }, [auth]);


    return (
        <>
            {song ? (
                <>
                    <div className="flex items-center justify-between p-2">
                        <div className="relative">
                            <img src={song.image_url} alt="Album cover" className="rounded-full w-28 h-28 object-cover" />
                            <div className="absolute bg-opacity-50 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white w-8 h-8 rounded-full p-1">
                                <button onClick={() => {isPlaying ? pauseSong() : playSong()}} className="text-2xl text-black hover:text-gray-900 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 hover:cursor-pointer pointer-events-auto z-40">
                                    {isPlaying ? <i class="fa-solid fa-pause"></i> : (<i class="fa-solid fa-play"></i>)}
                                </button>
                            </div>
                        </div>
                        <div className="flex flex-col flex-grow items-center justify-center gap-2 ml-4">
                            <div className='font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 text-lg'>{song.title}</div>
                            <div className="text-sm">{song.artist}</div>
                            <input type="range" min="0" max="100" value={song.time / song.duration * 100} onChange={handleProgressChange} className="appearance-none w-full h-2 rounded-full bg-gray-200 outline-none"
                                style={{
                                    background: `linear-gradient(to right, #1DB954 0%, #1DB954 ${song.time / song.duration * 100}%, #808080 ${song.time / song.duration * 100}%, gray-200 100%)`
                                }} />
                        </div>
                    </div>
                </>
            ) : (
                <div className='text-center text-gray-500'>Currently no songs are playing...</div>
            )}</>
    );
}