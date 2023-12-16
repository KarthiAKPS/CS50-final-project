import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';


export default function Login(){

        return(
            <>
            <div className='flex flex-col gap-2 justify-center items-center'>
            <div className='flex justify-end w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white'>
                <Link className='px-2 py-1' to="/"><i class="fa-solid fa-house"></i></Link>
                </div>
                <h1 className='text-center text-3xl font-bold py-2'>Login</h1>
                <div className='flex flex-col mx-4 my-2 md:w-1/2'>
                    <div className='flex flex-col gap-2 my-2'>
                    <label htmlFor="roomName">Email ID</label>
                    <input type="text" id="roomName" className='border-2 border-black rounded-md'/>
                    </div>
                    <div className='flex my-4 justify-center'>
                        <button
                            className='bg-gradient-to-r from-sky-300 to-sky-600 text-white font-bold px-2 py-1 rounded-md'
                        >Login</button>
                    </div>
                </div>
                </div>
            </>
        );
}