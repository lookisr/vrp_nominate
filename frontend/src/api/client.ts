import axios from 'axios';
import type { Nomination, Nominee, NominationResult, ResultsSummary, VoteRequest, VoteResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Получаем Telegram WebApp initData
const getTelegramInitData = (): string => {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    return window.Telegram.WebApp.initData || '';
  }
  return '';
};

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем interceptor для автоматической отправки Telegram initData
client.interceptors.request.use((config) => {
  const initData = getTelegramInitData();
  if (initData) {
    config.headers['X-Telegram-Init-Data'] = initData;
  }
  return config;
});

export const api = {
  // Номинации
  getNominations: async (): Promise<Nomination[]> => {
    const response = await client.get<{ nominations: Nomination[] }>('/nominations');
    return response.data.nominations;
  },

  getNomination: async (id: number): Promise<Nomination> => {
    const response = await client.get<Nomination>(`/nominations/${id}`);
    return response.data;
  },

  // Номинанты
  getNominees: async (nominationId: number): Promise<Nominee[]> => {
    const response = await client.get<{ nominees: Nominee[] }>(`/nominations/${nominationId}/nominees`);
    return response.data.nominees;
  },

  // Голосование
  vote: async (data: VoteRequest): Promise<VoteResponse> => {
    const response = await client.post<VoteResponse>('/votes', data);
    return response.data;
  },

  // Результаты
  getResults: async (): Promise<ResultsSummary> => {
    const response = await client.get<ResultsSummary>('/results');
    return response.data;
  },

  getNominationResults: async (nominationId: number): Promise<NominationResult> => {
    const response = await client.get<NominationResult>(`/results/${nominationId}`);
    return response.data;
  },
};

