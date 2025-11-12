export const MainPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Премия года VRP</h1>
          <p className="text-gray-600">
            Добро пожаловать на церемонию вручения премии года!
          </p>
        </div>
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">О премии</h2>
            <p className="text-gray-600 mb-4">
              Премия года VRP — это ежегодная церемония награждения лучших в различных номинациях.
            </p>
            <p className="text-gray-600">
              Выберите номинацию и проголосуйте за вашего фаворита!
            </p>
          </div>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-blue-800 text-sm">
              💡 Используйте нижнее меню для навигации по приложению
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

