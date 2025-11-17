import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { NominationCard } from '../components/NominationCard';
import { ErrorMessage } from '../components/ErrorMessage';
import { Loader } from '../components/Loader';

export const NominationsPage = () => {
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
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-lg">Номинации пока не добавлены</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-24">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white text-center mb-8">
          Голосование за номинации
        </h1>
        <div className="grid grid-cols-2 gap-4">
          {nominations.map((nomination) => (
            <NominationCard
              key={nomination.id}
              nomination={nomination}
              to={`/nominations/${nomination.id}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

