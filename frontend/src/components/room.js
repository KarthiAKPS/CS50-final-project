import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect, useParams } from 'react-router-dom';
import CreateRoom from "./CreateRoom";
import MusicPlayer from './music';


export default function Room() {

    const [roomData, setRoomData] = useState({});
    const { roomCode } = useParams();
    const [roomFound, setRoomFound] = useState(true);
    const navigate = useNavigate();
    const [settingsShow, setSettingsShow] = useState(false);
    const [loading, setLoading] = useState(false);
    const [showInfo, toggleInfo] = useState(false);
    const [authenticateSpotify, setAuthenticateSpotify] = useState(false);

    /**
    * Retrieves the CSRF token from the document cookie.
    * @returns {string|null} The CSRF token or null if not found.
    */
    const getCsrfToken = () => {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
        return cookie ? cookie.split('=')[1] : null;
    };

    const csrftoken = getCsrfToken();

    /* useEffect: This hook is used to perform side effects in function components. Side effects could be data fetching, subscriptions, or manually changing the DOM, among other things. In class components, you would typically use lifecycle methods like componentDidMount, componentDidUpdate, and componentWillUnmount for this, but in functional components, you can use useEffect. */
    useEffect(() => {
        setLoading(true);
        fetch('/apis/get-room' + '?code=' + roomCode)
            .then(response => {
                if (!response.ok) {
                    navigate('/');
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // const room = data.find(room => room.code === roomCode);
                if (data.code === roomCode) {
                    setRoomData(data);
                    console.log(data);
                    setLoading(false);
                } else {
                    setRoomFound(false);
                    console.log(`Room with code ${roomCode} not found`);
                    setLoading(false);
                }
            })
            .catch(error => console.log('Fetch error: ', error));
        authenticate();
    }, [roomCode]);

    const authenticate = () => {
        fetch("/spotify/is-authenticated")
            .then((response) => response.json())
            .then((data) => {
                setAuthenticateSpotify(data.status);
                console.log(data.status);
                if (!data.status) {
                    fetch("/spotify/get-auth-url")
                        .then((response) => response.json())
                        .then((data) => {
                            window.location.replace(data.url);
                        });
                }
            });
    }

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
        if(!authenticateSpotify) {
            authenticate();
        }
    },[]);

    const leaveButton = (event) => {
        event.preventDefault();
        fetch('/apis/leave-room', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        }).then((_response) => {
            navigate('/');
        });
    };


    return (
        <>
            {settingsShow ? (
                <CreateRoom updateRoomData={setRoomData} settingsShow={settingsShow} setSettingsShow={setSettingsShow} votesToSkipProp={roomData.votes_to_skip} name={roomData.name} guestCanPauseState={roomData.guest_can_pause} isPublicState={roomData.isPublic} codeState={roomData.code} />
            ) : (
                <> {!loading ? (
                    <div class="relative">
                        {roomData.is_creator ? (
                            <div className='flex w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white items-center justify-between'>
                                <div className="ml-4 font-bold">{roomData.code}</div>
                                <Link className='px-2 py-1' onClick={() => setSettingsShow(true)}>
                                    <i class="fa-solid fa-pen-to-square"></i>
                                </Link>
                            </div>
                        ) : (
                            <></>
                        )}
                        {roomFound ? (
                            <>
                                <div className="flex flex-col">
                                    <div className="mt-4 flex flex-row w-full items-center justify-center gap-2">
                                        <img src={roomData.playlist_cover} alt="Room cover" className="rounded-full w-32 h-32 object-cover" />
                                        <div class="flex flex-col items-center justify-evenly gap-2">
                                            <h1 className="font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 text-lg">{roomData.name}</h1>
                                            <div className="flex">
                                                <button className="font-bold w-fit h-fit bg-red-500 text-white px-2 py-1 rounded-md active:bg-red-700 hover:shadow-lg" onClick={leaveButton}>
                                                    {roomData.is_creator ? 'CLOSE' : 'LEAVE'}
                                                </button>
                                            </div>
                                            <i className="fa-solid fa-info-circle cursor-pointer" onClick={() => toggleInfo(!showInfo)}></i>
                                        </div>
                                    </div>
                                    <div className=' my-2 h-32 fixed bottom-0 left-1/2 transform -translate-x-1/2 w-auto bg-opacity-80 rounded-md shadow-lg'><MusicPlayer /></div>
                                    <div className="fixed bottom-0 left-0 right-0 mb-4 z-neg-1 flex items-center justify-center">
                                        {showInfo ? (
                                            <div className="inline-flex w-3/4 flex-col ml-4 bg-yellow-50 p-4 border-l-4 border-yellow-500 text-gray-700 rounded transition-all duration-500 ease-in-out transform opacity-100">
                                                <p className="mb-2 border-b pb-2"><span className="font-bold">Votes Needed to Skip:</span> {roomData.votes_to_skip}</p>
                                                <p className="border-b pb-2 font-bold text-green-500"> {roomData.guest_can_pause ? 'Guest Allowed to Pause' : ''}</p>
                                            </div>) : (
                                            <div className="inline-flex w-3/4 flex-col ml-4 bg-yellow-50 p-4 border-l-4 border-yellow-500 text-gray-700 rounded transition-all duration-500 ease-in-out transform opacity-0">
                                                <p className="mb-2 border-b pb-2"><span className="font-bold">Votes Needed to Skip:</span> {roomData.votes_to_skip}</p>
                                                <p className="border-b pb-2 font-bold text-green-500"> {roomData.guest_can_pause ? 'Guest Allowed to Pause' : ''}</p>
                                            </div>
                                        )}
                                    </div>
                                </div>
                                
                            </>
                        ) : (
                            <>
                                {setRoomFound(false)}
                                <p>Room with code {roomCode} not found</p>
                            </>
                        )}
                    </div>
                ) : (<div>loading....</div>)}
                </>
            )
            }
        </>
    )
}
