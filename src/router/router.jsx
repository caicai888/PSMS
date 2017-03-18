import React from "react";
import {Router,Route,hashHistory,IndexRedirect} from "react-router";

import App from  '../components/app';
import Login from "../components/login";

import About from "../components/about";
import List from "../components/list";

import Welcome from "../components/welcome";

import CreateCustomer from "../components/create_customer";
import CustomerList from "../components/customer_list";

import CreateOffer from "../components/create_offer";
import OfferList from "../components/offer_list";
import OfferDetail from "../components/offer_detail";

import CreateManager from "../components/create_manager";
import ManagerList from "../components/manager_list";
import CreateGroup from "../components/create_group";
import GroupList from "../components/group_list";

import Dashboard from "../components/dashboard";

import CreateAgent from "../components/create_agent";
import AgentList from "../components/agent_list";


var Routers = <Router history={hashHistory}>
                <Route path="/"  component={App}>
                    <IndexRedirect to="/welcome" />

                    <Route path="/welcome" component={Welcome}/>

                    <Route path="/dashboard" component={Dashboard}/>

                    <Route path="/create_manager(/:id)" component={CreateManager}/>
                    <Route path="/manager_list" component={ManagerList}/>
                    <Route path="/create_group_manager(/:id)" component={CreateGroup}/>
                    <Route path="/group_list_manager" component={GroupList}/>


                    <Route path="/login" component={Login}/>

                    <Route path="/create_customer(/:id)" component={CreateCustomer}/>
                    <Route path="/customer_list" component={CustomerList}/>

                    <Route path="/create_offer(/:id)" component={CreateOffer}/>
                    <Route path="/offer_list" component={OfferList}/>
                    <Route path="/offer_detail/:id(/:three)" component={OfferDetail}/>

                    <Route path="/create_agent(/:id)" component={CreateAgent}/>
                    <Route path="/agent_list" component={AgentList}/>

                    <Route path="list(/:name)" component={List}/>
                    <Route path="about" component={About}/>
                </Route>
             </Router>

export default Routers;
