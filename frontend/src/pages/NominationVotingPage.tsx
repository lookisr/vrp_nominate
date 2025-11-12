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
      <div className="min-h-screen bg-gray-50 pb-20 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 text-lg">Номинанты пока не добавлены</p>
        </div>
      </div>
    );
  }

  const isVotingDisabled = voteMutation.isPending || voteMutation.isError;

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          {nomination?.title || 'Голосование'}
        </h1>
        <p className="text-gray-600 mb-6">Выберите номинанта и проголосуйте</p>
        {voteMutation.isError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <p className="text-red-800 text-sm">
              {voteMutation.error instanceof Error
                ? voteMutation.error.message
                : 'Не удалось проголосовать. Голосование может быть закрыто.'}
            </p>
          </div>
        )}
        {voteMutation.data && !voteMutation.data.success && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <p className="text-yellow-800 text-sm font-medium">
              {voteMutation.data.message}
            </p>
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

