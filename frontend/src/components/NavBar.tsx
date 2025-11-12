import { Link, useLocation } from 'react-router-dom';

export const NavBar = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
      <div className="flex justify-around items-center h-16">
        <Link
          to="/"
          className={`flex flex-col items-center justify-center flex-1 h-full ${
            isActive('/') ? 'text-blue-600' : 'text-gray-600'
          }`}
        >
          <span className="text-xl mb-1">🏠</span>
          <span className="text-xs">Главная</span>
        </Link>
        <Link
          to="/nominations"
          className={`flex flex-col items-center justify-center flex-1 h-full ${
            isActive('/nominations') ? 'text-blue-600' : 'text-gray-600'
          }`}
        >
          <span className="text-xl mb-1">📋</span>
          <span className="text-xs">Номинации</span>
        </Link>
        <Link
          to="/results"
          className={`flex flex-col items-center justify-center flex-1 h-full ${
            isActive('/results') ? 'text-blue-600' : 'text-gray-600'
          }`}
        >
          <span className="text-xl mb-1">🏆</span>
          <span className="text-xs">Итоги</span>
        </Link>
      </div>
    </nav>
  );
};

