export interface Nomination {
  id: number;
  title: string;
  image_path: string;
  created_at: string;
}

export interface Nominee {
  id: number;
  nomination_id: number;
  name: string;
  image_path: string;
  created_at: string;
  vote_count?: number;
}

export interface VoteRequest {
  nominee_id: number;
  nomination_id: number;
}

export interface VoteResponse {
  success: boolean;
  message: string;
  nominee_name: string;
  vote_count: number;
  already_voted?: boolean;
}

export interface NominationResult {
  nomination_id: number;
  nomination_title: string;
  nominees: Nominee[];
}

export interface ResultsSummary {
  nominations: NominationResult[];
}

