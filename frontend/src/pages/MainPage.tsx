export const MainPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-24">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4 drop-shadow-lg">
            🏆 Премия года VRP
          </h1>
          <p className="text-blue-200 text-lg">
            Добро пожаловать на церемонию вручения премии года!
          </p>
        </div>
        <div className="max-w-2xl mx-auto">
          <div className="bg-white/10 backdrop-blur-md rounded-3xl shadow-xl p-6 mb-6 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-4">✨ О премии</h2>
            <p className="text-blue-100 mb-4 leading-relaxed">
              Премия года VRP — это ежегодная церемония награждения лучших в различных номинациях.
            </p>
            <p className="text-blue-100 leading-relaxed">
              Выберите номинацию и проголосуйте за вашего фаворита!
            </p>
          </div>
          <div className="bg-gradient-to-r from-blue-500/20 to-cyan-400/20 backdrop-blur-sm border border-blue-400/50 rounded-2xl p-4">
            <p className="text-blue-100 text-sm text-center">
              💡 Используйте нижнее меню для навигации по приложению
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

