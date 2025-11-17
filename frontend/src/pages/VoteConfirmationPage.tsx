import { useLocation, useNavigate } from 'react-router-dom';

export const VoteConfirmationPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { nomineeName, voteCount } = location.state || {};

  if (!nomineeName) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-lg mb-4">Данные о голосовании не найдены</p>
          <button
            onClick={() => navigate('/nominations')}
            className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white py-3 px-8 rounded-full hover:from-blue-600 hover:to-cyan-500 transition-all font-bold shadow-lg"
          >
            Вернуться к номинациям
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-20 flex items-center justify-center">
      <div className="container mx-auto px-4">
        <div className="max-w-md mx-auto bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl shadow-2xl p-8 text-center">
          <div className="mb-6">
            <div className="w-24 h-24 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span className="text-5xl text-white">✓</span>
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Голос учтён!</h1>
          </div>
          <div className="mb-8">
            <p className="text-blue-200 mb-2">Вы проголосовали за:</p>
            <p className="text-2xl font-bold text-white mb-4">{nomineeName}</p>
            <p className="text-blue-200">
              Всего голосов: <span className="font-bold text-cyan-400 text-xl">{voteCount || 0}</span>
            </p>
          </div>
          <div className="space-y-3">
            <button
              onClick={() => navigate('/nominations')}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-400 text-white py-3 px-6 rounded-full hover:from-blue-600 hover:to-cyan-500 transition-all font-bold shadow-lg"
            >
              Вернуться к номинациям
            </button>
            <button
              onClick={() => navigate('/results')}
              className="w-full bg-white/10 backdrop-blur-sm text-white border border-white/30 py-3 px-6 rounded-full hover:bg-white/20 transition-all font-bold"
            >
              Посмотреть итоги
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

