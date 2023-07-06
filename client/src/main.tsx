import ReactDOM from 'react-dom/client'
import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client'
import App from './App'
import { AppSettings } from '../appSettings'
import './index.css'

//import configureStore from './src/configureStore'
//const { store } = configureStore()

const graphqlServer = AppSettings.SERVER;

const client = new ApolloClient({
    uri: graphqlServer,
    cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
root.render(
    <ApolloProvider client={client}>
        <App title="Arctic SPA" />
    </ApolloProvider>
);
