import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect, useParams } from 'react-router-dom';
import CreateRoom from "./CreateRoom";


export default function Room() {

    const [roomData, setRoomData] = useState({});
    const { roomCode } = useParams();
    const [roomFound, setRoomFound] = useState(true);
    const navigate = useNavigate();
    const [settingsShow, setSettingsShow] = useState(false);

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
                } else {
                    setRoomFound(false);
                    console.log(`Room with code ${roomCode} not found`);
                }
            })
            .catch(error => console.log('Fetch error: ', error));
    }, [roomCode]);

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
            <CreateRoom update={true} settingsShow={settingsShow} setSettingsShow={setSettingsShow} votesToSkipProp={roomData.votes_to_skip} name={roomData.name} guestCanPauseState={roomData.guest_can_pause} isPublicState={roomData.isPublic} codeState={roomData.code} updateCallback={() => {}}/>
        ) : (
            <div className='flex flex-col gap-2'>
                {roomData.is_creator ? (<div className='flex justify-end w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white'>
                    <Link className='px-2 py-1' onClick={() => setSettingsShow(true)}>
                        <i class="fa-solid fa-pen-to-square"></i>
                    </Link>
                </div>) : <></>}
                {roomFound ? (
                    <>
                        <h1 className="flex w-screen justify-center m-2 font-bold">{roomData.name}</h1>
                        <p className="flex w-screen justify-center m-2">Votes : {roomData.votes_to_skip}</p>
                        <p className="flex w-screen justify-center m-2">Code : {roomData.code}</p>
                        <p className="flex w-screen justify-center m-2" p>GuestCanPause : {roomData.guest_can_pause ? 'Yes' : 'No'}</p>
                        <div class="flex w-screen justify-center m-2"><button className='flex justify-center m-2 font-bold w-fit bg-red-500 text-white px-2 py-1 rounded-md active:bg-red-700 hover:shadow-lg' onClick={leaveButton}> {roomData.is_creator ? 'CLOSE' : 'LEAVE'}</button></div>
                    </>
                ) : (
                    setRoomFound(false),
                    <p>Room with code {roomCode} not found</p>
                )}
            </div>
        )}
        </>
    );
}