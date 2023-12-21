import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect } from 'react-router-dom';

export default function Homepage(){

    const [data, setData] = useState(null);
    const navigate = useNavigate();

    const getCsrfToken = () => {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
        return cookie ? cookie.split('=')[1] : null;
    };
    
    const csrftoken = getCsrfToken();

    useEffect(() => {
        fetch('/apis/room')
            .then(response => response.json())
            .then(data => setData(data));
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/apis/in-room');
            const data = await response.json();
            if (data.message !== 'Room Not Found') {
                console.log(data.code);
                await navigate(`/room/${data.code}`);
            }
        }
        fetchData();
    }, []);

    const handleSubmit = (roomCode) => {
        
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
            alert('Room not found');
        });
    };

        return(
            <>
            <nav className="flex font-bold w-screen justify-evenly shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white py-1">
            <Link to="/profile">Profile</Link>
            <Link to="/login">Login</Link>
            <Link to="/create">Create Room</Link>
            <Link to="/join">Join Room</Link>
            </nav>

            <h1 className="flex w-screen justify-center m-2 font-bold">This is homepage</h1>

            <div className='relative'>
            <div className='mx-2 my-2 w-1/3 h-[calc(90vh-64px)] overflow-y-auto sm:overflow-y-scroll sm:overflow-hidden bg-opacity-70 bg-gradient-to-t from-slate-100 via-cyan-100 to-slate-100 rounded-md sm:absolute sm:right-5 shadow-lg sm:w-1/3 scrollbar-hide'>
            <div className='sticky top-0 text-center shadow-sm bg-opacity-70 bg-gradient-to-t from-sky-600 to-sky-400 text-sky-900 text-2xl py-2 px-4 font-bold'>Rooms</div>
                <div className='flex flex-col gap-4 p-4'>
                    {data && data.map((item, index) => (
                        <div className='border-solid border-2 border-slate-200 bg-white bg-opacity-90 shadow-md rounded-md p-1' key={index}> 
                        <div className='bg-opacity-100'>
                            <h3 className='font-bold leading-loose text-blue-600 border-b-2 border-solid border-gray-300 shadow-sm text-center'>{item.name}</h3>
                            <p className='font-semibold leading-loose text-center'>-{item.created_user}</p>
                            <p className='text-sm leading-loose text-gray-500 font-italic text-center'>{
                                new Date(item.created_time).toLocaleString('en-GB', {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                    day: '2-digit',
                                    month: '2-digit',
                                    year: '2-digit'
                                })
                            }, {item.is_public ? (<div className="text-green-500 leading-loose text-center">Public</div>) : (<div className="text-red-500 leading-loose text-center">Private</div>)}</p>
                            </div>
                            {item.is_public && <button onClick={(event) => {
                                event.preventDefault();
                                handleSubmit(item.code);
                            }} className="btn w-100 font-bold float-right bg-gradient-to-r from-green-300 to-green-600 text-white px-2 py-1 rounded-md">JOIN</button>}
                                                        
                        </div>
                    ))}
                </div>
            </div>
            </div>
        </>
        );
}