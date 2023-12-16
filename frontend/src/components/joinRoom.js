import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function JoinRoom() {
    const [roomCode, setRoomCode] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (event) => {
        event.preventDefault();
        navigate(`/room/${roomCode}`);
    };

    return (
        <>
            <div className='flex flex-col gap-2 justify-center items-center'>
                <div className='flex justify-end w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white'>
                    <Link className='px-2 py-1' to="/"><i class="fa-solid fa-house"></i></Link>
                </div>
                <h1 className='text-center text-3xl font-bold py-2'>Join Room</h1>
                <div className='flex flex-col mx-4 my-2 md:w-1/2'>
                    <div className='flex flex-col gap-2 my-2'>
                        <label htmlFor="roomName">Room ID</label>
                        <input type="text" id="roomName" className='border-2 border-black rounded-md' value={roomCode} onChange={(e) => setRoomCode(e.target.value)} />
                    </div>
                    <div className='flex my-4 justify-center'>
                        <button
                            className='font-bold bg-gradient-to-r from-sky-300 to-sky-600 text-white px-2 py-1 rounded-md'
                            onClick={handleSubmit}
                        >Join</button>
                    </div>
                </div>
            </div>
        </>
    );
}