import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { NomineeCard } from '../components/NomineeCard';
import { ErrorMessage } from '../components/ErrorMessage';
import { Loader } from '../components/Loader';

export const NominationResultsPage = () => {
  const { id } = useParams<{ id: string }>();
  const nominationId = parseInt(id || '0', 10);

  const { data: result, isLoading, error, refetch } = useQuery({
    queryKey: ['nomination-results', nominationId],
    queryFn: () => api.getNominationResults(nominationId),
    enabled: !!nominationId,
  });

  if (isLoading) return <Loader />;
  if (error) {
    return (
      <ErrorMessage
        message="Не удалось загрузить результаты. Попробуйте позже."
        onRetry={() => refetch()}
      />
    );
  }

  if (!result || !result.nominees || result.nominees.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 text-lg">Результаты пока недоступны</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">{result.nomination_title}</h1>
        <p className="text-gray-600 mb-6">Результаты голосования (по убыванию голосов)</p>
        <div className="space-y-4">
          {result.nominees.map((nominee, index) => (
            <div key={nominee.id} className="relative">
              {index === 0 && result.nominees[0] && result.nominees[0].vote_count && result.nominees[0].vote_count > 0 && (
                <div className="absolute -top-2 -right-2 bg-yellow-400 text-yellow-900 rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm z-10">
                  1
                </div>
              )}
              <NomineeCard nominee={nominee} showVoteButton={false} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

