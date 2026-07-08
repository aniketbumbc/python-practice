// TODO: currentUser store
import { create } from 'zustand';
import type { User } from '@/lib/types';

type AuthState = {
  currentUser: User | null;
  login: (u: User) => void;
  logout: () => void;
  isOwner: (authorId: string) => boolean;
};

export const useAuth = create<AuthState>((set, get) => ({
  currentUser: null,
  login: (u) => set({ currentUser: u }),
  logout: () => set({ currentUser: null }),
  isOwner: (authorId) => get().currentUser?.id === authorId,
}));
