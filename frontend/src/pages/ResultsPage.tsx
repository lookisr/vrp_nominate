import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { NominationCard } from '../components/NominationCard';
import { ErrorMessage } from '../components/ErrorMessage';
import { Loader } from '../components/Loader';

export const ResultsPage = () => {
  const { data: nominations, isLoading, error, refetch } = useQuery({
    queryKey: ['nominations'],
    queryFn: api.getNominations,
  });

  if (isLoading) return <Loader />;
  if (error) {
    return (
      <ErrorMessage
        message="Не удалось загрузить номинации. Попробуйте позже."
        onRetry={() => refetch()}
      />
    );
  }

  if (!nominations || nominations.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 text-lg">Номинации пока не добавлены</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Итоги</h1>
        <p className="text-gray-600 mb-6">Выберите номинацию для просмотра результатов</p>
        <div className="grid grid-cols-2 gap-4">
          {nominations.map((nomination) => (
            <NominationCard
              key={nomination.id}
              nomination={nomination}
              to={`/results/${nomination.id}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

