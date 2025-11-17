import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/client';
import { NomineeCard } from '../components/NomineeCard';
import { ErrorMessage } from '../components/ErrorMessage';
import { Loader } from '../components/Loader';

export const NominationVotingPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const nominationId = parseInt(id || '0', 10);

  const { data: nomination, isLoading: isLoadingNomination } = useQuery({
    queryKey: ['nomination', nominationId],
    queryFn: () => api.getNomination(nominationId),
    enabled: !!nominationId,
  });

  const { data: nominees, isLoading: isLoadingNominees, error, refetch } = useQuery({
    queryKey: ['nominees', nominationId],
    queryFn: () => api.getNominees(nominationId),
    enabled: !!nominationId,
  });

  const voteMutation = useMutation({
    mutationFn: api.vote,
    onSuccess: (data) => {
      if (data.success) {
        queryClient.invalidateQueries({ queryKey: ['nominees', nominationId] });
        navigate(`/vote/confirm`, {
          state: {
            nomineeName: data.nominee_name,
            voteCount: data.vote_count,
          },
        });
      }
    },
  });

  const handleVote = (nomineeId: number) => {
    voteMutation.mutate({
      nominee_id: nomineeId,
      nomination_id: nominationId,
    });
  };

  if (isLoadingNomination || isLoadingNominees) return <Loader />;
  if (error) {
    return (
      <ErrorMessage
        message="Не удалось загрузить номинантов. Попробуйте позже."
        onRetry={() => refetch()}
      />
    );
  }

  if (!nominees || nominees.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-lg">Номинанты пока не добавлены</p>
        </div>
      </div>
    );
  }

  const isVotingDisabled = voteMutation.isPending || voteMutation.isError;

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-blue-900 to-purple-900 pb-24">
      <div className="container mx-auto px-4 py-6">
        {/* Кнопка категории */}
        <div className="flex justify-center mb-6">
          <div className="bg-gradient-to-r from-blue-500 to-cyan-400 px-6 py-3 rounded-full shadow-lg">
            <h1 className="text-xl font-bold text-white text-center">
              {nomination?.title || 'Голосование'}
            </h1>
          </div>
        </div>

        {voteMutation.isError && (
          <div className="bg-red-500/20 border border-red-400 rounded-lg p-4 mb-4">
            <p className="text-red-100 text-sm text-center">
              {voteMutation.error instanceof Error
                ? voteMutation.error.message
                : 'Не удалось проголосовать. Голосование может быть закрыто.'}
            </p>
          </div>
        )}
        {voteMutation.data && !voteMutation.data.success && (
          <div className="bg-yellow-500/20 border border-yellow-400 rounded-2xl p-6 mb-4">
            <p className="text-yellow-100 text-base font-bold text-center mb-4">
              {voteMutation.data.message}
            </p>
            {voteMutation.data.message.includes('подписаться на канал') && (
              <div className="flex justify-center">
                <a
                  href="https://t.me/vrpnews"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gradient-to-r from-blue-500 to-cyan-400 text-white py-3 px-8 rounded-full hover:from-blue-600 hover:to-cyan-500 transition-all font-bold shadow-lg inline-flex items-center gap-2"
                >
                  <span>📢</span>
                  Подписаться на канал
                </a>
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-2 gap-4">
          {nominees.map((nominee) => (
            <NomineeCard
              key={nominee.id}
              nominee={nominee}
              onVote={() => handleVote(nominee.id)}
              showVoteButton
              isVotingDisabled={isVotingDisabled}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

