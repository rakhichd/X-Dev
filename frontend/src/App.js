import './App.css';
import { Sidebar, Main } from './components';

function App() {
  return (
    <div className="App">
      <div className='flex'>
        <Sidebar />
        <Main />
      </div>
    </div>
  );
}

export default App;
