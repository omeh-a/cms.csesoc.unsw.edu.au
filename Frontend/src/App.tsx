import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { Provider } from 'react-redux';
import { GlobalStore } from 'src/redux-state/index';

// imports
import Dashboard from './packages/dashboard/Dashboard';
import Editor from './packages/editor/Editor';

import './css/styles.css'


const App: React.FC = () => {

  return (
    <div className="App">
      <Provider store={GlobalStore}>
        <Router>
          <Switch>
            <Route path="/" element={<Dashboard/>}/>
            <Route path="/editor" element={<Editor/>}/>
          </Switch>
        </Router>
      </Provider>
    </div>
  );
}

export default App;
