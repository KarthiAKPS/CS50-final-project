import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';

export default function Profile(){

        return(
            <>
            <div className='flex flex-col gap-2'>
                <div className='flex justify-end w-screen shadow-lg bg-gradient-to-b from-sky-300 to-sky-600 text-white'>
                <Link className='px-2 py-1' to="/"><i class="fa-solid fa-house"></i></Link>
                </div>
                <h1 className="flex w-screen justify-center m-2 font-bold">profile</h1>
                </div>
            </>
        );
}