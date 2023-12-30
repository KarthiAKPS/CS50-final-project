import React from 'react';
import {render} from 'react-dom';
import Homepage from './Homepage';
import Profile from './profile';
import Room from './room';
import CreateRoom from './CreateRoom';
import JoinRoom from './joinRoom';
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';

export default function App(){

        return(
            <Router>
                <Routes>
                    <Route path="/" exact element={<Homepage/>}></Route>
                    <Route path="/profile" element={<Profile/>}></Route>
                    <Route path="/room/:roomCode" element={<Room/>}></Route>
                    <Route path="/create" element={<CreateRoom/>}></Route>
                    <Route path="/join" element={<JoinRoom/>}></Route>
                </Routes>
            </Router>
        )
    }

const appdiv = document.getElementById("app");
render(<App />, appdiv);