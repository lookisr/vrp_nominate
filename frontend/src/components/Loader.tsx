export const Loader = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-cyan-400 border-t-transparent mx-auto mb-4"></div>
        <p className="text-blue-200 text-sm">Загрузка...</p>
      </div>
    </div>
  );
};

