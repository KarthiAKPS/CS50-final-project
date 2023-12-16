import React, { useState } from 'react';
import { BrowserRouter as Router, useNavigate, Routes, Route, Link, Redirect } from 'react-router-dom';

export default function CreateRoom() {
    const [votesToSkip, setVotesToSkip] = useState(2);
    const navigate = useNavigate();

    const handleVotesToSkipChange = (event) => {
        const value = parseInt(event.target.value);
        if (value >= 0) {
            setVotesToSkip(value);
        }
    }

    const handleSubmit = () => {
        console.log('clicked');
        // Get the values from the input fields
        const roomName = document.getElementById('roomName').value;
        const guestCanPause = document.querySelector('input[name="GuestCanPause"]:checked').value;
        const votesToSkip = document.getElementById('votesToSkip').value;
        const isPublic = document.querySelector('input[name="isPublic"]:checked').value;
        
        // Validate the data
        if (roomName === '' || guestCanPause === '' || votesToSkip === '') {
            alert('All fields are required!');
        };


        // Make the HTTP request to the backend
        const request = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                name: roomName,
                guest_can_pause: guestCanPause,
                votes_to_skip: votesToSkip,
                is_public: isPublic
            })
        };
        
        fetch('/apis/create-room', request)
            .then(response => response.json())
                .then(data => {
                    // Navigate to the new room
                    navigate(`/room/${data.code}`);
                    console.log(data);
                })
                .catch(error => {
                    // Handle any errors that occur during the request
                    console.error(error);
                });
        }



    return (
        <>
            <div className='flex flex-col gap-2 justify-center items-center'>
                <div className='flex justify-end w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white'>
                    <Link className='px-2 py-1' to='/'>
                        <i class='fa-solid fa-house'></i>
                    </Link>
                </div>
                <h1 className='text-center text-3xl font-bold'>Create Room</h1>
                <div className='mx-4 my-2 md:w-1/2'>
                    <div className='flex flex-col gap-2 my-2'>
                        <label htmlFor='roomName'>Room Name</label>
                        <input type='text' id='roomName' className='border-2 border-black rounded-md' />
                    </div>
                    <div className='flex gap-2 my-2 align-items-center'>
                        <label>Guest Can Pause?</label>
                        <input
                            type='radio'
                            name='GuestCanPause'
                            className='w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                            value='1'
                        />
                        <label className='ms-2 text-sm font-medium text-gray-900 dark:text-gray-300'>
                            Yes
                        </label>
                        <input
                            type='radio'
                            name='GuestCanPause'
                            defaultChecked
                            className='w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                            value='0'
                        />
                        <label className='ms-2 text-sm font-medium text-gray-900 dark:text-gray-300'>
                            No
                        </label>
                    </div>
                    <div className='flex gap-2 my-2 align-items-center'>
                        <label>Availability</label>
                        <input
                            type='radio'
                            name='isPublic'
                            className='w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                            value='1'
                        />
                        <label className='ms-2 text-sm font-medium text-gray-900 dark:text-gray-300'>
                            Public
                        </label>
                        <input
                            type='radio'
                            name='isPublic'
                            defaultChecked
                            className='w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
                            value='0'
                        />
                        <label className='ms-2 text-sm font-medium text-gray-900 dark:text-gray-300'>
                            Private
                        </label>
                    </div>
                    <div className='flex flex-col gap-2 my-2'>
                        <label htmlFor='votesToSkip'>Votes to Skip</label>
                        <input
                            type='number'
                            id='votesToSkip'
                            className='border-2 border-black rounded-md text-center'
                            min='1'
                            value={votesToSkip}
                            onChange={handleVotesToSkipChange}
                        />
                    </div>
                    <div className='flex my-4 justify-center'>
                        <button
                            className='bg-gradient-to-r from-sky-300 to-sky-600 font-bold text-white px-2 py-1 rounded-md'
                            onClick={handleSubmit}
                        >Create</button>
                    </div>
                </div>
            </div>
        </>
    );
}
