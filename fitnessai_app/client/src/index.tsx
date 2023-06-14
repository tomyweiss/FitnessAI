import ReactDOM from 'react-dom';
import './assets/css/index.css';
import {BrowserRouter, Switch, Route,} from 'react-router-dom';
import LandingPage from './components/LandingPage';
import { Store } from './store/reducer'
import { Provider } from "react-redux"

ReactDOM.render(
  <Provider store={Store}>
    <BrowserRouter>
      <Switch>
        <Route path="/" component={LandingPage} />
      </Switch>
    </BrowserRouter>
  </Provider>
  ,
  document.getElementById('root'));