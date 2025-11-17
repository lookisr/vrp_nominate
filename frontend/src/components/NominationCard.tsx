import { Link } from 'react-router-dom';
import type { Nomination } from '../types';

interface NominationCardProps {
  nomination: Nomination;
  to?: string;
}

export const NominationCard = ({ nomination, to }: NominationCardProps) => {
  const imageUrl = nomination.image_path.startsWith('http')
    ? nomination.image_path
    : nomination.image_path.startsWith('/')
    ? nomination.image_path
    : `/${nomination.image_path}`;

  const content = (
    <div className="group cursor-pointer">
      <div className="relative aspect-square w-full rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-105">
        <img
          src={imageUrl}
          alt={nomination.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
      </div>
      <div className="mt-3 px-2">
        <h3 className="text-base font-bold text-white text-left line-clamp-2">
          {nomination.title}
        </h3>
      </div>
    </div>
  );

  if (to) {
    return <Link to={to}>{content}</Link>;
  }

  return content;
};

