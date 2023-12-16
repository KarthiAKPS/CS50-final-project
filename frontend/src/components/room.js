import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect, useParams } from 'react-router-dom';

export default function Room() {

    const [roomData, setRoomData] = useState({});
    const { roomCode } = useParams();
    const [roomFound, setRoomFound] = useState(true);

    useEffect(() => {
        fetch('/apis/room')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const room = data.find(room => room.code === roomCode);
                if (room) {
                    setRoomData(room);
                    console.log(room);
                } else {
                    setRoomFound(false);
                    console.log(`Room with code ${roomCode} not found`);
                }
            })
            .catch(error => console.log('Fetch error: ', error));
    }, [roomCode]);


    return (
        <>
            <div className='flex flex-col gap-2'>
                <div className='flex justify-end w-screen bg-gradient-to-b from-sky-300 to-sky-600 text-white shadow-lg'>
                    <Link className='px-2 py-1' to="/"><i class="fa-solid fa-house"></i></Link>
                </div>
                {roomFound ? (
                    <>
                        <h1 className="flex w-screen justify-center m-2 font-bold">{roomData.name}</h1>
                        <p>Votes : {roomData.votes_to_skip}</p>
                        <p>GuestCanPause : {roomData.guest_can_pause ? 'Yes' : 'No'}</p>
                    </>
                ) : (
                    <p>Room with code {roomCode} not found</p>
                )}
            </div>
        </>
    );
}