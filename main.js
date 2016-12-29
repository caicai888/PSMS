/**
 * Created by sa on 16-12-15.
 */
require("./src/css/css");
import React from 'react';
import ReactDom from 'react-dom';
import Header from  './src/components/header';
import Footer from  './src/components/footer';
import Fixed from  './src/components/fixed';
import Routers from  './src/router/router';

ReactDom.render(<Header />,$("#header")[0]);
ReactDom.render(Routers,$("#app")[0]);
ReactDom.render(<Footer />,$("#footer")[0]);
ReactDom.render(<Fixed />,document.getElementById("fixed"));
