import type { Nominee } from '../types';

interface NomineeCardProps {
  nominee: Nominee;
  onVote?: () => void;
  showVoteButton?: boolean;
  isVotingDisabled?: boolean;
}

export const NomineeCard = ({
  nominee,
  onVote,
  showVoteButton = false,
  isVotingDisabled = false,
}: NomineeCardProps) => {
  const imageUrl = nominee.image_path.startsWith('http')
    ? nominee.image_path
    : nominee.image_path.startsWith('/')
    ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${nominee.image_path}`
    : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/${nominee.image_path}`;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="aspect-square w-full">
        <img
          src={imageUrl}
          alt={nominee.name}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-3">
        <h3 className="text-sm font-semibold text-gray-800 mb-2">{nominee.name}</h3>
        {nominee.vote_count !== undefined && (
          <p className="text-xs text-gray-600 mb-2">Голосов: {nominee.vote_count}</p>
        )}
        {showVoteButton && (
          <button
            onClick={onVote}
            disabled={isVotingDisabled}
            className={`w-full py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              isVotingDisabled
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800'
            }`}
          >
            Проголосовать
          </button>
        )}
      </div>
    </div>
  );
};

