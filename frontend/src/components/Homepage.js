import React, { Component } from 'react';
import profile from './profile';
import room from './room';
import login from './login';
import { BrowserRouter, Switch, Route, Link, Redirect } from 'react-router-dom';

export default class Homepage extends Component {
    constructor(props) {
        super(props);
    }

    render(){
        return(
            <BrowserRouter>
                <Switch>
                    <Route exact path='/'><p>This is the Home Page</p></Route>
                    <Route path="/profile" component={profile} />
                    <Route path="/room" component={room} />
                    <Route path="/login" component={login} />
                </Switch>
            </BrowserRouter>
        );
    }
}