import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect } from 'react-router-dom';
import MusicPlayer from './music' ;

export default function Homepage() {

    const [data, setData] = useState(null);
    const navigate = useNavigate();
    const [authenticateSpotify, setAuthenticateSpotify] = useState(false);
    const [spotifyUserData, setSpotifyUserData] = useState({});
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [song, setSong] = useState(null);

    const getCsrfToken = () => {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
        return cookie ? cookie.split('=')[1] : null;
    };

    const csrftoken = getCsrfToken();


    function timeSince(date) {
        const seconds = Math.floor((new Date() - date) / 1000);
        let interval = Math.floor(seconds / 31536000);

        if (interval > 1) {
            return interval + " years";
        }
        interval = Math.floor(seconds / 2592000);
        if (interval > 1) {
            return interval + " months";
        }
        interval = Math.floor(seconds / 86400);
        if (interval > 1) {
            return interval + " days";
        }
        interval = Math.floor(seconds / 3600);
        if (interval > 1) {
            return interval + " hours";
        }
        interval = Math.floor(seconds / 60);
        if (interval > 1) {
            return interval + " minutes";
        }
        return Math.floor(seconds) + " seconds";
    }

    function getUserProfile() {
        fetch("/spotify/user-profile")
            .then(response => {
                if (!response.ok) {
                    console.log('no user loged in');
                    return {}
                } else {
                    return response.json();
                }
            })
            .then(data => {
                setSpotifyUserData(data);
                localStorage.setItem('spotifyUserData', JSON.stringify(data));
            });
    };

    useEffect(() => {
        if (authenticateSpotify) {
            const storedUserData = localStorage.getItem('spotifyUserData');
            if (storedUserData) {
                setSpotifyUserData(JSON.parse(storedUserData));
            } else {
                getUserProfile();
            }
        }
    }, [authenticateSpotify]);


    const authenticate = useCallback(() => {
        fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
                window.location.replace(data.url);
            });;
    }, []);

    useEffect(() => {
        is_auth();
    }, []);

    function is_auth() {
        fetch("/spotify/is-authenticated")
            .then((response) => response.json())
            .then((data) => {
                setAuthenticateSpotify(data.status);
                console.log(data.status);
            })
    };

    useEffect(() => {
        fetch('/apis/room')
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`Server responded with status code ${response.status}`);
                }
            })
            .then(data => setData(data));
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/apis/in-room');
            if (response.ok) {
                const d = await response.json();
                if (d.message !== 'Room Not Found') {
                    console.log(d.code);
                    await navigate(`/room/${d.code}`);
                }
                else {
                    console.log(d.message);
                }
            } else {
                console.log('Error:', response.status, response.statusText);
            }
        }
        fetchData();
    }, []);

    const handleSubmit = useCallback((roomCode) => {

        fetch('/apis/join-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                code: roomCode,  // roomCode is the value of the input field, the key - value pair is code: roomCode, key should be similar to that of in the backend views.py
            })
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`Server responded with status code ${response.status}`);
            }
        }).then(data => {
            navigate(`/room/${roomCode}`);
        }).catch(error => {
            console.log(error);
            alert('Room not found or room expired');
        });
    }, [csrftoken]);

    return (
        <>
            {window.innerWidth > 640 ? (
                <nav className="flex font-bold py-2 text-xl w-screen justify-evenly shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white">
                    {authenticateSpotify ? (
                        <div className="bg-black bg-opacity-100 rounded p-1">
                        <p className="text-xl font-semibold text-green-500">Hi, {spotifyUserData.display_name}</p>
                        </div>
                    ) : (
                        <Link onClick={authenticate}>Login</Link>
                    )}
                    {authenticateSpotify && (<Link to="/profile">Profile</Link>)}
                    {authenticateSpotify && (<Link to="/create">Create Room</Link>)}
                    {authenticateSpotify && (<Link to="/join">Join Room</Link>)}
                </nav>
            ) : (
                <>
                    <div className={`fixed inset-0 z-50 h-full transition-transform duration-200 transform ${sidebarOpen ? 'block' : 'hidden'} sm:hidden`} onClick={() => setSidebarOpen(false)}>
                        <nav style={{ width: '50vw' }} className={`fixed bg-opacity-80 inset-y-0 h-full left-0 z-30 w-64 px- pt-5 pb-4 bg-sky-700 text-white transition-transform duration-200 transform overflow-y-auto ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 md:static md:inset-0 md:overflow-visible sm:hidden`}>
                            <div className="flex items-center justify-center px-4 md:hidden">
                                <button className="p-1 rounded-md focus:outline-none focus:ring-2 focus:ring-white" onClick={() => setSidebarOpen(false)}>
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                                    </svg>
                                </button>
                            </div>
                            <div class="flex flex-col items-center justify-center mt-5">
                                {authenticateSpotify ? (
                                    <></>
                                ) : (
                                    <Link className="text-lg font-medium text-center hover:underline px-2 py-2 w-4/5 rounded-full bg-sky-800 hover:bg-gray-300" onClick={authenticate}>Login</Link>
                                )}
                                {authenticateSpotify &&
                                    <Link className="mt-2 text-lg text-center font-medium hover:underline px-2 py-2 w-4/5 rounded-full bg-sky-800 hover:bg-gray-300" to="/profile">Profile</Link>
                                }
                                {authenticateSpotify &&
                                    <Link className="mt-2 text-lg text-center font-medium hover:underline px-2 py-2 w-4/5 rounded-full bg-sky-800 hover:bg-gray-300" to="/create">Create Room</Link>
                                }
                                {authenticateSpotify &&
                                    <Link className="mt-2 text-lg text-center font-medium hover:underline px-2 py-2 w-4/5 rounded-full bg-sky-800 hover:bg-gray-300" to="/join">Join Room</Link>
                                }
                            </div>
                        </nav>
                    </div>
                    <div className="sm:hidden">
                        <button className="p-1 sticky rounded-md focus:outline-none focus:ring-2 focus:ring-white" onClick={() => setSidebarOpen(true)}>
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                            </svg>
                        </button>
                    </div>
                    {authenticateSpotify ? (<div className="bg-black bg-opacity-100 rounded p-2 mx-auto w-fit">
                                    <p className=" text-xl font-bold text-green-500">Hi, {spotifyUserData.display_name}</p>
                                    </div>) : (<></>)}
                </>
            )}
            
            <div className='mx-8 flex gap-2 flex-col sm:flex-row '>
                <div className="md:flex-grow">
                <div className='mx-auto my-2 mt-5 w-fit h-fit bg-opacity-80 rounded-md shadow-lg'> 
                <MusicPlayer song={song} setSong={setSong} />
                </div>
                </div>
                <div className='mx-2 my-2 mt-5 sm:w-1/3 md:w-1/3 h-auto max-h-[calc(90vh-64px)] overflow-x-hidden overflow-y-auto bg-opacity-60 rounded-md shadow-lg scrollbar-hide'>
                    <div className='sticky top-0 z-10 text-center shadow-sm bg-gradient-to-b from-sky-300 to-sky-600 text-white text-2xl py-2 px-4 font-bold'>Rooms</div>
                    <div className='flex flex-col z-neg-1 gap-4 p-4'>
                        {data && data.map((item, index) => (
                            <div className='border-solid border-2 border-slate-200 bg-opacity-90 shadow-md rounded-md p-1' style={{ backgroundImage: `url(${item.playlist_cover})`, backgroundSize: 'cover', backdropFilter: 'blur(10px)' }}>
                                <div>
                                    <h3 className='leading-loose border-b-2 border-solid border-gray-300 shadow-sm text-center font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 text-lg'>{item.name}</h3>
                                    <p className='text-sm leading-loose text-gray-500 font-italic text-center'>{
                                        timeSince(new Date(item.created_time))
                                    } ago
                                    </p>
                                    {item.is_public ? (<div className="text-green-500 leading-loose text-center">Public</div>) : (<div className="text-red-500 leading-loose text-center">Private</div>)}
                                </div>
                                {item.is_public && <button onClick={(event) => {
                                    event.preventDefault();
                                    handleSubmit(item.code);
                                }} className="btn w-full font-bold float-right bg-gradient-to-r from-green-300 to-green-600 text-white px-2 py-1 rounded-md">JOIN</button>}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}