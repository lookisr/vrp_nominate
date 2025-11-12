import { useLocation, useNavigate } from 'react-router-dom';

export const VoteConfirmationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { nomineeName, voteCount } = location.state || {};

  if (!nomineeName) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 text-lg mb-4">Данные о голосовании не найдены</p>
          <button
            onClick={() => navigate('/nominations')}
            className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 transition-colors"
          >
            Вернуться к номинациям
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
      <div className="container mx-auto px-4">
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="mb-6">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-4xl">✓</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Голос учтён!</h1>
          </div>
          <div className="mb-6">
            <p className="text-gray-600 mb-2">Вы проголосовали за:</p>
            <p className="text-xl font-semibold text-gray-800 mb-4">{nomineeName}</p>
            <p className="text-gray-600">
              Всего голосов: <span className="font-semibold text-blue-600">{voteCount || 0}</span>
            </p>
          </div>
          <div className="space-y-3">
            <button
              onClick={() => navigate('/nominations')}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 transition-colors font-medium"
            >
              Вернуться к номинациям
            </button>
            <button
              onClick={() => navigate('/results')}
              className="w-full bg-gray-200 text-gray-800 py-3 px-6 rounded-md hover:bg-gray-300 transition-colors font-medium"
            >
              Посмотреть итоги
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

