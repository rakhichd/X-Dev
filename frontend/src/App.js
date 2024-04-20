import './App.css';
import { Sidebar, Main } from './components';

function App() {
  return (
    <div className="App">
      <div>
        <Sidebar />
        <div className='ml-[80px]'>
        <Main />

        </div>
      </div>
    </div>
  );
}

export default App;
