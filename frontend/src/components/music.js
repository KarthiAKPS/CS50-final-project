import React, { useState, useEffect } from 'react';

export default function MusicPlayer() {
    const [song, setSong] = useState(null);

    useEffect(() => {
        fetch('/spotify/current-song')
            .then(response => {
                setSong(response.data);
                console.log(response.data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    return (
        <div className='mx-auto my-2 mt-5 h-fit md:flex-grow bg-opacity-60 rounded-md shadow-lg'>
            {song && (
                <>
                    <img src={song.image_url} alt="Album cover" className="rounded-full w-32 h-32 object-cover" />
                    <div className="flex flex-col items-center justify-evenly gap-2">
                        <h1 className="font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 text-lg">this song is{song.title}</h1>
                        <p className="text-sm">{song.artist}</p>
                        <audio controls>
                            <source src={song.id} type="audio/mpeg">
                            Your browser does not support the audio element.
                            </source>
                        </audio>
                    </div>
                </>
            )}
        </div>
    );
}