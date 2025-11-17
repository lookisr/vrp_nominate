import { Link, useLocation } from 'react-router-dom';

export const NavBar = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-indigo-900 to-blue-900 border-t border-blue-500/30 shadow-2xl z-50 backdrop-blur-lg">
      <div className="flex justify-around items-center h-16">
        <Link
          to="/"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-all ${
            isActive('/') 
              ? 'text-cyan-400 scale-110' 
              : 'text-blue-200 hover:text-white'
          }`}
        >
          <span className="text-2xl mb-1">🏠</span>
          <span className="text-xs font-medium">Главная</span>
        </Link>
        <Link
          to="/nominations"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-all ${
            isActive('/nominations') || location.pathname.startsWith('/nominations/')
              ? 'text-cyan-400 scale-110' 
              : 'text-blue-200 hover:text-white'
          }`}
        >
          <span className="text-2xl mb-1">🗳️</span>
          <span className="text-xs font-medium">Голосование</span>
        </Link>
        <Link
          to="/results"
          className={`flex flex-col items-center justify-center flex-1 h-full transition-all ${
            isActive('/results') || location.pathname.startsWith('/results/')
              ? 'text-cyan-400 scale-110' 
              : 'text-blue-200 hover:text-white'
          }`}
        >
          <span className="text-2xl mb-1">🏆</span>
          <span className="text-xs font-medium">Итоги</span>
        </Link>
      </div>
    </nav>
  );
};

