import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../api/client';
import { NomineeCard } from '../components/NomineeCard';
import { ErrorMessage } from '../components/ErrorMessage';
import { Loader } from '../components/Loader';
import { CrownIcon } from '../components/Icons';

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
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-lg">Результаты пока недоступны</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-24">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-center mb-6">
          <div className="bg-gradient-to-r from-amber-500 to-yellow-400 px-6 py-3 rounded-full shadow-lg">
            <h1 className="text-xl font-bold text-white text-center">
              {result.nomination_title}
            </h1>
          </div>
        </div>
        <p className="text-blue-200 mb-6 text-center">Результаты голосования (по убыванию голосов)</p>
        <div className="grid grid-cols-2 gap-4">
          {result.nominees.map((nominee, index) => (
            <div key={nominee.id} className="relative">
              {index === 0 && result.nominees[0] && result.nominees[0].vote_count && result.nominees[0].vote_count > 0 && (
                <div className="absolute -top-2 -right-2 bg-gradient-to-r from-amber-400 to-yellow-500 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold text-lg z-10 shadow-lg border-2 border-white">
                  <CrownIcon className="w-6 h-6" />
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

