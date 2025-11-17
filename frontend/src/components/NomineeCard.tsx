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
    ? nominee.image_path
    : `/${nominee.image_path}`;

  return (
    <div className="group cursor-pointer">
      <div className="relative aspect-square w-full rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300">
        <img
          src={imageUrl}
          alt={nominee.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
        {showVoteButton && (
          <div className="absolute bottom-0 left-0 right-0 p-3">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onVote?.();
              }}
              disabled={isVotingDisabled}
              className={`w-full py-2.5 px-4 rounded-full text-sm font-bold transition-all duration-200 ${
                isVotingDisabled
                  ? 'bg-gray-400/50 text-gray-200 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-500 to-cyan-400 text-white hover:from-blue-600 hover:to-cyan-500 active:scale-95 shadow-lg'
              }`}
            >
              Проголосовать
            </button>
          </div>
        )}
      </div>
      <div className="mt-3 px-2">
        <h3 className="text-base font-bold text-white text-left line-clamp-2">
          {nominee.name}
        </h3>
        {nominee.vote_count !== undefined && (
          <p className="text-sm text-blue-200 mt-1">Голосов: {nominee.vote_count}</p>
        )}
      </div>
    </div>
  );
};

