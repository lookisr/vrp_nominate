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
    ? `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${nomination.image_path}`
    : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/${nomination.image_path}`;

  const content = (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="aspect-square w-full">
        <img
          src={imageUrl}
          alt={nomination.title}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-3">
        <h3 className="text-sm font-semibold text-gray-800 text-center line-clamp-2">
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

