import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';

export default function Profile() {

    const [userdata, setuserData] = useState({});
    const [playlists, setPlaylists] = useState([]);

    useEffect(() => {
        fetch('/spotify/user-profile')
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`Server responded with status code ${response.status}`);
                }
            })
            .then(data => {
                setuserData(data)
                console.log(userdata)
            });

        fetch('/spotify/playlists')
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`Server responded with status code ${response.status}`);
                }
            })
            .then(data => {
                setPlaylists(data.items);
            })
            .catch(error => {
                console.error('Error fetching playlists', error);
            });
    }, []);

    return (
        <>
            <div className="flex flex-wrap justify-between w-full px-8 py-2 bg-gradient-to-b from-sky-300 to-sky-600 text-white">
                <h1 className="text-2xl font-bold">Profile</h1>
                <Link className="px-2 py-1" to="/"><i className="fa-solid fa-house"></i></Link>
            </div>
            <div className="flex flex-col h-screen md:h-auto md:flex-row justify-between">
                <div className="flex flex-col md:flex-row flex-grow overflow-auto">
                    <div className="flex flex-col w-full md:w-1/2 p-4">
                        <div className="flex flex-col items-center justify-center bg-white p-8 rounded-lg shadow-lg mb-4">
                            {userdata.image &&
                                <img className="w-32 h-32 rounded-full mb-4" src={userdata.image} alt="Profile" />}
                            <h2 className="text-2xl font-bold mb-2">{userdata.display_name}</h2>
                            <p className="text-gray-500">Followers: {userdata.followers}</p>
                        </div>
                        <div className="flex flex-col items-center justify-center bg-white p-8 rounded-lg">
                            <div className="w-full">
                                <div className="flex h-2 rounded overflow-hidden bg-gray-200">
                                    {/*to be added in the future */}
                                    <div style={{ width: `${(userdata.likes / (userdata.likes + userdata.dislikes)) * 100}%` }} className="bg-green-500"></div> 
                                    <div style={{ width: `${(userdata.dislikes / (userdata.likes + userdata.dislikes)) * 100}%` }} className="bg-red-500"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col w-full md:w-1/2 p-4">
                        <div className="flex flex-col items-center justify-center bg-white p-4 rounded-lg shadow-lg mb-2">
                            <h2 className="text-2xl font-bold mb-2">Playlists</h2>
                            <div className="grid md:grid-cols-2 gap-4 md:gap-8 overflow-auto sm:overflow-visible h-auto sm:max-h-[calc(65vh-64px)] md:my-8">
                                {playlists.map(playlist => (
                                    <div key={playlist.id} className="mb-4 bg-white rounded-lg shadow-md">
                                        <div className="p-4">
                                            <h3 className="text-xl font-bold">{playlist.name}</h3>
                                            <p className="text-gray-500">{playlist.description}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                    </div>
                    </div>
                </>);
}